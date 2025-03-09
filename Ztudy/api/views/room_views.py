from rest_flex_fields.views import FlexFieldsMixin
from ..models import Room, RoomCategory, RoomParticipant, UserActivityLog, User
from ..serializers import RoomSerializer, RoomCategorySerializer, RoomParticipantSerializer, ThumbnailUploadSerializer
from .base_views import BaseListCreateView, BaseRetrieveUpdateDestroyView, SwaggerExpandMixin
from ..pagination import CustomPagination
from ..ml import content_based_filtering, collaborative_filtering
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status, generics, permissions
import cloudinary.uploader
import imghdr
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RoomListCreate(FlexFieldsMixin, SwaggerExpandMixin, BaseListCreateView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filterset_fields = ['code_invite', 'category', 'creator_user']
    permit_list_expands = ['category', 'creator_user']

class RoomRetrieveUpdateDestroy(FlexFieldsMixin, SwaggerExpandMixin, BaseRetrieveUpdateDestroyView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permit_list_expands = ['category', 'creator_user']

class UploadThumbnailView(generics.CreateAPIView):
    queryset = Room.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        request_body=ThumbnailUploadSerializer,
        responses={201: openapi.Response('Thumbnail uploaded successfully', ThumbnailUploadSerializer)},
        operation_description="Upload an thumbnail image to Cloudinary",
    )
    def post(self, request, *args, **kwargs):
        room = get_object_or_404(Room, id=kwargs['pk'])
        file = request.FILES.get('thumbnail')

        if not file:
            return Response({'detail': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        if not imghdr.what(file):
            return Response({'detail': 'Invalid image format'}, status=status.HTTP_400_BAD_REQUEST)

        upload_result = cloudinary.uploader.upload(
            file,
            folder="ztudy/thumbnails/",
            public_id=f"room_{room.id}_thumbnail",
            overwrite=True
        )

        room.thumbnail = upload_result['secure_url']
        room.save()

        return Response({'thumbnail': room.thumbnail}, status=status.HTTP_201_CREATED)

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
    """
    API view to suggest rooms to authenticated users based on their activity.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RoomSerializer
    pagination_class = CustomPagination
    permit_list_expands = ['category', 'creator_user']

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


class JoinRoomAPIView(APIView):
    """API cho phép user tham gia phòng."""
    def post(self, request, code_invite):
        room = get_object_or_404(Room, code_invite=code_invite)
        user = request.user

        # Kiểm tra xem user đã ở trong phòng chưa
        participant, created = RoomParticipant.objects.get_or_create(room=room, user=user)

        if room.type == "PRIVATE" and not participant.is_approved:
            return Response({'message': 'Waiting for admin approval'}, status=status.HTTP_202_ACCEPTED)

        participant.is_out = False  # Đánh dấu user đang ở trong phòng
        participant.is_approved = True  # Nếu phòng PUBLIC thì approved luôn
        participant.save()

        # Gửi sự kiện WebSocket thông báo user vào phòng
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{room.id}',
            {'type': 'user_joined', 'user_id': user.id, 'username': user.username}
        )

        return Response({'message': 'Joined room successfully!'}, status=status.HTTP_200_OK)


class LeaveRoomAPIView(APIView):
    """API cho phép user rời phòng."""
    def post(self, request, code_invite):
        room = get_object_or_404(Room, code_invite=code_invite)
        user = request.user

        participant = get_object_or_404(RoomParticipant, room=room, user=user)
        participant.is_out = True  # Đánh dấu là đã rời phòng
        participant.save()

        # Gửi sự kiện WebSocket thông báo user rời phòng
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{room.id}',
            {'type': 'user_left', 'user_id': user.id, 'username': user.username}
        )

        return Response({'message': 'Left room successfully!'}, status=status.HTTP_200_OK)


