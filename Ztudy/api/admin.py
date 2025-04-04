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


class CloudinaryUploadMixin:
    """
    Mixin to handle Cloudinary image uploads for admin forms.
    """
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Save the instance first to get an ID if it's a new instance
        if not instance.id:
            instance.save()
            commit = False
        
        # Handle image upload if a file was provided
        for field_name, field in self.fields.items():
            if isinstance(field, CloudinaryFileField) and field_name in self.files:
                image_file = self.files[field_name]
                if image_file:
                    import cloudinary.uploader
                    upload_result = cloudinary.uploader.upload(
                        image_file,
                        folder=f"ztudy/{instance._meta.model_name}-images/",
                        public_id=f"{instance._meta.model_name}_{instance.id}_{field_name}",
                        overwrite=True
                    )
                    setattr(instance, field_name, upload_result['secure_url'])
        
        if commit:
            instance.save()
        return instance


class RoomAdminForm(CloudinaryUploadMixin, forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'type', 'thumbnail', 'creator_user', 'code_invite', 'category', 'max_participants', 'is_active']


class UserAdminForm(CloudinaryUploadMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_online', 'avatar', 'monthly_level', 'is_staff', 'is_active']


class RoomCategoryAdminForm(CloudinaryUploadMixin, forms.ModelForm):
    class Meta:
        model = RoomCategory
        fields = ['name', 'description', 'thumbnail']


class BackgroundVideoAdminForm(CloudinaryUploadMixin, forms.ModelForm):
    class Meta:
        model = BackgroundVideo
        fields = ['youtube_url', 'type', 'image']


class RoomAdmin(admin.ModelAdmin):
    form = RoomAdminForm
    list_display = (
        "id",
        "decoded_name",
        "thumbnail_preview",
        "type",
        "creator_user",
        "category",
        "max_participants",
        "is_active",
    )
    list_filter = ("type", "is_active", "category")
    search_fields = ("name", "creator_user__username", "code_invite")
    readonly_fields = ("created_at", "updated_at", "thumbnail_preview", "thumbnail_url")
    list_per_page = 20
    date_hierarchy = "created_at"
    fieldsets = (
        (None, {
            'fields': ('name', 'type', 'thumbnail', 'creator_user', 'code_invite', 'category', 'max_participants', 'is_active'),
            'description': 'Enter room details and upload a thumbnail image.'
        }),
        ('Image Information', {
            'fields': ('thumbnail_preview', 'thumbnail_url'),
            'classes': ('collapse',),
            'description': 'Thumbnail preview and URL information'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Creation and update timestamps'
        }),
    )

    def decoded_name(self, obj):
        return decode_emoji(obj.name)

    decoded_name.short_description = "Name"
    
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="100" height="100" style="border-radius: 5px; object-fit: cover;" />', obj.thumbnail)
        return "No image"
    
    thumbnail_preview.short_description = "Thumbnail"
    
    def thumbnail_url(self, obj):
        if obj.thumbnail:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.thumbnail, obj.thumbnail)
        return "No image URL"
    
    thumbnail_url.short_description = "Thumbnail URL"


class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = (
        "id",
        "avatar_preview",
        "decoded_username",
        "email",
        "is_online",
        "monthly_level",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_online", "monthly_level", "is_staff", "is_active")
    search_fields = ("username", "email")
    readonly_fields = ("created_at", "updated_at", "monthly_study_time", "avatar_preview", "avatar_url")
    list_per_page = 20
    date_hierarchy = "date_joined"
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'is_online', 'avatar', 'monthly_level', 'is_staff', 'is_active'),
            'description': 'Enter user details and upload an avatar image.'
        }),
        ('Image Information', {
            'fields': ('avatar_preview', 'avatar_url'),
            'classes': ('collapse',),
            'description': 'Avatar preview and URL information'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'monthly_study_time'),
            'classes': ('collapse',),
            'description': 'Creation and update timestamps'
        }),
    )

    def decoded_username(self, obj):
        return decode_emoji(obj.username)

    decoded_username.short_description = "Username"
    
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="100" height="100" style="border-radius: 100%; object-fit: cover;" />', obj.avatar)
        return "No avatar"
    
    avatar_preview.short_description = "Avatar"
    
    def avatar_url(self, obj):
        if obj.avatar:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.avatar, obj.avatar)
        return "No avatar URL"
    
    avatar_url.short_description = "Avatar URL"


class RoomCategoryAdmin(admin.ModelAdmin):
    form = RoomCategoryAdminForm
    list_display = ("id", "thumbnail_preview", "decoded_name", "decoded_description")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at", "thumbnail_preview", "thumbnail_url")
    list_per_page = 20
    date_hierarchy = "created_at"
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'thumbnail'),
            'description': 'Enter category details and upload a thumbnail image.'
        }),
        ('Image Information', {
            'fields': ('thumbnail_preview', 'thumbnail_url'),
            'classes': ('collapse',),
            'description': 'Thumbnail preview and URL information'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Creation and update timestamps'
        }),
    )

    def decoded_name(self, obj):
        return decode_emoji(obj.name)

    decoded_name.short_description = "Name"

    def decoded_description(self, obj):
        return decode_emoji(obj.description) if obj.description else None

    decoded_description.short_description = "Description"
    
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="100" height="100" style="border-radius: 5px; object-fit: cover;" />', obj.thumbnail)
        return "No image"
    
    thumbnail_preview.short_description = "Thumbnail"
    
    def thumbnail_url(self, obj):
        if obj.thumbnail:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.thumbnail, obj.thumbnail)
        return "No image URL"
    
    thumbnail_url.short_description = "Thumbnail URL"


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
            return format_html('<img src="{}" width="100" height="auto" style="border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);" />', obj.image)
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
