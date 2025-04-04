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
import tempfile
import os
from cloudinary.models import CloudinaryField


class CloudinaryUploadFormMixin(forms.ModelForm):
    def handle_cloudinary_upload(self, instance, field_name, folder, prefix):
        """
        Xử lý upload file lên Cloudinary
        Args:
            instance: Instance của model
            field_name: Tên trường CloudinaryField
            folder: Tên folder trên Cloudinary
            prefix: Prefix cho public_id
        """
        if field_name in self.files:
            file = self.files[field_name]
            if file:
                import cloudinary.uploader
                
                # Create a temporary file
                with tempfile.NamedTemporaryFile(delete=False) as temp:
                    for chunk in file.chunks():
                        temp.write(chunk)
                
                try:
                    # Use the temporary file for uploading
                    upload_result = cloudinary.uploader.upload(
                        temp.name,
                        folder=folder,
                        public_id=f"{prefix}_{instance.id}_{field_name}",
                        overwrite=True
                    )
                    setattr(instance, field_name, upload_result['secure_url'])
                    instance.save()
                except Exception as e:
                    print(f"Cloudinary upload error: {e}")
                    raise
                finally:
                    # Clean up the temporary file
                    os.unlink(temp.name)


class CloudinaryAdminMixin:
    def get_cloudinary_fields(self):
        """Lấy danh sách các trường CloudinaryField của model"""
        return [
            field.name for field in self.model._meta.fields 
            if isinstance(field, CloudinaryField)
        ]
    
    def get_readonly_fields(self, request, obj=None):
        """Thêm các trường preview và url cho mỗi CloudinaryField"""
        readonly_fields = list(super().get_readonly_fields(request, obj))
        
        for field_name in self.get_cloudinary_fields():
            preview_field = f"{field_name}_preview"
            url_field = f"{field_name}_url"
            if preview_field not in readonly_fields:
                readonly_fields.extend([preview_field, url_field])
        
        return readonly_fields

    def get_fieldsets(self, request, obj=None):
        """Thêm section cho mỗi CloudinaryField"""
        fieldsets = list(super().get_fieldsets(request, obj))
        
        for field_name in self.get_cloudinary_fields():
            preview_field = f"{field_name}_preview"
            url_field = f"{field_name}_url"
            
            fieldsets.append(
                (f'{field_name.title()} Information', {
                    'fields': (field_name, preview_field, url_field),
                    'classes': ('collapse',),
                    'description': f'Upload and preview {field_name}'
                })
            )
        
        return fieldsets

    def _get_preview_method(self, field_name):
        """Generate preview method for a field"""
        def preview_method(obj):
            value = getattr(obj, field_name)
            if value:
                return format_html(
                    '<img src="{}" width="100" height="auto" style="border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);" />', 
                    value
                )
            return "No image"
        preview_method.short_description = f"{field_name.title()} Preview"
        return preview_method

    def _get_url_method(self, field_name):
        """Generate URL method for a field"""
        def url_method(obj):
            value = getattr(obj, field_name)
            if value:
                return format_html('<a href="{}" target="_blank">{}</a>', value, value)
            return "No URL"
        url_method.short_description = f"{field_name.title()} URL"
        return url_method

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Dynamically add preview and URL methods for each CloudinaryField
        for field_name in self.get_cloudinary_fields():
            preview_method = self._get_preview_method(field_name)
            url_method = self._get_url_method(field_name)
            
            setattr(self, f'{field_name}_preview', preview_method)
            setattr(self, f'{field_name}_url', url_method)


class BackgroundVideoAdminForm(CloudinaryUploadFormMixin):
    class Meta:
        model = BackgroundVideo
        fields = ['youtube_url', 'type', 'image']
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # First save the instance to get an ID if it doesn't have one
        if instance.id is None:
            instance.save()
            
        # Handle the image upload using the mixin
        self.handle_cloudinary_upload(
            instance=instance,
            field_name='image',
            folder='ztudy/background-video-images',
            prefix='background-video'
        )
        
        if commit:
            instance.save()
            
        return instance


class RoomAdminForm(CloudinaryUploadFormMixin):
    class Meta:
        model = Room
        fields = '__all__'
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if instance.id is None:
            instance.save()
            
        self.handle_cloudinary_upload(
            instance=instance,
            field_name='thumbnail',
            folder='ztudy/room-thumbnails',
            prefix='room'
        )
        
        if commit:
            instance.save()
            
        return instance


class RoomCategoryAdminForm(CloudinaryUploadFormMixin):
    class Meta:
        model = RoomCategory
        fields = '__all__'
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if instance.id is None:
            instance.save()
            
        self.handle_cloudinary_upload(
            instance=instance,
            field_name='thumbnail',
            folder='ztudy/category-thumbnails',
            prefix='category'
        )
        
        if commit:
            instance.save()
            
        return instance


class UserAdminForm(CloudinaryUploadFormMixin):
    class Meta:
        model = User
        fields = '__all__'
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if instance.id is None:
            instance.save()
            
        self.handle_cloudinary_upload(
            instance=instance,
            field_name='avatar',
            folder='ztudy/user-avatars',
            prefix='user'
        )
        
        if commit:
            instance.save()
            
        return instance


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
        return decode_emoji(obj.name)

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
        return decode_emoji(obj.username)

    decoded_username.short_description = "Username"


class RoomCategoryAdmin(CloudinaryAdminMixin, admin.ModelAdmin):
    form = RoomCategoryAdminForm
    list_display = ("id", "decoded_name", "decoded_description", "thumbnail_preview")
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


class BackgroundVideoAdmin(CloudinaryAdminMixin, admin.ModelAdmin):
    form = BackgroundVideoAdminForm
    list_display = ("id", "youtube_url", "decoded_type", "image_preview")
    list_filter = ("type",)
    search_fields = ("youtube_url",)
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 20
    date_hierarchy = "created_at"

    def decoded_type(self, obj):
        return decode_emoji(obj.type.name)

    decoded_type.short_description = "Type"


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
