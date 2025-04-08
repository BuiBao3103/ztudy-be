import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.timezone import now
from asgiref.sync import sync_to_async

from socket_service.utils import (
    update_user_online_status,
    update_study_time,
)
from socket_service.serializers import WebSocketMessageSerializer

from core.models import (
    User,
)


class OnlineStatusConsumer(AsyncWebsocketConsumer):
    # Dictionary to keep track of active connections per user
    active_connections = {}

    async def connect(self):
        self.user = self.scope["user"]

        if self.user.is_authenticated:
            # Add this connection to the user's active connections
            if self.user.id not in self.active_connections:
                self.active_connections[self.user.id] = set()
            self.active_connections[self.user.id].add(self.channel_name)

            # Update online status in database
            await update_user_online_status(self.user.id, True)

            self.session_start = now()
            self.is_active = True

            # Add to groups
            await self.channel_layer.group_add("global_online_users", self.channel_name)
            await self.channel_layer.group_add(
                f"user_{self.user.id}", self.channel_name
            )
            await self.accept()

            # Broadcast initial online count
            await self.broadcast_online_count()

            # Start auto-update task
            asyncio.create_task(self.auto_update_study_time())

        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            # Remove this connection from user's active connections
            if self.user.id in self.active_connections:
                self.active_connections[self.user.id].discard(self.channel_name)

                # If no more active connections, update online status
                if not self.active_connections[self.user.id]:
                    await update_user_online_status(self.user.id, False)
                    del self.active_connections[self.user.id]

                    # Broadcast user status update
                    await self.channel_layer.group_send(
                        "global_online_users",
                        {
                            "type": "user_status_update",
                            "user_id": self.user.id,
                            "is_online": False,
                        },
                    )

            self.is_active = False

            # Update study time if session was started
            if hasattr(self, "session_start"):
                new_level, new_monthly_time = await update_study_time(
                    self.user, self.session_start, now()
                )

                if new_level:
                    await self.send_achievement(new_level, new_monthly_time)

            # Remove from groups
            await self.channel_layer.group_discard(
                "global_online_users", self.channel_name
            )
            await self.channel_layer.group_discard(
                f"user_{self.user.id}", self.channel_name
            )

            # Broadcast updated online count
            await self.broadcast_online_count()

    async def auto_update_study_time(self):
        while self.is_active:
            await asyncio.sleep(15)
            if self.is_active:
                new_level, new_monthly_time = await update_study_time(
                    self.user, self.session_start, now()
                )

                if new_level:
                    await self.send_achievement(new_level, new_monthly_time)

                self.session_start = now()

    async def send_achievement(self, level, monthly_study_time):
        await self.send(
            text_data=json.dumps(
                WebSocketMessageSerializer(
                    {
                        "type": "send_achievement",
                        "level": level,
                        "monthly_study_time": monthly_study_time,
                    }
                ).data
            )
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
                WebSocketMessageSerializer(
                    {"type": "online_count", "online_count": event["online_count"]}
                ).data
            )
        )

    async def user_status_update(self, event):
        await self.send(
            text_data=json.dumps(
                WebSocketMessageSerializer(
                    {
                        "type": "user_status_update",
                        "user_id": event["user_id"],
                        "is_online": event["is_online"],
                    }
                ).data
            )
        )
