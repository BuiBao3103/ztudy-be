from django.contrib import admin
from django.apps import apps
from django.utils.html import format_html
from .models import (
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
from .utils import decode_emoji
from django import forms
from cloudinary.forms import CloudinaryFileField


class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "decoded_name",
        "type",
        "creator_user",
        "category",
        "max_participants",
        "is_active",
    )
    list_filter = ("type", "is_active", "category")
    search_fields = ("name", "creator_user__username", "code_invite")
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 20
    date_hierarchy = "created_at"

    def decoded_name(self, obj):
        return decode_emoji(obj.name)

    decoded_name.short_description = "Name"


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "decoded_username",
        "email",
        "is_online",
        "monthly_level",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_online", "monthly_level", "is_staff", "is_active")
    search_fields = ("username", "email")
    readonly_fields = ("created_at", "updated_at", "monthly_study_time")
    list_per_page = 20
    date_hierarchy = "date_joined"

    def decoded_username(self, obj):
        return decode_emoji(obj.username)

    decoded_username.short_description = "Username"


class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "decoded_name", "decoded_description")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 20
    date_hierarchy = "created_at"

    def decoded_name(self, obj):
        return decode_emoji(obj.name)

    decoded_name.short_description = "Name"

    def decoded_description(self, obj):
        return decode_emoji(obj.description) if obj.description else None

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
        return decode_emoji(obj.room.name)

    decoded_room.short_description = "Room"

    def decoded_user(self, obj):
        return decode_emoji(obj.user.username)

    decoded_user.short_description = "User"


class BackgroundVideoAdminForm(forms.ModelForm):
    class Meta:
        model = BackgroundVideo
        fields = ['youtube_url', 'type', 'image']
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Save the instance first to get an ID if it's a new instance
        if not instance.id:
            instance.save()
            commit = False
        
        # Handle image upload if a file was provided
        if 'image' in self.files:
            image_file = self.files['image']
            if image_file:
                import cloudinary.uploader
                upload_result = cloudinary.uploader.upload(
                    image_file,
                    folder="ztudy/background-video-images/",
                    public_id=f"background-video_{instance.id}_image",
                    overwrite=True
                )
                instance.image = upload_result['secure_url']
        
        if commit:
            instance.save()
        return instance


class BackgroundVideoAdmin(admin.ModelAdmin):
    form = BackgroundVideoAdminForm
    list_display = ("id", "youtube_url", "decoded_type", "image_preview")
    list_filter = ("type",)
    search_fields = ("youtube_url",)
    readonly_fields = ("created_at", "updated_at", "image_preview", "image_url")
    list_per_page = 20
    date_hierarchy = "created_at"
    fieldsets = (
        (None, {
            'fields': ('youtube_url', 'type', 'image'),
            'description': 'Enter the YouTube URL and select a type. You can also upload an image.'
        }),
        ('Image Information', {
            'fields': ('image_preview', 'image_url'),
            'classes': ('collapse',),
            'description': 'Image preview and URL information'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Creation and update timestamps'
        }),
    )

    def decoded_type(self, obj):
        return decode_emoji(obj.type.name)

    decoded_type.short_description = "Type"
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" height="auto" style="border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);" />', obj.image)
        return "No image"
    
    image_preview.short_description = "Image Preview"
    
    def image_url(self, obj):
        if obj.image:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.image, obj.image)
        return "No image URL"
    
    image_url.short_description = "Image URL"


class BackgroundVideoTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "decoded_name", "decoded_description")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 20
    date_hierarchy = "created_at"

    def decoded_name(self, obj):
        return decode_emoji(obj.name)

    decoded_name.short_description = "Name"

    def decoded_description(self, obj):
        return decode_emoji(obj.description) if obj.description else None

    decoded_description.short_description = "Description"


class SessionGoalAdmin(admin.ModelAdmin):
    list_display = ("id", "decoded_goal", "status", "decoded_user")
    list_filter = ("status",)
    search_fields = ("goal", "user__username")
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 20
    date_hierarchy = "created_at"

    def decoded_goal(self, obj):
        return decode_emoji(obj.goal)

    decoded_goal.short_description = "Goal"

    def decoded_user(self, obj):
        return decode_emoji(obj.user.username)

    decoded_user.short_description = "User"


class MotivationalQuoteAdmin(admin.ModelAdmin):
    list_display = ("id", "decoded_quote", "decoded_author")
    search_fields = ("quote", "author")
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 20
    date_hierarchy = "created_at"

    def decoded_quote(self, obj):
        return decode_emoji(obj.quote)

    decoded_quote.short_description = "Quote"

    def decoded_author(self, obj):
        return decode_emoji(obj.author)

    decoded_author.short_description = "Author"


class SoundAdmin(admin.ModelAdmin):
    list_display = ("id", "decoded_name")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 20
    date_hierarchy = "created_at"

    def decoded_name(self, obj):
        return decode_emoji(obj.name)

    decoded_name.short_description = "Name"


class InterestAdmin(admin.ModelAdmin):
    list_display = ("id", "decoded_user", "decoded_category", "created_at")
    list_filter = ("category",)
    search_fields = ("user__username", "category__name")
    list_per_page = 20
    date_hierarchy = "created_at"

    def decoded_user(self, obj):
        return decode_emoji(obj.user.username)

    decoded_user.short_description = "User"

    def decoded_category(self, obj):
        return decode_emoji(obj.category.name)

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
        return decode_emoji(obj.user.username)

    decoded_user.short_description = "User"

    def decoded_room(self, obj):
        return decode_emoji(obj.room.name)

    decoded_room.short_description = "Room"


class StudySessionAdmin(admin.ModelAdmin):
    list_display = ("id", "decoded_user", "date", "total_time")
    list_filter = ("date",)
    search_fields = ("user__username",)
    list_per_page = 20
    date_hierarchy = "date"

    def decoded_user(self, obj):
        return decode_emoji(obj.user.username)

    decoded_user.short_description = "User"


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
