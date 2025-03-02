from rest_flex_fields.views import FlexFieldsMixin
from ..models import Room, RoomCategory, RoomParticipant, Interest
from ..serializers import RoomSerializer, RoomCategorySerializer, RoomParticipantSerializer
from .base_views import BaseListCreateView, BaseRetrieveUpdateDestroyView, SwaggerExpandMixin
from ..pagination import CustomPagination
from rest_framework import generics, permissions
from ..ml import get_suggested_rooms

class RoomListCreate(FlexFieldsMixin, SwaggerExpandMixin, BaseListCreateView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permit_list_expands = ['category', 'creator_user']

class RoomRetrieveUpdateDestroy(FlexFieldsMixin, SwaggerExpandMixin, BaseRetrieveUpdateDestroyView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permit_list_expands = ['category', 'creator_user']

class RoomCategoryListCreate(FlexFieldsMixin, SwaggerExpandMixin, BaseListCreateView):
    queryset = RoomCategory.objects.all()
    serializer_class = RoomCategorySerializer

class RoomCategoryRetrieveUpdateDestroy(FlexFieldsMixin, SwaggerExpandMixin, BaseRetrieveUpdateDestroyView):
    queryset = RoomCategory.objects.all()
    serializer_class = RoomCategorySerializer

class RoomParticipantListCreate(FlexFieldsMixin, SwaggerExpandMixin, BaseListCreateView):
    queryset = RoomParticipant.objects.all()
    serializer_class = RoomParticipantSerializer
    permit_list_expands = ['room', 'user']

class RoomParticipantRetrieveUpdateDestroy(FlexFieldsMixin, SwaggerExpandMixin, BaseRetrieveUpdateDestroyView):
    queryset = RoomParticipant.objects.all()
    serializer_class = RoomParticipantSerializer
    permit_list_expands = ['room', 'user']


class SuggestedRoomsAPIView(FlexFieldsMixin, SwaggerExpandMixin, generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RoomSerializer
    pagination_class = CustomPagination
    permit_list_expands = ['category', 'creator_user']

    def get(self, request, *args, **kwargs):
        user = self.request.user  # Get the currently authenticated user

        # Get the recommended rooms based on the machine learning models (content-based or collaborative)
        suggested_rooms = get_suggested_rooms(user)

        # Apply pagination to the queryset
        paginator = CustomPagination()
        paginated_rooms = paginator.paginate_queryset(suggested_rooms, request)

        # Serialize the paginated room data and return as a response
        serializer = self.serializer_class(paginated_rooms, many=True)
        return paginator.get_paginated_response(serializer.data)

