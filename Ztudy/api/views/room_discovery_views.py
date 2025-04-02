from django.db.models import Count, Q, Avg
from rest_flex_fields.views import FlexFieldsMixin
from rest_framework import generics, permissions

from .base_views import SwaggerExpandMixin
from ..models import Room, UserActivityLog
from ..ml import content_based_filtering, collaborative_filtering
from ..serializers import RoomSerializer
from ..pagination import CustomPagination


class RoomTrendingList(FlexFieldsMixin, SwaggerExpandMixin, generics.ListAPIView):
    serializer_class = RoomSerializer
    pagination_class = CustomPagination
    permit_list_expands = ['category', 'creator_user']

    def get_queryset(self):
        # Get all active rooms and annotate participant count
        active_rooms = Room.objects.filter(
            is_active=True
        ).annotate(
            participant_count=Count(
                'participants',
                filter=Q(
                    participants__is_out=False,
                    participants__is_approved=True
                )
            )
        ).filter(
            participant_count__gt=0  # Filter out rooms with no participants
        )

        # Calculate average participant count
        avg_participants = active_rooms.aggregate(
            avg=Avg('participant_count')
        )['avg'] or 0

        # Get rooms with participant count >= average
        trending_rooms = active_rooms.filter(
            participant_count__gte=avg_participants
        ).order_by('-participant_count')

        return trending_rooms


class SuggestedRoomsAPIView(FlexFieldsMixin, SwaggerExpandMixin, generics.ListAPIView):
    """
    API view to suggest rooms to authenticated users based on their activity.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RoomSerializer
    pagination_class = CustomPagination
    permit_list_expands = ["category", "creator_user"]

    def get_queryset(self):
        """
        Determine the recommendation method based on the user's activity count.

        Returns:
            QuerySet: A queryset of recommended Room objects.
        """
        user = self.request.user
        activity_count = UserActivityLog.objects.filter(user=user).count()

        # Use content-based filtering for users with less than 20 activities
        if activity_count < 20:
            return content_based_filtering(user)
        # Use collaborative filtering for users with 20 or more activities
        return collaborative_filtering(user) 