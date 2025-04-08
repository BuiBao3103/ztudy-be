import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from core.models import (
    RoomParticipant,
    Role,
)
from socket_service.utils import (
    update_user_online_status,
    update_room_participant_status,
    get_room_participant,
    get_room_by_code,
    serialize_user,
)
from socket_service.serializers import (
    WebSocketMessageSerializer,
    RoomParticipantSerializer,
)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.code_invite = self.scope["url_route"]["kwargs"]["code_invite"]
        self.user = self.scope["user"]
        self.is_in_waiting_state = False

        try:
            self.room = await get_room_by_code(self.code_invite)
            if not self.room:
                await self.close()
                return

            self.room_group_name = f"chat_{self.room.id}"
            self.user_group_name = f"user_{self.user.id}"
        except Exception:
            await self.close()
            return

        await self.accept()
        await self.channel_layer.group_add(self.user_group_name, self.channel_name)

        participant = await get_room_participant(self.room.id, self.user.id)

        if not participant:
            await self.send_error("You are not a participant of this room.")
            await self.close()
            return

        if self.room.type == "PRIVATE" and not participant.is_approved:
            self.is_in_waiting_state = True
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await update_room_participant_status(self.room.id, self.user.id, False)

        user_data = serialize_user(self.user)
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "user_joined", "user": user_data}
        )

        await self.broadcast_participant_list()

        if participant.role in [Role.MODERATOR, Role.ADMIN]:
            await self.broadcast_pending_requests()

    async def send_error(self, message):
        await self.send(
            text_data=json.dumps(
                WebSocketMessageSerializer({"type": "error", "message": message}).data
            )
        )

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

        if hasattr(self, "room") and hasattr(self, "user"):
            await update_room_participant_status(self.room.id, self.user.id, True)
            await update_user_online_status(self.user.id, False)

            user_data = serialize_user(self.user)
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "user_left", "user": user_data}
            )

            await self.broadcast_participant_list()

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            serializer = WebSocketMessageSerializer(data=data)
            if not serializer.is_valid():
                return

            message_type = serializer.validated_data["type"]
            if message_type == "message":
                user_data = serialize_user(self.user)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chat_message",
                        "user": user_data,
                        "message": serializer.validated_data["message"],
                    },
                )
            elif message_type == "typing":
                user_data = serialize_user(self.user)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "typing_status",
                        "is_typing": serializer.validated_data["is_typing"],
                        "user": user_data,
                    },
                )
        except json.JSONDecodeError:
            print("Invalid JSON received")
        except Exception as e:
            print(f"Error processing message: {str(e)}")

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                WebSocketMessageSerializer(
                    {
                        "type": "chat_message",
                        "user": event["user"],
                        "message": event["message"],
                    }
                ).data
            )
        )

    async def typing_status(self, event):
        await self.send(
            text_data=json.dumps(
                WebSocketMessageSerializer(
                    {
                        "type": "typing_status",
                        "is_typing": event["is_typing"],
                        "user": event["user"],
                    }
                ).data
            )
        )

    async def broadcast_participant_list(self):
        participants = await sync_to_async(
            lambda: RoomParticipant.objects.filter(room=self.room).select_related(
                "user"
            )
        )()

        serialized_participants = RoomParticipantSerializer(
            participants, many=True
        ).data

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "update_participant_list",
                "participants": serialized_participants,
            },
        )

    async def update_participant_list(self, event):
        await self.send(
            text_data=json.dumps(
                WebSocketMessageSerializer(
                    {"type": "participant_list", "participants": event["participants"]}
                ).data
            )
        )

    async def broadcast_pending_requests(self):
        pending_requests = await sync_to_async(
            lambda: RoomParticipant.objects.filter(
                room=self.room, is_approved=False
            ).select_related("user")
        )()

        serialized_requests = RoomParticipantSerializer(
            pending_requests, many=True
        ).data

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "update_pending_requests",
                "pending_requests": serialized_requests,
            },
        )

    async def update_pending_requests(self, event):
        await self.send(
            text_data=json.dumps(
                WebSocketMessageSerializer(
                    {
                        "type": "pending_requests",
                        "pending_requests": event["pending_requests"],
                    }
                ).data
            )
        )

    async def user_approved(self, event):
        user = event["user"]
        room_id = event["room_id"]
        code_invite = event["code_invite"]

        if user["id"] == self.user.id and self.is_in_waiting_state:
            self.is_in_waiting_state = False

            # Add user to room group
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

            # Notify user about approval
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "user_approved",
                        "user": user,
                        "room_id": room_id,
                        "code_invite": code_invite,
                    }
                )
            )

            # Broadcast user joined to room
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "user_joined", "user": user}
            )

            # Update user list in room
            await self.broadcast_participant_list()

    async def user_rejected(self, event):
        user = event["user"]
        room_id = event["room_id"]
        code_invite = event["code_invite"]

        if user["id"] == self.user.id and self.is_in_waiting_state:
            self.is_in_waiting_state = False

            # Notify user about rejection
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "user_rejected",
                        "user": user,
                        "room_id": room_id,
                        "code_invite": code_invite,
                    }
                )
            )

    async def user_assigned_moderator(self, event):
        user = event["user"]
        room_id = event["room_id"]
        code_invite = event["code_invite"]

        if user["id"] == self.user.id:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "user_assigned_moderator",
                        "user": user,
                        "room_id": room_id,
                        "code_invite": code_invite,
                    }
                )
            )

            # Update user list in room
            await self.broadcast_pending_requests()
            await self.broadcast_participant_list()

    async def user_revoked_moderator(self, event):
        user = event["user"]
        room_id = event["room_id"]
        code_invite = event["code_invite"]

        if user["id"] == self.user.id:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "user_revoked_moderator",
                        "user": user,
                        "room_id": room_id,
                        "code_invite": code_invite,
                    }
                )
            )

            # Update user list in room
            await self.broadcast_pending_requests()
            await self.broadcast_participant_list()

    async def room_ended(self, event):
        """Handle room ended event"""

        await self.send(
            text_data=json.dumps(
                {
                    "type": "room_ended",
                    "room_id": event["room_id"],
                    "code_invite": event["code_invite"],
                }
            )
        )

        # Disconnect user from room
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )
