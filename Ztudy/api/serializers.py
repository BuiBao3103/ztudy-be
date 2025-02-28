from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from .models import BackgroundVideoType, BackgroundVideo, SessionGoal, User, MotivationalQuote, Sound, RoomCategory, Room, RoomParticipant


class BackgroundVideoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackgroundVideoType
        # fields = '__all__'
        exclude = ['deleted_at', 'restored_at', 'transaction_id']

class BackgroundVideoSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = BackgroundVideo
        fields = '__all__'
        expandable_fields = {
            'type': BackgroundVideoTypeSerializer
        }

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['password', 'deleted_at', 'restored_at', 'transaction_id', 'is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions']

class SessionGoalSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = SessionGoal
        fields = '__all__'
        expandable_fields = {
            'user': UserSerializer
        }

class MotivationalQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotivationalQuote
        fields = '__all__'

class SoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sound
        fields = '__all__'

class RoomCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomCategory
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    # Sử dụng RoomCategorySerializer để nhúng thể loại phòng
    category = RoomCategorySerializer(read_only=True)
    creator_user = UserSerializer(read_only=True)

    class Meta:
        model = Room
        fields = '__all__'
        expandable_fields = {
            'category': RoomCategorySerializer,
            'creator_user': UserSerializer
        }

class RoomParticipantSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = RoomParticipant
        fields = '__all__'
        expandable_fields = {
            'room': RoomSerializer,
            'user': UserSerializer
        }