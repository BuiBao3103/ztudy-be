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
from .base import CloudinaryAdminMixin
from .forms import (
    BackgroundVideoAdminForm,
    RoomAdminForm,
    RoomCategoryAdminForm,
    UserAdminForm,
)
from ..utils import get_decoded_field


class RoomAdmin(CloudinaryAdminMixin, admin.ModelAdmin):
    form = RoomAdminForm
    list_display = (
        "id",
        "decoded_name",
        "type",
        "creator_user",
        "category",
        "max_participants",
        "is_active",
        "thumbnail_preview"
    )
    list_filter = ("type", "is_active", "category")
    search_fields = ("name", "creator_user__username", "code_invite")
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 20
    date_hierarchy = "created_at"

    def decoded_name(self, obj):
        return get_decoded_field(obj, 'name')

    decoded_name.short_description = "Name"


class UserAdmin(CloudinaryAdminMixin, admin.ModelAdmin):
    form = UserAdminForm
    list_display = (
        "id",
        "decoded_username",
        "email",
        "is_online",
        "monthly_level",
        "is_staff",
        "is_active",
        "avatar_preview"
    )
    list_filter = ("is_online", "monthly_level", "is_staff", "is_active")
    search_fields = ("username", "email")
    readonly_fields = ("created_at", "updated_at", "monthly_study_time")
    list_per_page = 20
    date_hierarchy = "date_joined"

    def decoded_username(self, obj):
        return get_decoded_field(obj, 'username')

    decoded_username.short_description = "Username"


class RoomCategoryAdmin(CloudinaryAdminMixin, admin.ModelAdmin):
    form = RoomCategoryAdminForm
    list_display = ("id", "decoded_name", "decoded_description", "thumbnail_preview")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 20
    date_hierarchy = "created_at"

    def decoded_name(self, obj):
        return get_decoded_field(obj, 'name')

    decoded_name.short_description = "Name"

    def decoded_description(self, obj):
        return get_decoded_field(obj, 'description')

    decoded_description.short_description = "Description"


class RoomParticipantAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "decoded_room",
        "decoded_user",
        "role",
        "is_out",
        "is_approved",
        "joined_at",
    )
    list_filter = ("role", "is_out", "is_approved")
    search_fields = ("room__name", "user__username")
    list_per_page = 20
    date_hierarchy = "joined_at"

    def decoded_room(self, obj):
        return get_decoded_field(obj.room, 'name')

    decoded_room.short_description = "Room"

    def decoded_user(self, obj):
        return get_decoded_field(obj.user, 'username')

    decoded_user.short_description = "User"


class BackgroundVideoAdmin(CloudinaryAdminMixin, admin.ModelAdmin):
    form = BackgroundVideoAdminForm
    list_display = ("id", "youtube_url", "decoded_type", "image_preview")
    list_filter = ("type",)
    search_fields = ("youtube_url",)
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 20
    date_hierarchy = "created_at"

    def decoded_type(self, obj):
        return get_decoded_field(obj.type, 'name')

    decoded_type.short_description = "Type"


class BackgroundVideoTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "decoded_name", "decoded_description")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 20
    date_hierarchy = "created_at"

    def decoded_name(self, obj):
        return get_decoded_field(obj, 'name')

    decoded_name.short_description = "Name"

    def decoded_description(self, obj):
        return get_decoded_field(obj, 'description')

    decoded_description.short_description = "Description"


class SessionGoalAdmin(admin.ModelAdmin):
    list_display = ("id", "decoded_goal", "status", "decoded_user")
    list_filter = ("status",)
    search_fields = ("goal", "user__username")
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 20
    date_hierarchy = "created_at"

    def decoded_goal(self, obj):
        return get_decoded_field(obj, 'goal')

    decoded_goal.short_description = "Goal"

    def decoded_user(self, obj):
        return get_decoded_field(obj.user, 'username')

    decoded_user.short_description = "User"


class MotivationalQuoteAdmin(admin.ModelAdmin):
    list_display = ("id", "decoded_quote", "decoded_author")
    search_fields = ("quote", "author")
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 20
    date_hierarchy = "created_at"

    def decoded_quote(self, obj):
        return get_decoded_field(obj, 'quote')

    decoded_quote.short_description = "Quote"

    def decoded_author(self, obj):
        return get_decoded_field(obj, 'author')

    decoded_author.short_description = "Author"


class SoundAdmin(admin.ModelAdmin):
    list_display = ("id", "decoded_name")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 20
    date_hierarchy = "created_at"

    def decoded_name(self, obj):
        return get_decoded_field(obj, 'name')

    decoded_name.short_description = "Name"


class InterestAdmin(admin.ModelAdmin):
    list_display = ("id", "decoded_user", "decoded_category", "created_at")
    list_filter = ("category",)
    search_fields = ("user__username", "category__name")
    list_per_page = 20
    date_hierarchy = "created_at"

    def decoded_user(self, obj):
        return get_decoded_field(obj.user, 'username')

    decoded_user.short_description = "User"

    def decoded_category(self, obj):
        return get_decoded_field(obj.category, 'name')

    decoded_category.short_description = "Category"


class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "decoded_user",
        "decoded_room",
        "joined_at",
        "left_at",
        "interaction_count",
    )
    list_filter = ("room",)
    search_fields = ("user__username", "room__name")
    readonly_fields = ("joined_at", "left_at")
    list_per_page = 20
    date_hierarchy = "joined_at"

    def decoded_user(self, obj):
        return get_decoded_field(obj.user, 'username')

    decoded_user.short_description = "User"

    def decoded_room(self, obj):
        return get_decoded_field(obj.room, 'name')

    decoded_room.short_description = "Room"


class StudySessionAdmin(admin.ModelAdmin):
    list_display = ("id", "decoded_user", "date", "total_time")
    list_filter = ("date",)
    search_fields = ("user__username",)
    list_per_page = 20
    date_hierarchy = "date"

    def decoded_user(self, obj):
        return get_decoded_field(obj.user, 'username')

    decoded_user.short_description = "User" 