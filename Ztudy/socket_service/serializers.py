from rest_framework import serializers
from core.models import User, Room, RoomParticipant


class WebSocketMessageSerializer(serializers.Serializer):
    type = serializers.CharField()
    message = serializers.CharField(required=False)
    is_typing = serializers.BooleanField(required=False)
    user = serializers.JSONField(required=False)
    room_id = serializers.IntegerField(required=False)
    code_invite = serializers.CharField(required=False)
    is_online = serializers.BooleanField(required=False)
    online_count = serializers.IntegerField(required=False)
    level = serializers.CharField(required=False)
    monthly_study_time = serializers.FloatField(required=False)


class RoomParticipantSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = RoomParticipant
        fields = ["id", "user", "role", "is_approved", "is_out"]

    def get_user(self, obj):
        from api.serializers import UserSerializer

        return UserSerializer(obj.user).data


class RoomSerializer(serializers.ModelSerializer):
    participants = RoomParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ["id", "name", "code_invite", "type", "participants"]
