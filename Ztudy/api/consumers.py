import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Room, RoomParticipant, User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Xử lý kết nối WebSocket."""
        self.code_invite = self.scope['url_route']['kwargs']['code_invite']
        self.user = self.scope["user"]

        try:
            self.room = await sync_to_async(Room.objects.get)(code_invite=self.code_invite)
            self.room_group_name = f'chat_{self.room.id}'
        except Room.DoesNotExist:
            await self.close()
            return

        participant = await sync_to_async(
            lambda: RoomParticipant.objects.filter(room=self.room, user=self.user, is_out=False).first())()

        if not participant:
            await self.close()
            return

        if self.room.type == "PRIVATE" and not participant.is_approved:
            await self.close()
            return

        # Add to group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Notify others that user has joined
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'user_joined', 'username': self.user.username}
        )

        # Broadcast updated user list
        await self.broadcast_user_list()

    async def disconnect(self, close_code):
        # Remove from group
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # Update participant status to 'is_out'
        if hasattr(self, 'room') and hasattr(self, 'user'):
            await sync_to_async(
                lambda: RoomParticipant.objects.filter(room=self.room, user=self.user).update(is_out=True))()

            # Notify others that user has left
            await self.channel_layer.group_send(
                self.room_group_name,
                {'type': 'user_left', 'username': self.user.username}
            )

            # Broadcast updated user list
            await self.broadcast_user_list()

    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get("type")

            if message_type == "message":
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'username': self.user.username,
                        'message': text_data_json["message"]
                    }
                )
            elif message_type == "typing":
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'typing_status',
                        'is_typing': text_data_json["is_typing"],
                        'username': text_data_json["username"]
                    }
                )
        except json.JSONDecodeError:
            print("Invalid JSON received")
        except Exception as e:
            print(f"Error processing message: {str(e)}")

    async def chat_message(self, event):
        """Send chat message to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'username': event['username'],
            'message': event['message']
        }))

    async def typing_status(self, event):
        """Send typing status to WebSocket"""
        print(f"Typing status: {event['is_typing']}")
        await self.send(text_data=json.dumps({
            'type': 'typing_status',
            'is_typing': event['is_typing'],
            'username': event['username']
        }))

    async def user_joined(self, event):
        """Notify that a user has joined"""
        await self.send(text_data=json.dumps({
            'type': 'user_joined',
            'username': event['username']
        }))

    async def user_left(self, event):
        """Notify that a user has left"""
        await self.send(text_data=json.dumps({
            'type': 'user_left',
            'username': event['username']
        }))

    async def broadcast_user_list(self):
        """Send the updated user list to all clients in the room"""
        users = await sync_to_async(list)(
            RoomParticipant.objects.filter(room=self.room, is_out=False).values_list('user__username', flat=True)
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'update_user_list', 'users': users}
        )

    async def update_user_list(self, event):
        """Send the user list to the WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'user_list',
            'users': event['users']
        }))