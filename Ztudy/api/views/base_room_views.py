from rest_flex_fields.views import FlexFieldsMixin
from rest_framework import generics

from .base_views import BaseListCreateView, BaseRetrieveUpdateDestroyView, SwaggerExpandMixin
from core.models import Room, RoomCategory, RoomParticipant
from ..serializers import RoomSerializer, RoomCategorySerializer, RoomParticipantSerializer
from ..pagination import CustomPagination


class BaseRoomView(FlexFieldsMixin, SwaggerExpandMixin):
    """Base class for room-related views with common functionality"""
    permit_list_expands = ["category", "creator_user"]


class RoomListCreate(BaseRoomView, BaseListCreateView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filterset_fields = ["code_invite", "category", "creator_user", "type"]


class RoomRetrieveUpdateDestroy(BaseRoomView, BaseRetrieveUpdateDestroyView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomCategoryListCreate(BaseRoomView, BaseListCreateView):
    queryset = RoomCategory.objects.all()
    serializer_class = RoomCategorySerializer


class RoomCategoryRetrieveUpdateDestroy(BaseRoomView, BaseRetrieveUpdateDestroyView):
    queryset = RoomCategory.objects.all()
    serializer_class = RoomCategorySerializer


class RoomParticipantListCreate(BaseRoomView, BaseListCreateView):
    queryset = RoomParticipant.objects.all()
    serializer_class = RoomParticipantSerializer
    filterset_fields = ["room"]
    permit_list_expands = ["room", "user"]


class RoomParticipantRetrieveUpdateDestroy(BaseRoomView, BaseRetrieveUpdateDestroyView):
    queryset = RoomParticipant.objects.all()
    serializer_class = RoomParticipantSerializer
    permit_list_expands = ["room", "user"] 