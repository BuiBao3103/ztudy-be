import asyncio
import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import F
from django.utils.timezone import now

from core.models import (
    User,
    StudySession,
    MonthlyLevel,
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
            await sync_to_async(User.objects.filter(id=self.user.id).update)(
                is_online=True
            )

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
                    await sync_to_async(User.objects.filter(id=self.user.id).update)(
                        is_online=False
                    )
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
                await self.update_study_time(self.session_start, now())

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

            # Send achievement notification
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "send_achievement",
                        "level": new_level,
                        "monthly_study_time": new_monthly_time,
                    }
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
                {"type": "online_count", "online_count": event["online_count"]}
            )
        )

    async def user_status_update(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "user_status_update",
                    "user_id": event["user_id"],
                    "is_online": event["is_online"],
                }
            )
        )
