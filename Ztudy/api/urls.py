from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include
from . import views

# Set up Swagger Schema View
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
    path('users/', views.UserListCreate.as_view(), name='user-view-create'),
    path('users/<int:pk>/', views.UserRetrieveUpdateDestroy.as_view(), name='user-view-detail'),

    path('motivational-quotes/', views.MotivationalQuoteListCreate.as_view(), name='motivational-quote-view-create'),
    path('motivational-quotes/<int:pk>/', views.MotivationalQuoteRetrieveUpdateDestroy.as_view(), name='motivational-quote-view-detail'),

    # Swagger URL
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
]
