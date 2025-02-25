# Ztudy/api/urls.py

from allauth.account.views import ConfirmEmailView
from django.urls import path, include, re_path

from . import views
from django.contrib import admin

# Set up Swagger Schema View
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="User API",
        default_version='v1',
        description="API documentation for the User management",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", views.LoginPage.as_view(), name="login"),

    path('api/v1/users/', views.UserListCreate.as_view(), name='user-view-create'),
    path('api/v1/users/<int:pk>/', views.UserRetrieveUpdateDestroy.as_view(), name='user-view-detail'),


    # Motivational Quote URLs
    path('api/v1/motivational-quotes/', views.MotivationalQuoteListCreate.as_view(), name='motivational-quote-view-create'),
    path('api/v1/motivational-quotes/<int:pk>/', views.MotivationalQuoteRetrieveUpdateDestroy.as_view(), name='motivational-quote-view-detail'),
    path('api/v1/motivational-quotes/random-quote/', views.RandomMotivationalQuoteView.as_view(), name='random-quote'),

    # Background Video URLs
    path('api/v1/background-videos/', views.BackgroundVideoListCreate.as_view(), name='background-video-view-create'),
    path('api/v1/background-videos/<int:pk>/', views.BackgroundVideoRetrieveUpdateDestroy.as_view(), name='background-video-view-detail'),
    path('api/v1/background-video-types/', views.BackgroundVideoTypeListCreate.as_view(), name='background-video-type-view-create'),
    path('api/v1/background-video-types/<int:pk>/', views.BackgroundVideoTypeRetrieveUpdateDestroy.as_view(), name='background-video-type-view-detail'),

    # Auth URLs
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    re_path(r"^api/v1/auth/accounts/", include("allauth.urls")),
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/v1/auth/google/", views.GoogleLogin.as_view(), name="google_login"),
    path(
        "api/v1/auth/google/callback/",
        views.GoogleLoginCallback.as_view(),
        name="google_login_callback",
    ),
    re_path(
        "^auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$",
        ConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),

    # Swagger URL
    path('api/v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
]