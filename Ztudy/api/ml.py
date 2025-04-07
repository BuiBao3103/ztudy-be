from django.db.models import Case, When, Value, IntegerField, Count
from core.models import Room, UserActivityLog, Interest


def get_user_interests(user):
    """
    Retrieve the interests (categories) of the user efficiently.
    """
    interests = Interest.objects.filter(user=user).values_list('category_id', flat=True)
    return set(interests) if interests.exists() else set()


def content_based_filtering(user):
    """
    Content-Based Filtering: Recommend rooms based on user's interests with improved prioritization.

    Args:
        user: The user object to generate recommendations for.

    Returns:
        QuerySet: A queryset of Room objects sorted by priority and creation date.
    """
    interests = get_user_interests(user)
    rooms = Room.objects.filter(type="PUBLIC", is_active=True)

    # If user has no interests, return rooms sorted by creation date
    if not interests:
        return rooms.order_by('-created_at')

    # Annotate rooms with priority based on user's interests
    rooms = rooms.annotate(
        priority=Case(
            When(category_id__in=interests, then=Value(1)),  # High priority for matching interests
            default=Value(10),  # Lower priority for non-matching interests
            output_field=IntegerField()
        )
    ).order_by('priority', '-created_at')  # Sort by priority and then by creation date

    return rooms


def collaborative_filtering(user):
    """
    Collaborative Filtering: Recommend rooms based on similar users' behavior.

    Args:
        user: The user object to generate recommendations for.

    Returns:
        QuerySet: A queryset of Room objects sorted by interaction count and creation date.
    """
    # Get room IDs the user has interacted with
    user_room_ids = UserActivityLog.objects.filter(user=user).values_list('room_id', flat=True)

    # If user has no interactions, return latest public rooms
    if not user_room_ids.exists():
        return Room.objects.filter(type="PUBLIC", is_active=True).order_by('-created_at')

    # Find similar users who interacted with the same rooms
    similar_users = UserActivityLog.objects.filter(
        room_id__in=user_room_ids
    ).exclude(user=user).values_list('user', flat=True).distinct()

    # Recommend rooms based on similar users' interactions
    recommended_rooms = Room.objects.filter(
        id__in=UserActivityLog.objects.filter(user__in=similar_users).values_list('room_id', flat=True),
        type="PUBLIC",
        is_active=True
    ).annotate(
        similar_user_count=Count('activity_logs__user', distinct=True)  # Count distinct users who interacted
    ).filter(
        similar_user_count__gte=2  # Filter rooms with at least 2 similar users
    ).order_by('-similar_user_count', '-created_at')[:50]  # Sort and limit to 50 results

    return recommended_rooms


