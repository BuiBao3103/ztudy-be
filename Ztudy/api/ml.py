import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
from .models import Room, UserActivityLog, Interest


def get_user_interests(user):
    """
    Retrieve the interests (categories) of the user.
    """
    interests = Interest.objects.filter(user=user).values_list('category_id', flat=True)
    return list(interests)


def content_based_filtering(user):
    """
    Content-Based Filtering: Recommend rooms based on the user's interests, but include all public rooms.
    """
    interests = get_user_interests(user)

    # Get all public rooms
    rooms = Room.objects.filter(type="PUBLIC", is_active=True)
    room_data = pd.DataFrame(list(rooms.values('id', 'name', 'category_id')))

    # Assign a "priority" score based on whether the room's category matches the user's interests
    room_data['priority'] = room_data['category_id'].apply(lambda x: 1 if x in interests else 2)

    # Sort rooms: First by priority (rooms that match interests come first), then by the newest rooms
    filtered_rooms = room_data.sort_values(by=['priority', 'id'], ascending=[True, False])  # Sort by priority and id (newest)

    # Convert the sorted DataFrame back into a queryset of Room objects to be compatible with pagination
    room_ids = filtered_rooms['id'].tolist()
    return Room.objects.filter(id__in=room_ids)



def collaborative_filtering(user):
    """
    Collaborative Filtering: Recommend rooms based on the behavior of similar users.
    """
    # Get all user activity logs for the current user
    activity_logs = UserActivityLog.objects.filter(user=user)
    if activity_logs.count() < 5:  # Not enough data, fall back to Content-Based Filtering
        return content_based_filtering(user)

    # Create a user-room interaction matrix
    room_ids = Room.objects.values_list('id', flat=True)
    user_room_matrix = pd.DataFrame(0, index=[user.id], columns=room_ids)

    # Fill in the interaction data (1 for rooms the user has interacted with)
    for log in activity_logs:
        user_room_matrix.at[user.id, log.room.id] = 1

    # Calculate cosine similarity between users
    similarity_matrix = cosine_similarity(user_room_matrix)

    # Use NearestNeighbors to find similar users
    knn = NearestNeighbors(n_neighbors=5, metric='cosine')
    knn.fit(user_room_matrix.T)  # Room-based matrix
    similar_users = knn.kneighbors(user_room_matrix.T, n_neighbors=5)

    # Recommend rooms based on the activities of similar users
    suggested_rooms = []
    for similar_user_id in similar_users[0]:
        similar_user_logs = UserActivityLog.objects.filter(user_id=similar_user_id)
        for log in similar_user_logs:
            if log.room.id not in suggested_rooms:
                suggested_rooms.append(log.room.id)

    return Room.objects.filter(id__in=suggested_rooms)


def get_suggested_rooms(user):
    """
    Get a list of recommended rooms for the user.
    - Use Content-Based Filtering if the user has insufficient data.
    - Use Collaborative Filtering when sufficient data is available.
    """
    # Count the number of activity logs for the user
    activity_count = UserActivityLog.objects.filter(user=user).count()

    if activity_count < 5:
        return content_based_filtering(user)  # Not enough data, use Content-Based Filtering
    else:
        return collaborative_filtering(user)  # Enough data, use Collaborative Filtering
