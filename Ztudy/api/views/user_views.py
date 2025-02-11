from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from ..models import User
from ..pagination import CustomPagination
from ..serializers import UserSerializer


class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['username', 'email']
    search_fields = ['username', 'email']
    ordering_fields = ['id', 'username']
    pagination_class = CustomPagination

class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
