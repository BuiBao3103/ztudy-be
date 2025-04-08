from django import forms
import tempfile
import os
from cloudinary.models import CloudinaryField
from core.models import (
    BackgroundVideo,
    Room,
    RoomCategory,
    User,
)


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