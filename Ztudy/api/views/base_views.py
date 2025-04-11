from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from ..pagination import CustomPagination

class BaseListCreateView(generics.ListCreateAPIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['id']
    pagination_class = CustomPagination

class BaseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class SwaggerExpandMixin:
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'expand',
                openapi.IN_QUERY,
                description="Expand related fields (e.g., 'type')",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
