import asyncio
import json
from .models import (
    Role,
)
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import F
from django.utils.timezone import now

from .models import Room, RoomParticipant, User, StudySession, MonthlyLevel
from .serializers import UserSerializer
from django.db.models import F, Q
from django.utils.timezone import now

from .models import Room, RoomParticipant, User, StudySession


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.code_invite = self.scope["url_route"]["kwargs"]["code_invite"]
        self.user = self.scope["user"]
        self.is_in_waiting_state = False

        try:
            self.room = await sync_to_async(Room.objects.get)(
                code_invite=self.code_invite
            )
            self.room_group_name = f"chat_{self.room.id}"
            self.user_group_name = f"user_{self.user.id}"
        except Room.DoesNotExist:
            await self.close()
            return

        # Accept the connection right away
        await self.accept()

        # Always add user to their personal channel
        await self.channel_layer.group_add(self.user_group_name, self.channel_name)
        print(self.room.id)
        print(self.user.id)
        participant = await sync_to_async(
            lambda: RoomParticipant.objects.filter(
                room=self.room, user=self.user
            ).first()
        )()

        if not participant:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "error",
                        "message": "You are not a participant of this room.",
                    }
                )
            )
            await self.close()
            return

        if self.room.type == "PRIVATE" and not participant.is_approved:
            self.is_in_waiting_state = True
            return

        # User is approved, add them to the room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await sync_to_async(
            lambda: RoomParticipant.objects.filter(
                room=self.room, user=self.user
            ).update(is_out=False)
        )()
        user = UserSerializer(self.user).data

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "user_joined", "user": user}
        )

        await self.broadcast_participant_list()

        # If this is an admin and moderator, send them the pending requests list
        if participant.role == Role.MODERATOR or participant.role == Role.ADMIN:
            await self.broadcast_pending_requests()

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

    async def disconnect(self, close_code):

        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

        if hasattr(self, "room") and hasattr(self, "user"):
            await sync_to_async(
                lambda: RoomParticipant.objects.filter(
                    room=self.room, user=self.user
                ).update(is_out=True)
            )()

            await sync_to_async(
                lambda: User.objects.filter(id=self.user.id).update(is_online=False)
            )()

            user = UserSerializer(self.user).data

            await self.channel_layer.group_send(
                self.room_group_name, {"type": "user_left", "user": user}
            )

            await self.broadcast_participant_list()

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get("type")
            if message_type == "message":
                user = UserSerializer(self.user).data

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chat_message",
                        "user": user,
                        "message": text_data_json["message"],
                    },
                )
            elif message_type == "typing":
                user = UserSerializer(self.user).data

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "typing_status",
                        "is_typing": text_data_json["is_typing"],
                        "user": user,
                    },
                )
        except json.JSONDecodeError:
            print("Invalid JSON received")
        except Exception as e:
            print(f"Error processing message: {str(e)}")

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "chat_message",
                    "user": event["user"],
                    "message": event["message"],
                }
            )
        )

    async def typing_status(self, event):
        print(f"Typing status: {event['is_typing']}")
        await self.send(
            text_data=json.dumps(
                {
                    "type": "typing_status",
                    "is_typing": event["is_typing"],
                    "user": event["user"],
                }
            )
        )

    async def user_joined(self, event):
        # Gửi thông tin người dùng khi họ tham gia phòng
        await self.send(
            text_data=json.dumps({"type": "user_joined", "user": event["user"]})
        )

    async def user_left(self, event):
        await self.send(
            text_data=json.dumps({"type": "user_left", "user": event["user"]})
        )

    async def broadcast_participant_list(self):
        participants = await sync_to_async(list)(
            RoomParticipant.objects.filter(room=self.room, is_out=False).select_related(
                "user"
            )
        )

        participant_data_list = []
        for participant in participants:
            user_data = UserSerializer(participant.user).data
            participant_data = {
                "user": user_data,
                "role": participant.role,
                "is_approved": participant.is_approved,
                "is_out": participant.is_out,
            }
            participant_data_list.append(participant_data)

        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "update_participant_list", "participants": participant_data_list},
        )

    async def update_participant_list(self, event):
        await self.send(
            text_data=json.dumps(
                {"type": "participant_list", "participants": event["participants"]}
            )
        )

    async def broadcast_pending_requests(self):
        try:
            pending_requests = await sync_to_async(list)(
                RoomParticipant.objects.filter(
                    room=self.room, is_approved=False
                ).select_related("user")
            )

            request_list = []
            for participant in pending_requests:
                user_data = UserSerializer(participant.user).data
                participant_data = {
                    "user": user_data,
                    "role": participant.role,
                    "is_approved": participant.is_approved,
                    "is_out": participant.is_out,
                }
                request_list.append(participant_data)

            admin_participants = await sync_to_async(list)(
                RoomParticipant.objects.filter(room=self.room)
                .filter(Q(role=Role.ADMIN) | Q(role=Role.MODERATOR))
                .select_related("user")
            )
            for admin in admin_participants:
                admin_user_group = f"user_{admin.user.id}"
                await self.channel_layer.group_send(
                    admin_user_group,
                    {"type": "update_pending_requests", "requests": request_list},
                )
        except Exception as e:
            print(f"Error in broadcast_pending_requests: {str(e)}")

    async def update_pending_requests(self, event):
        await self.send(
            text_data=json.dumps(
                {"type": "pending_requests", "requests": event["requests"]}
            )
        )

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


class OnlineStatusConsumer(AsyncWebsocketConsumer):
    # Dictionary to keep track of active connections per user
    active_connections = {}

    async def connect(self):
        self.user = self.scope["user"]

        if self.user.is_authenticated:
            # Increment active connections counter for this user
            if self.user.id not in self.active_connections:
                self.active_connections[self.user.id] = 1
            else:
                self.active_connections[self.user.id] += 1

            # Only update is_online if this is the first connection
            if self.active_connections[self.user.id] == 1:
                await sync_to_async(User.objects.filter(id=self.user.id).update)(
                    is_online=True
                )

            self.session_start = now()
            self.is_active = True

            await self.channel_layer.group_add("global_online_users", self.channel_name)
            await self.channel_layer.group_add(
                f"user_{self.user.id}", self.channel_name
            )
            await self.accept()

            await self.broadcast_online_count()

            asyncio.create_task(self.auto_update_study_time())

        else:
            await self.close()

    async def disconnect(self, close_code):
        print(f"OnlineStatusConsumer disconnect called with close_code: {close_code}")
        if self.user.is_authenticated:
            # Decrement active connections counter
            if self.user.id in self.active_connections:
                self.active_connections[self.user.id] -= 1
                print(
                    f"Active connections for user {self.user.id}: {self.active_connections[self.user.id]}"
                )

                # Only update is_online if this was the last connection
                if self.active_connections[self.user.id] <= 0:
                    await sync_to_async(User.objects.filter(id=self.user.id).update)(
                        is_online=False
                    )
                    print(
                        f"Updating online status for user {self.user.id} to False - all connections closed"
                    )
                    del self.active_connections[self.user.id]

                    # Broadcast user status update to all users
                    await self.channel_layer.group_send(
                        "global_online_users",
                        {
                            "type": "user_status_update",
                            "user_id": self.user.id,
                            "is_online": False,
                        },
                    )

            self.is_active = False

            if hasattr(self, "session_start"):
                await self.update_study_time(self.session_start, now())

            await self.channel_layer.group_discard(
                "global_online_users", self.channel_name
            )
            await self.channel_layer.group_discard(
                f"user_{self.user.id}", self.channel_name
            )

            await self.broadcast_online_count()

    async def auto_update_study_time(self):
        while self.is_active:
            await asyncio.sleep(15)
            if self.is_active:
                await self.update_study_time(self.session_start, now())
                self.session_start = now()

    async def update_study_time(self, session_start, session_end):
        study_duration = (session_end - session_start).total_seconds() / 3600
        study_date = session_start.date()

        record, created = await sync_to_async(StudySession.objects.get_or_create)(
            user=self.user, date=study_date
        )

        if created:
            record.total_time = study_duration
            await sync_to_async(record.save)()
        else:
            await sync_to_async(StudySession.objects.filter(id=record.id).update)(
                total_time=F("total_time") + study_duration
            )

        await sync_to_async(User.objects.filter(id=self.user.id).update)(
            monthly_study_time=F("monthly_study_time") + study_duration
        )

        new_monthly_time = self.user.monthly_study_time + study_duration
        self.user.monthly_study_time = new_monthly_time

        new_level = MonthlyLevel.get_role_from_time(new_monthly_time)
        if MonthlyLevel.compare_levels(new_level, self.user.monthly_level) > 0:
            await sync_to_async(User.objects.filter(id=self.user.id).update)(
                monthly_level=new_level
            )
            self.user.monthly_level = new_level

            await self.send_level_achievement_notification(
                self.user.id, new_level, new_monthly_time
            )

    async def send_level_achievement_notification(
        self, user_id, new_level, monthly_study_time
    ):
        await self.channel_layer.group_send(
            f"user_{user_id}",
            {
                "type": "send_achievement",
                "level": new_level,
                "monthly_study_time": monthly_study_time,
            },
        )

    async def broadcast_online_count(self):
        online_count = await sync_to_async(User.objects.filter(is_online=True).count)()

        await self.channel_layer.group_send(
            "global_online_users",
            {"type": "update_online_count", "online_count": online_count},
        )

    async def update_online_count(self, event):

        await self.send(
            text_data=json.dumps(
                {"type": "online_count", "online_count": event["online_count"]}
            )
        )

    async def send_achievement(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "send_achievement",
                    "level": event["level"],
                    "monthly_study_time": event["monthly_study_time"],
                }
            )
        )

    async def user_status_update(self, event):
        """Handle user status update event"""
        await self.send(
            text_data=json.dumps(
                {
                    "type": "user_status_update",
                    "user_id": event["user_id"],
                    "is_online": event["is_online"],
                }
            )
        )
