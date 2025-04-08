from asgiref.sync import sync_to_async
from django.utils.timezone import now
from django.db.models import F
from core.models import User, StudySession, RoomParticipant, Room, MonthlyLevel
from api.serializers import UserSerializer


async def update_user_online_status(user_id: int, is_online: bool):
    """Update user's online status in the database"""
    await sync_to_async(User.objects.filter(id=user_id).update)(is_online=is_online)


async def update_room_participant_status(room_id: int, user_id: int, is_out: bool):
    """Update room participant's status"""
    await sync_to_async(
        RoomParticipant.objects.filter(room_id=room_id, user_id=user_id).update
    )(is_out=is_out)


async def get_room_participant(room_id: int, user_id: int):
    """Get room participant"""
    return await sync_to_async(
        lambda: RoomParticipant.objects.filter(room_id=room_id, user_id=user_id).first()
    )()


async def get_room_by_code(code_invite: str):
    """Get room by code invite"""
    return await sync_to_async(
        lambda: Room.objects.filter(code_invite=code_invite).first()
    )()


async def update_study_time(user, session_start, session_end):
    """Update user's study time and level"""
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
            total_time=F("total_time") + study_duration
        )

    await sync_to_async(User.objects.filter(id=user.id).update)(
        monthly_study_time=F("monthly_study_time") + study_duration
    )

    new_monthly_time = user.monthly_study_time + study_duration
    user.monthly_study_time = new_monthly_time

    new_level = MonthlyLevel.get_role_from_time(new_monthly_time)
    if MonthlyLevel.compare_levels(new_level, user.monthly_level) > 0:
        await sync_to_async(User.objects.filter(id=user.id).update)(
            monthly_level=new_level
        )
        user.monthly_level = new_level
        return new_level, new_monthly_time

    return None, new_monthly_time


def serialize_user(user):
    """Serialize user object to JSON"""
    return UserSerializer(user).data
