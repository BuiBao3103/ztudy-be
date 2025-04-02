from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..models import Room, RoomParticipant, Role, RoomType
from ..serializers import UserSerializer, RoomJoinSerializer, RoomParticipantSerializer
from ..utils.websocket import send_to_user_group, send_to_chat_group, get_pending_requests_data


class BaseParticipationView(APIView):
    permission_classes = [IsAuthenticated]


class JoinRoomAPIView(BaseParticipationView):
    def post(self, request, code_invite):
        room = get_object_or_404(Room, code_invite=code_invite)

        # Check if room is active
        if not room.is_active:
            return Response(
                {"detail": "This room has been ended!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        room_data = RoomJoinSerializer(room).data
        participant, created = RoomParticipant.objects.get_or_create(
            room=room, user=user
        )

        if room.type == "PRIVATE" and not participant.is_approved:
            participant.is_out = True
            participant.save()
            participant_data = RoomParticipantSerializer(participant).data

            # Get pending requests data
            request_list = get_pending_requests_data(room)
            admin_participants = RoomParticipant.objects.filter(
                room=room,
                role__in=[Role.ADMIN, Role.MODERATOR]
            ).select_related("user")

            # Notify admins about new request
            for admin in admin_participants:
                send_to_user_group(
                    admin.user.id,
                    "update_pending_requests",
                    {"requests": request_list}
                )

            return Response(
                {
                    "message": "Waiting for admin approval",
                    "room": room_data,
                    "participant": participant_data,
                },
                status=status.HTTP_202_ACCEPTED,
            )

        # If already approved or public room, allow joining
        if (room.type == "PRIVATE" and participant.is_approved) or room.type == "PUBLIC":
            participant.is_approved = True
            participant.save()
            participant_data = RoomParticipantSerializer(participant).data
            
            # Notify room about new participant
            user_data = UserSerializer(user).data
            send_to_chat_group(
                room.id,
                "user_joined",
                {"user": user_data}
            )

            return Response(
                {
                    "message": "Joined room successfully!",
                    "room": room_data,
                    "participant": participant_data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"message": "You are still waiting for approval"},
            status=status.HTTP_202_ACCEPTED,
        )


class JoinRandomRoomAPIView(BaseParticipationView):
    def post(self, request):
        user = request.user
        room = Room.objects.filter(is_active=True, type=RoomType.PUBLIC).order_by("?").first()
        
        if room is None:
            return Response(
                {"detail": "No active rooms available!"},
                status=status.HTTP_404_NOT_FOUND
            )

        room_data = RoomJoinSerializer(room).data
        participant, created = RoomParticipant.objects.get_or_create(
            room=room, user=user, is_approved=True
        )

        participant.save()
        participant_data = RoomParticipantSerializer(participant).data
        
        # Notify room about new participant
        user_data = UserSerializer(user).data
        send_to_chat_group(
            room.id,
            "user_joined",
            {"user": user_data}
        )

        return Response(
            {
                "message": "Joined room successfully!",
                "room": room_data,
                "participant": participant_data,
            },
            status=status.HTTP_200_OK,
        )


class CancelJoinRoomAPIView(BaseParticipationView):
    def post(self, request, code_invite):
        room = get_object_or_404(Room, code_invite=code_invite)
        user = request.user

        participant = get_object_or_404(RoomParticipant, room=room, user=user)
        participant.delete()

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
            {"message": "Cancelled join request successfully!"},
            status=status.HTTP_200_OK
        )


class LeaveRoomAPIView(BaseParticipationView):
    def post(self, request, code_invite):
        room = get_object_or_404(Room, code_invite=code_invite)
        user = request.user

        participant = get_object_or_404(RoomParticipant, room=room, user=user)
        participant.is_out = True
        participant.save()

        # Notify room about leaving participant
        user_data = UserSerializer(user).data
        send_to_chat_group(
            room.id,
            "user_left",
            {"user": user_data}
        )

        return Response(
            {"message": "Left room successfully!"},
            status=status.HTTP_200_OK
        ) 