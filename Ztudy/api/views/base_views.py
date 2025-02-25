from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from ..pagination import CustomPagination

class BaseListCreateView(generics.ListCreateAPIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['id']
    pagination_class = CustomPagination

class BaseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
