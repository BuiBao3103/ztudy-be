from rest_flex_fields.views import FlexFieldsMixin
from ..models import Room, RoomCategory, RoomParticipant, Interest
from ..serializers import RoomSerializer, RoomCategorySerializer, RoomParticipantSerializer
from .base_views import BaseListCreateView, BaseRetrieveUpdateDestroyView, SwaggerExpandMixin
from ..pagination import CustomPagination
from django.db.models import Case, When, Value, IntegerField
from rest_framework import generics, permissions

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

    def get_queryset(self):
        user = self.request.user  # Get the currently authenticated user
        interests = Interest.objects.filter(user=user).values_list('category_id',
                                                                   flat=True)  # Retrieve category IDs that the user is interested in

        # Assign priority: Rooms that belong to the user's interests are given priority = 1, others are assigned priority = 2
        rooms = Room.objects.annotate(
            priority=Case(
                When(category_id__in=interests, then=Value(1)),
                # Rooms matching the user's interests → Higher priority (1)
                default=Value(2),  # Other rooms → Lower priority (2)
                output_field=IntegerField(),
            )
        ).filter(type="PUBLIC", is_active=True)  # Filter only public and active rooms

        # Order results: First by priority (preferred rooms first), then by newest rooms
        return rooms.order_by("priority", "-created_at")



