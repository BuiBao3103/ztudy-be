from .models import Room, UserActivityLog, Interest
from django.db.models import Case, When, Value, IntegerField, Count, Q


def get_user_interests(user):
    """
    Retrieve the interests (categories) of the user more efficiently.
    """
    return set(Interest.objects.filter(user=user).values_list('category_id', flat=True))


def content_based_filtering(user):
    """
    Content-Based Filtering: Recommend rooms based on user's interests with improved prioritization.
    """
    # Get the user's interests (categories)
    interests = get_user_interests(user)

    # Filter active public rooms
    rooms = Room.objects.filter(type="PUBLIC", is_active=True)

    # Add a 'priority' field to prioritize rooms based on the user's interests
    rooms = rooms.annotate(
        # Prioritize rooms that belong to the user's interest categories
        priority=Case(
            When(category_id__in=interests, then=Value(1)),  # If category matches interest, priority = 1
            default=Value(2),  # Otherwise, priority = 2
            output_field=IntegerField()
        )
    )

    # Order the rooms by priority and then by creation date (newest first)
    rooms = rooms.order_by('priority', '-created_at')

    return rooms

def collaborative_filtering(user):
    """
    Collaborative Filtering: Better implementation with weighted recommendations.
    """
    # Check activity count in a single query
    if UserActivityLog.objects.filter(user=user).count() < 5:
        return content_based_filtering(user)

    # Get rooms the user has interacted with
    user_room_ids = UserActivityLog.objects.filter(user=user).values_list('room_id', flat=True)

    # Find similar users more efficiently
    similar_users = UserActivityLog.objects.filter(
        room_id__in=user_room_ids
    ).exclude(
        user=user
    ).values_list('user', flat=True).distinct()

    # Use annotations to weight rooms by popularity among similar users
    return Room.objects.filter(
        Q(id__in=UserActivityLog.objects.filter(user__in=similar_users).values_list('room_id', flat=True)) &
        Q(type="PUBLIC", is_active=True)  # Ensure we only get public, active rooms
    ).annotate(
        # Use the correct related_name from UserActivityLog to Room
        similar_user_count=Count(
            'activity_logs__user',  # Assuming 'activity_logs' is the related_name
            distinct=True,
            filter=Q(activity_logs__user__in=similar_users)  # Also update here
        )
    ).order_by('-similar_user_count', '-created_at')


