from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from ..pagination import CustomPagination
from ..serializers import UserSerializer, AddUserInterestSerializer, RoomCategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import User, Interest, RoomCategory
from ..exceptions import CustomAPIException

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['username', 'email', 'is_online']
    search_fields = ['username', 'email']
    ordering_fields = ['id', 'username']
    pagination_class = CustomPagination


class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'

class CheckUserPreferences(APIView):
    """
    API to check if a user has selected preferences.
    - Returns 400 if no preferences are found.
    - Returns a list of preferences if they exist.
    """

    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)

        # Get user's interests
        interests = Interest.objects.filter(user=user).select_related('category')

        # If no interests exist, return an error
        if not interests.exists():
            raise CustomAPIException("User has not selected any preferences")

        # Serialize the Room Categories (Preferences)
        categories = [interest.category for interest in interests]
        serialized_categories = RoomCategorySerializer(categories, many=True).data

        return Response({
            'message': 'User has selected preferences',
            'preferences': serialized_categories
        }, status=status.HTTP_200_OK)

class AddUserInterest(APIView):
    """
    API to allow a user to add interests (preferences).
    """

    @swagger_auto_schema(
        request_body=AddUserInterestSerializer,
        operation_description="Add interests for a specific user",
        responses={201: 'Interests added successfully'}
    )
    def post(self, request, pk, *args, **kwargs):
        """Add interests for a specific user"""
        user = get_object_or_404(User, pk=pk)  # Automatically raises 404 if user not found
        category_ids = request.data.get('category_ids', [])

        if not category_ids:
            raise CustomAPIException("Please provide at least one category ID.")

        # Fetch valid categories
        categories = RoomCategory.objects.filter(id__in=category_ids)
        if not categories.exists():
            raise CustomAPIException("Invalid category IDs provided.")

        # Add interests, avoiding duplicates
        interests_to_add = []
        for category in categories:
            if not Interest.objects.filter(user=user, category=category).exists():
                interests_to_add.append(Interest(user=user, category=category))

        if interests_to_add:
            Interest.objects.bulk_create(interests_to_add)

        return Response({'message': 'Interests added successfully'}, status=status.HTTP_201_CREATED)
