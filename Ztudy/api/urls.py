from allauth.account.views import ConfirmEmailView
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.conf import settings
from . import views
from .admin import admin

schema_view = get_schema_view(
        openapi.Info(
                title="User API",
                default_version="v1",
                description="API documentation for the User management",
                terms_of_service="https://www.google.com/policies/terms/",
                contact=openapi.Contact(email="contact@myapi.com"),
                license=openapi.License(name="MIT License"),
        ),
        public=True,
        url='https://api.ztudy.io.vn/' if not settings.DEBUG else 'http://localhost:8000/',
)

urlpatterns = [
        path("admin/", admin.site.urls),
        path("login/", views.LoginPage.as_view(), name="login"),
        # User URLs
        path("api/v1/users/", views.UserList.as_view(), name="user-view"),
        path(
                "api/v1/users/<int:pk>/",
                views.UserRetrieveUpdateDestroy.as_view(),
                name="user-view-detail",
        ),
        path(
                "api/v1/users/<int:pk>/upload-avatar/",
                views.UploadAvatarView.as_view(),
                name="upload-avatar",
        ),
        path(
                "api/v1/users/<int:pk>/check-preferences/",
                views.CheckUserPreferences.as_view(),
                name="check-user-preferences",
        ),
        path(
                "api/v1/users/<int:pk>/add-interests/",
                views.AddUserInterest.as_view(),
                name="add-user-interests",
        ),
        # Motivational Quote URLs
        path(
                "api/v1/motivational-quotes/",
                views.MotivationalQuoteListCreate.as_view(),
                name="motivational-quote-view-create",
        ),
        path(
                "api/v1/motivational-quotes/<int:pk>/",
                views.MotivationalQuoteRetrieveUpdateDestroy.as_view(),
                name="motivational-quote-view-detail",
        ),
        path(
                "api/v1/motivational-quotes/random-quote/",
                views.RandomMotivationalQuoteView.as_view(),
                name="random-quote",
        ),
        # Background Video URLs
        path(
                "api/v1/background-videos/",
                views.BackgroundVideoListCreate.as_view(),
                name="background-video-view-create",
        ),
        path(
                "api/v1/background-videos/<int:pk>/upload-thumbnail/",
                views.UploadBackgroundVideoView.as_view(),
                name="upload-background-video-thumbnail",
        ),
        path(
                "api/v1/background-videos/<int:pk>/",
                views.BackgroundVideoRetrieveUpdateDestroy.as_view(),
                name="background-video-view-detail",
        ),
        path(
                "api/v1/background-video-types/",
                views.BackgroundVideoTypeListCreate.as_view(),
                name="background-video-type-view-create",
        ),
        path(
                "api/v1/background-video-types/<int:pk>/",
                views.BackgroundVideoTypeRetrieveUpdateDestroy.as_view(),
                name="background-video-type-view-detail",
        ),
        # Session Goal URLs
        path(
                "api/v1/session-goals/",
                views.SessionGoalListCreate.as_view(),
                name="session-goal-view-create",
        ),
        path(
                "api/v1/session-goals/<int:pk>/",
                views.SessionGoalRetrieveUpdateDestroy.as_view(),
                name="session-goal-view-detail",
        ),
        # Sound URLs
        path('api/v1/sounds/', views.SoundList.as_view(), name='sound-view'),
        path('api/v1/sounds/<int:pk>/',
             views.SoundDetail.as_view(), name='sound-view-detail'),
        path('api/v1/sounds/upload/', views.SoundUpload.as_view(), name='sound-upload'),
        path('api/v1/sounds/<int:pk>/stream/',
             views.StreamAudioView.as_view(), name='stream-audio'),

        # Room URLs
        path('api/v1/rooms/', views.RoomListCreate.as_view(), name='room-view-create'),
        path('api/v1/rooms/<int:pk>/upload-thumbnail/',
             views.UploadThumbnailView.as_view(), name='upload-thumbnail'),
        path('api/v1/rooms/<int:pk>/',
             views.RoomRetrieveUpdateDestroy.as_view(), name='room-view-detail'),
        path('api/v1/rooms/suggested/',
             views.SuggestedRoomsAPIView.as_view(), name='suggested-rooms'),
        path('api/v1/rooms/trending/',
             views.RoomTrendingList.as_view(), name='trending-rooms'),
        path('api/v1/rooms/<str:code_invite>/join/',
             views.JoinRoomAPIView.as_view(), name='join-room'),
        path('api/v1/rooms/join-random/',
             views.JoinRandomRoomAPIView.as_view(), name='join-random-room'),
        path('api/v1/rooms/<str:code_invite>/leave/',
             views.LeaveRoomAPIView.as_view(), name='leave-room'),
        path('api/v1/rooms/<str:code_invite>/cancel-join/',
             views.CancelJoinRoomAPIView.as_view(), name='cancel-join-room'),
        path('api/v1/rooms/<str:code_invite>/approve/<int:user_id>/',
             views.ApproveJoinRequestAPIView.as_view(), name='approve-join-request'),
        path('api/v1/rooms/<str:code_invite>/reject/<int:user_id>/',
             views.RejectJoinRequestAPIView.as_view(), name='reject-join-request'),
        path('api/v1/rooms/<str:code_invite>/assign-moderator/<int:user_id>/',
             views.AssignRoomModeratorAPIView.as_view(), name='assign-room-moderator'),
        path('api/v1/rooms/<str:code_invite>/revoke-moderator/<int:user_id>/',
             views.RevokeRoomModeratorAPIView.as_view(), name='revoke-room-moderator'),
        path('api/v1/rooms/<str:code_invite>/end/',
             views.EndRoomAPIView.as_view(), name='end-room'),

        # Room Category URLs
        path('api/v1/room-categories/', views.RoomCategoryListCreate.as_view(),
             name='room-category-view-create'),
        path('api/v1/room-categories/<int:pk>/', views.RoomCategoryRetrieveUpdateDestroy.as_view(),
             name='room-category-view-detail'),
        path("api/v1/room-categories/<int:pk>/upload-thumbnail/", views.UploadCategoryThumbnailView.as_view(),
             name="upload-category-thumbnail"),

        # Room Participant URLs
        path(
                "api/v1/room-participants/",
                views.RoomParticipantListCreate.as_view(),
                name="room-participant-view-create",
        ),
        path(
                "api/v1/room-participants/<int:pk>/",
                views.RoomParticipantRetrieveUpdateDestroy.as_view(),
                name="room-participant-view-detail",
        ),
        # Stats URLs
        path(
                "api/v1/stats/study-time/",
                views.StudyTimeStatsView.as_view(),
                name="study-time-stats",
        ),
        path(
                "api/v1/stats/study-time-chart/",
                views.StudyTimeChartView.as_view(),
                name="study-time-chart",
        ),
        path(
                "api/v1/stats/leaderboard/<str:period>/",
                views.LeaderboardView.as_view(),
                name="leader-board",
        ),
        # Auth URLs
        path("api/v1/auth/", include("dj_rest_auth.urls")),
                path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),
        path("api/v1/auth/google/", views.GoogleLogin.as_view(), name="google_login"),
        path("api/v1/auth/google/callback/", views.GoogleLoginCallback.as_view(), name="google_login_callback"),
        path("api/v1/auth/login/", views.LoginPage.as_view(), name="login_page"),
        re_path(r"^api/v1/auth/accounts/", include("allauth.urls")),
        re_path(
                "^auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$",
                ConfirmEmailView.as_view(),
                name="account_confirm_email",
        ),
        # Swagger URL
        path(
                "api/v1/swagger/",
                schema_view.with_ui("swagger", cache_timeout=0),
                name="swagger-ui",
        ),
        # Chat Room URL
        path("together/", views.chat_room, name="chat-room"),

        # Agora generate token
        path('api/v1/agora/token/', views.AgoraTokenView.as_view(), name='agora-token'),
]
