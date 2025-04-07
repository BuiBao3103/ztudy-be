from django.contrib import admin
from cloudinary.models import CloudinaryField
from ..utils import render_image_preview, render_url_link


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
            return render_image_preview(value)
        preview_method.short_description = f"{field_name.title()} Preview"
        return preview_method

    def _get_url_method(self, field_name):
        """Generate URL method for a field"""
        def url_method(obj):
            value = getattr(obj, field_name)
            return render_url_link(value)
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