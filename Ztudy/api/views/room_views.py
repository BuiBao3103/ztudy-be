import imghdr

import cloudinary.uploader
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_flex_fields.views import FlexFieldsMixin
from rest_framework import status, generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .base_views import BaseListCreateView, BaseRetrieveUpdateDestroyView, SwaggerExpandMixin
from ..ml import content_based_filtering, collaborative_filtering
from ..models import Room, RoomCategory, RoomParticipant, UserActivityLog
from ..pagination import CustomPagination
from ..serializers import RoomSerializer, RoomCategorySerializer, RoomParticipantSerializer, ThumbnailUploadSerializer, \
    UserSerializer, RoomJoinSerializer, CategoryThumbnailUploadSerializer


class RoomListCreate(FlexFieldsMixin, SwaggerExpandMixin, BaseListCreateView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filterset_fields = ['code_invite', 'category', 'creator_user', 'type']
    permit_list_expands = ['category', 'creator_user']


class RoomRetrieveUpdateDestroy(FlexFieldsMixin, SwaggerExpandMixin, BaseRetrieveUpdateDestroyView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permit_list_expands = ['category', 'creator_user']


class UploadCategoryThumbnailView(generics.CreateAPIView):
    queryset = RoomCategory.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        request_body=CategoryThumbnailUploadSerializer,
        responses={201: openapi.Response(
            'Thumbnail uploaded successfully', CategoryThumbnailUploadSerializer)},
        operation_description="Upload an thumbnail image to Cloudinary",
    )
    def post(self, request, *args, **kwargs):
        category = get_object_or_404(RoomCategory, id=kwargs['pk'])
        file = request.FILES.get('thumbnail')

        if not file:
            return Response({'detail': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        if not imghdr.what(file):
            return Response({'detail': 'Invalid image format'}, status=status.HTTP_400_BAD_REQUEST)

        upload_result = cloudinary.uploader.upload(
            file,
            folder="ztudy/category_thumbnails/",
            public_id=f"category_{category.id}_thumbnail",
            overwrite=True
        )

        category.thumbnail = upload_result['secure_url']
        category.save()

        return Response({'thumbnail': category.thumbnail}, status=status.HTTP_201_CREATED)


class UploadThumbnailView(generics.CreateAPIView):
    queryset = Room.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        request_body=ThumbnailUploadSerializer,
        responses={201: openapi.Response(
            'Thumbnail uploaded successfully', ThumbnailUploadSerializer)},
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
    filterset_fields = ['room']
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
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, code_invite):
        room = get_object_or_404(Room, code_invite=code_invite)
        user = request.user

        room_data = RoomJoinSerializer(room).data
        participant, created = RoomParticipant.objects.get_or_create(
            room=room, user=user)

        if room.type == "PRIVATE" and not participant.is_approved:
            participant.is_out = True
            participant.save()
            participant_data = RoomParticipantSerializer(participant).data

            # Get all pending requests with participant data
            pending_requests = list(
                RoomParticipant.objects.filter(room=room, is_approved=False)
                .select_related('user')
            )
            request_list = [{
                'user': UserSerializer(req.user).data,
                'is_admin': req.is_admin,
                'is_approved': req.is_approved,
                'is_out': req.is_out
            } for req in pending_requests]

            # Get all admin participants
            admin_participants = list(
                RoomParticipant.objects.filter(room=room, is_admin=True).select_related('user')
            )

            channel_layer = get_channel_layer()
            for admin in admin_participants:
                admin_user_group = f'user_{admin.user.id}'
                async_to_sync(channel_layer.group_send)(
                    admin_user_group,
                    {
                        'type': 'update_pending_requests',
                        'requests': request_list
                    }
                )

            return Response(
                {'message': 'Waiting for admin approval',
                 'room': room_data,
                 'participant': participant_data},
                status=status.HTTP_202_ACCEPTED)

        # If already approved, allow joining
        if participant.is_approved:
            participant.save()
            participant_data = RoomParticipantSerializer(participant).data
            channel_layer = get_channel_layer()
            user_data = UserSerializer(user).data
            async_to_sync(channel_layer.group_send)(
                f'chat_{room.id}',
                {'type': 'user_joined', 'user': user_data}
            )

            return Response({'message': 'Joined room successfully!',
                             'room': room_data,
                             'participant': participant_data}, status=status.HTTP_200_OK)

        # If public room, auto-approve
        if room.type == "PUBLIC":
            participant.is_approved = True
            participant.save()
            participant_data = RoomParticipantSerializer(participant).data
            channel_layer = get_channel_layer()
            user_data = UserSerializer(user).data
            async_to_sync(channel_layer.group_send)(
                f'chat_{room.id}',
                {'type': 'user_joined', 'user': user_data}
            )

            return Response(
                {'message': 'Joined room successfully!',
                 'room': room_data,
                 'participant': participant_data},
                status=status.HTTP_200_OK)

        return Response({'message': 'You are still waiting for approval'}, status=status.HTTP_202_ACCEPTED)


class LeaveRoomAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, code_invite):
        room = get_object_or_404(Room, code_invite=code_invite)
        user = request.user

        participant = get_object_or_404(RoomParticipant, room=room, user=user)
        participant.is_out = True
        participant.save()

        channel_layer = get_channel_layer()
        user = UserSerializer(user).data
        async_to_sync(channel_layer.group_send)(
            f'chat_{room.id}',
            {'type': 'user_left', 'user': user}
        )

        return Response({'message': 'Left room successfully!'}, status=status.HTTP_200_OK)


class ApproveJoinRequestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, code_invite, user_id):
        room = get_object_or_404(Room, code_invite=code_invite)

        user_request = request.user
        participant_user = RoomParticipant.objects.get(user=user_request, room=room)
        if participant_user is None or not participant_user.is_admin:
            return Response({'detail': 'You are not authorized to approve requests!'}, status=status.HTTP_403_FORBIDDEN)

        participant = get_object_or_404(
            RoomParticipant, room=room, user_id=user_id)

        if participant.is_approved:
            return Response({'detail': 'User has already been approved!'}, status=status.HTTP_400_BAD_REQUEST)

        participant.is_approved = True
        participant.is_out = False
        participant.save()

        channel_layer = get_channel_layer()

        # Send notification to the approved user
        user_data = UserSerializer(participant.user).data
        async_to_sync(channel_layer.group_send)(
            f'user_{participant.user.id}',
            {
                'type': 'user_approved',
                'user': user_data,
                'room_id': room.id,
                'code_invite': code_invite
            }
        )

        # Update pending requests list with participant data
        pending_requests = list(
            RoomParticipant.objects.filter(room=room, is_approved=False)
            .select_related('user')
        )
        request_list = [{
            'user': UserSerializer(req.user).data,
            'is_admin': req.is_admin,
            'is_approved': req.is_approved,
            'is_out': req.is_out
        } for req in pending_requests]

        # Get all admin participants
        admin_participants = list(
            RoomParticipant.objects.filter(room=room, is_admin=True).select_related('user')
        )

        for admin in admin_participants:
            admin_user_group = f'user_{admin.user.id}'
            async_to_sync(channel_layer.group_send)(
                admin_user_group,
                {
                    'type': 'update_pending_requests',
                    'requests': request_list
                }
            )

        return Response({'message': 'User has been approved successfully!'}, status=status.HTTP_200_OK)


class RejectJoinRequestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, code_invite, user_id):
        room = get_object_or_404(Room, code_invite=code_invite)

        user_request = request.user
        participant_user = RoomParticipant.objects.get(user=user_request, room=room)
        if participant_user is None or not participant_user.is_admin:
            return Response({'detail': 'You are not authorized to approve requests!'}, status=status.HTTP_403_FORBIDDEN)

        participant = get_object_or_404(
            RoomParticipant, room=room, user_id=user_id)

        if participant.is_approved:
            return Response({'detail': 'User has already been approved!'}, status=status.HTTP_400_BAD_REQUEST)

        # Store user data before deleting participant
        user_data = UserSerializer(participant.user).data
        participant.delete()

        channel_layer = get_channel_layer()

        # Send notification to the rejected user
        async_to_sync(channel_layer.group_send)(
            f'user_{user_id}',
            {
                'type': 'user_rejected',
                'user': user_data,
                'room_id': room.id,
                'code_invite': code_invite
            }
        )

        # Update pending requests list with participant data
        pending_requests = list(
            RoomParticipant.objects.filter(room=room, is_approved=False)
            .select_related('user')
        )
        request_list = [{
            'user': UserSerializer(req.user).data,
            'is_admin': req.is_admin,
            'is_approved': req.is_approved,
            'is_out': req.is_out
        } for req in pending_requests]

        # Get all admin participants
        admin_participants = list(
            RoomParticipant.objects.filter(room=room, is_admin=True).select_related('user')
        )

        for admin in admin_participants:
            admin_user_group = f'user_{admin.user.id}'
            async_to_sync(channel_layer.group_send)(
                admin_user_group,
                {
                    'type': 'update_pending_requests',
                    'requests': request_list
                }
            )

        return Response({'message': 'User has been rejected successfully!'}, status=status.HTTP_200_OK)


class AssignRoomAdminAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, code_invite, user_id):
        room = get_object_or_404(Room, code_invite=code_invite)

        user_request = request.user
        participant_user = RoomParticipant.objects.get(user=user_request, room=room)
        if participant_user is None or not participant_user.is_admin:
            return Response({'detail': 'You are not authorized to approve requests!'}, status=status.HTTP_403_FORBIDDEN)

        participant = get_object_or_404(
            RoomParticipant, room=room, user_id=user_id)

        participant.is_admin = True
        participant.save()

        channel_layer = get_channel_layer()

        user_data = UserSerializer(participant.user).data
        # Send to user-specific group
        async_to_sync(channel_layer.group_send)(
            f'user_{participant.user.id}',
            {
                'type': 'user_assigned_admin',
                'user': user_data,
                'room_id': room.id,
                'code_invite': code_invite
            }
        )

        return Response({'message': 'User has been assigned as admin successfully!'}, status=status.HTTP_200_OK)
