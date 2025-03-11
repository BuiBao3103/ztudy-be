from .models import Room, RoomParticipant, User, StudySession
import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.timezone import now
from django.db.models import F
from asgiref.sync import sync_to_async
from .serializers import UserSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
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

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        user = UserSerializer(self.user).data

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_joined',
                'user': user
            }
        )

        await self.broadcast_user_list()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        if hasattr(self, 'room') and hasattr(self, 'user'):
            await sync_to_async(
                lambda: RoomParticipant.objects.filter(room=self.room, user=self.user).update(is_out=True))()

            user = UserSerializer(self.user).data

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_left',
                    'user': user
                }
            )

            await self.broadcast_user_list()

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get("type")
            print(f"Message type: {message_type}")
            if message_type == "message":
                user = UserSerializer(self.user).data

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'user': user,
                        'message': text_data_json["message"]
                    }
                )
            elif message_type == "typing":
                user = UserSerializer(self.user).data

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'typing_status',
                        'is_typing': text_data_json["is_typing"],
                        'user': user
                    }
                )
        except json.JSONDecodeError:
            print("Invalid JSON received")
        except Exception as e:
            print(f"Error processing message: {str(e)}")

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'user': event['user'],
            'message': event['message']
        }))

    async def typing_status(self, event):
        print(f"Typing status: {event['is_typing']}")
        await self.send(text_data=json.dumps({
            'type': 'typing_status',
            'is_typing': event['is_typing'],
            'user': event['user']
        }))

    async def user_joined(self, event):
        # Gửi thông tin người dùng khi họ tham gia phòng
        await self.send(text_data=json.dumps({
            'type': 'user_joined',
            'user': event['user']
        }))

    async def user_left(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_left',
            'user': event['user']
        }))

    async def broadcast_user_list(self):
        participants = await sync_to_async(list)(
            RoomParticipant.objects.filter(room=self.room, is_out=False).select_related('user')
        )

        user_data_list = []
        for participant in participants:
            user_data = UserSerializer(participant.user).data
            user_data_list.append(user_data)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'update_user_list',
                'users': user_data_list
            }
        )

    async def update_user_list(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_list',
            'users': event['users']
        }))


class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if self.user.is_authenticated:
            await sync_to_async(User.objects.filter(id=self.user.id).update)(is_online=True)

            self.session_start = now()
            self.is_active = True

            await self.channel_layer.group_add("global_online_users", self.channel_name)
            await self.accept()

            await self.broadcast_online_count()

            asyncio.create_task(self.auto_update_study_time())

        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await sync_to_async(User.objects.filter(id=self.user.id).update)(is_online=False)
            self.is_active = False

            if hasattr(self, 'session_start'):
                await self.update_study_time(self.user, self.session_start, now())

            await self.channel_layer.group_discard("global_online_users", self.channel_name)
            await self.broadcast_online_count()

    async def auto_update_study_time(self):
        while self.is_active:
            await asyncio.sleep(360)
            if self.is_active:
                await self.update_study_time(self.user, self.session_start, now())
                self.session_start = now()

    async def update_study_time(self, user, session_start, session_end):
        study_duration = (session_end - session_start).total_seconds() / 3600
        study_date = session_start.date()

        record, created = await sync_to_async(StudySession.objects.get_or_create)(
            user=user, date=study_date
        )

        if created:
            record.total_time = study_duration
            await sync_to_async(record.save)()
        else:
            await sync_to_async(StudySession.objects.filter(id=record.id).update)(
                total_time=F('total_time') + study_duration
            )

    async def broadcast_online_count(self):
        online_count = await sync_to_async(User.objects.filter(is_online=True).count)()

        await self.channel_layer.group_send(
            "global_online_users",
            {
                "type": "update_online_count",
                "online_count": online_count
            }
        )

    async def update_online_count(self, event):
        await self.send(text_data=json.dumps({
            "type": "online_count",
            "online_count": event["online_count"]
        }))
