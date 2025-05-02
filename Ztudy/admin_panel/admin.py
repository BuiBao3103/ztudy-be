from django.contrib import admin
from django.urls import path
from django.shortcuts import render
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

# Tạo custom admin site
class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('chatbot/', self.admin_view(self.chatbot_view), name='admin_chatbot'),
        ]
        return custom_urls + urls
    
    def chatbot_view(self, request):
        context = {
            'title': 'Chatbot',
            'site_title': self.site_title,
            'site_header': self.site_header,
            'has_permission': self.has_permission(request),
            'available_apps': self.get_app_list(request),  # Quan trọng: Thêm app_list vào context
        }
        return render(request, 'admin/chatbot/index.html', context)
    
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        
        # Thêm mục chatbot vào danh sách ứng dụng
        custom_app = {
            'name': 'Công cụ bổ sung',
            'app_label': 'custom_tools',
            'app_url': '#',
            'has_module_perms': True,
            'models': [
                {
                    'name': 'Chatbot',
                    'object_name': 'Chatbot',
                    'admin_url': '/admin/chatbot/',
                    'view_only': True,
                }
            ]
        }
        
        app_list.append(custom_app)
        return app_list

# Tạo instance của CustomAdminSite
custom_admin_site = CustomAdminSite(name='custom_admin')

# Đăng ký models với custom admin site
custom_admin_site.register(Room, RoomAdmin)
custom_admin_site.register(User, UserAdmin)
custom_admin_site.register(RoomCategory, RoomCategoryAdmin)
custom_admin_site.register(RoomParticipant, RoomParticipantAdmin)
custom_admin_site.register(BackgroundVideo, BackgroundVideoAdmin)
custom_admin_site.register(BackgroundVideoType, BackgroundVideoTypeAdmin)
custom_admin_site.register(SessionGoal, SessionGoalAdmin)
custom_admin_site.register(MotivationalQuote, MotivationalQuoteAdmin)
custom_admin_site.register(Sound, SoundAdmin)
custom_admin_site.register(Interest, InterestAdmin)
custom_admin_site.register(UserActivityLog, UserActivityLogAdmin)
custom_admin_site.register(StudySession, StudySessionAdmin)