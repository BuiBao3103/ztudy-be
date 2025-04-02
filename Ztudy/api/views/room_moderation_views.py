from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..models import Room, RoomParticipant, Role
from ..serializers import UserSerializer, RoomParticipantSerializer
from ..utils.websocket import send_to_user_group, send_to_chat_group, get_pending_requests_data


class BaseModerationView(APIView):
    permission_classes = [IsAuthenticated]

    def get_admin_participant(self, room, user):
        participant = get_object_or_404(RoomParticipant, user=user, room=room)
        if participant.role != Role.ADMIN:
            raise PermissionError("You are not authorized to perform this action!")
        return participant


class ApproveJoinRequestAPIView(BaseModerationView):
    def post(self, request, code_invite, user_id):
        room = get_object_or_404(Room, code_invite=code_invite)
        self.get_admin_participant(room, request.user)

        participant = get_object_or_404(RoomParticipant, room=room, user_id=user_id)
        if participant.is_approved:
            return Response(
                {"detail": "User has already been approved!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        participant.is_approved = True
        participant.is_out = False
        participant.save()

        # Send notification to the approved user
        user_data = UserSerializer(participant.user).data
        send_to_user_group(
            participant.user.id,
            "user_approved",
            {
                "user": user_data,
                "room_id": room.id,
                "code_invite": code_invite,
            }
        )

        # Update pending requests for admins
        request_list = get_pending_requests_data(room)
        admin_participants = RoomParticipant.objects.filter(
            room=room,
            role__in=[Role.ADMIN, Role.MODERATOR]
        ).select_related("user")

        for admin in admin_participants:
            send_to_user_group(
                admin.user.id,
                "update_pending_requests",
                {"requests": request_list}
            )

        return Response(
            {"message": "User has been approved successfully!"},
            status=status.HTTP_200_OK,
        )


class RejectJoinRequestAPIView(BaseModerationView):
    def post(self, request, code_invite, user_id):
        room = get_object_or_404(Room, code_invite=code_invite)
        self.get_admin_participant(room, request.user)

        participant = get_object_or_404(RoomParticipant, room=room, user_id=user_id)
        if participant.is_approved:
            return Response(
                {"detail": "User has already been approved!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Store user data before deleting participant
        user_data = UserSerializer(participant.user).data
        participant.delete()

        # Send notification to the rejected user
        send_to_user_group(
            user_id,
            "user_rejected",
            {
                "user": user_data,
                "room_id": room.id,
                "code_invite": code_invite,
            }
        )

        # Update pending requests for admins
        request_list = get_pending_requests_data(room)
        admin_participants = RoomParticipant.objects.filter(
            room=room,
            role__in=[Role.ADMIN, Role.MODERATOR]
        ).select_related("user")

        for admin in admin_participants:
            send_to_user_group(
                admin.user.id,
                "update_pending_requests",
                {"requests": request_list}
            )

        return Response(
            {"message": "User has been rejected successfully!"},
            status=status.HTTP_200_OK,
        )


class AssignRoomAdminAPIView(BaseModerationView):
    def post(self, request, code_invite, user_id):
        room = get_object_or_404(Room, code_invite=code_invite)
        self.get_admin_participant(room, request.user)

        participant = get_object_or_404(RoomParticipant, room=room, user_id=user_id)
        participant.role = Role.MODERATOR
        participant.save()

        user_data = UserSerializer(participant.user).data
        send_to_user_group(
            participant.user.id,
            "user_assigned_moderator",
            {
                "user": user_data,
                "room_id": room.id,
                "code_invite": code_invite,
            }
        )

        return Response(
            {"message": "User has been assigned as admin successfully!"},
            status=status.HTTP_200_OK,
        )


class RevokeRoomAdminAPIView(BaseModerationView):
    def post(self, request, code_invite, user_id):
        room = get_object_or_404(Room, code_invite=code_invite)
        self.get_admin_participant(room, request.user)

        participant = get_object_or_404(RoomParticipant, room=room, user_id=user_id)
        participant.role = Role.USER
        participant.save()

        user_data = UserSerializer(participant.user).data
        send_to_user_group(
            participant.user.id,
            "user_revoked_moderator",
            {
                "user": user_data,
                "room_id": room.id,
                "code_invite": code_invite,
            }
        )

        return Response(
            {"message": "User has been revoked as admin successfully!"},
            status=status.HTTP_200_OK,
        )


class EndRoomAPIView(BaseModerationView):
    def post(self, request, code_invite):
        room = get_object_or_404(Room, code_invite=code_invite)
        self.get_admin_participant(room, request.user)

        # Update room status
        room.is_active = False
        room.save()

        # Update all participants status
        RoomParticipant.objects.filter(room=room).update(is_out=True)

        # Notify all users in the room
        send_to_chat_group(
            room.id,
            "room_ended",
            {
                "room_id": room.id,
                "code_invite": code_invite
            }
        )

        return Response(
            {"message": "Room has been ended successfully!"},
            status=status.HTTP_200_OK
        ) 