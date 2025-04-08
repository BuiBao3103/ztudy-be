from django.contrib import admin
from core.models import (
    Room,
    User,
    RoomCategory,
    RoomParticipant,
    BackgroundVideo,
    BackgroundVideoType,
    SessionGoal,
    MotivationalQuote,
    Sound,
    Interest,
    UserActivityLog,
    StudySession,
)
from .model_admins import (
    RoomAdmin,
    UserAdmin,
    RoomCategoryAdmin,
    RoomParticipantAdmin,
    BackgroundVideoAdmin,
    BackgroundVideoTypeAdmin,
    SessionGoalAdmin,
    MotivationalQuoteAdmin,
    SoundAdmin,
    InterestAdmin,
    UserActivityLogAdmin,
    StudySessionAdmin,
)

# Register models with their admin classes
admin.site.register(Room, RoomAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(RoomCategory, RoomCategoryAdmin)
admin.site.register(RoomParticipant, RoomParticipantAdmin)
admin.site.register(BackgroundVideo, BackgroundVideoAdmin)
admin.site.register(BackgroundVideoType, BackgroundVideoTypeAdmin)
admin.site.register(SessionGoal, SessionGoalAdmin)
admin.site.register(MotivationalQuote, MotivationalQuoteAdmin)
admin.site.register(Sound, SoundAdmin)
admin.site.register(Interest, InterestAdmin)
admin.site.register(UserActivityLog, UserActivityLogAdmin)
admin.site.register(StudySession, StudySessionAdmin)
