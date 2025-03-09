from allauth.account.models import EmailAddress
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from .models import BackgroundVideoType, BackgroundVideo, SessionGoal, User, MotivationalQuote, Sound, RoomCategory, \
    Room, RoomParticipant, Interest
from django.core.exceptions import ValidationError
from .utils import generate_unique_code, encode_emoji, decode_emoji


class BackgroundVideoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackgroundVideoType
        exclude = ['deleted_at', 'restored_at', 'transaction_id']

    def create(self, validated_data):
        if 'name' in validated_data:
            validated_data['name'] = encode_emoji(validated_data['name'])
        if 'description' in validated_data:
            validated_data['description'] = encode_emoji(validated_data['description'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            validated_data['name'] = encode_emoji(validated_data['name'])
        if 'description' in validated_data:
            validated_data['description'] = encode_emoji(validated_data['description'])
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'name' in data:
            data['name'] = decode_emoji(data['name'])
        if 'description' in data:
            data['description'] = decode_emoji(data['description'])
        return data


class BackgroundVideoSerializer(FlexFieldsModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = BackgroundVideo
        fields = '__all__'
        expandable_fields = {
            'type': BackgroundVideoTypeSerializer
        }


class BackgroundVideoUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        exclude = ['password', 'deleted_at', 'restored_at', 'transaction_id', 'is_superuser', 'is_staff', 'groups',
                   'user_permissions']


class AvatarUploadSerializer(serializers.Serializer):
    avatar = serializers.ImageField()


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

    def create(self, validated_data):
        if 'name' in validated_data:
            validated_data['name'] = encode_emoji(validated_data['name'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            validated_data['name'] = encode_emoji(validated_data['name'])
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'name' in data:
            data['name'] = decode_emoji(data['name'])
        return data


class RoomCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomCategory
        fields = '__all__'

    def create(self, validated_data):
        if 'name' in validated_data:
            validated_data['name'] = encode_emoji(validated_data['name'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            validated_data['name'] = encode_emoji(validated_data['name'])
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'name' in data:
            data['name'] = decode_emoji(data['name'])
        return data


class RoomSerializer(FlexFieldsModelSerializer):
    thumbnail = serializers.ImageField(required=False, allow_null=True)

    def create(self, validated_data):
        if 'code_invite' not in validated_data or not validated_data['code_invite']:
            validated_data['code_invite'] = generate_unique_code(Room, 'code_invite', 6)

        room = super().create(validated_data)

        if room.creator_user:
            RoomParticipant.objects.create(room=room, user=room.creator_user, is_admin=True)

        return room

    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ['is_active', 'code_invite']
        expandable_fields = {
            'category': RoomCategorySerializer,
            'creator_user': UserSerializer
        }


class ThumbnailUploadSerializer(serializers.Serializer):
    thumbnail = serializers.ImageField()


class RoomParticipantSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = RoomParticipant
        fields = '__all__'
        expandable_fields = {
            'room': RoomSerializer,
            'user': UserSerializer
        }


class InterestSerializer(serializers.ModelSerializer):
    category = RoomCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=RoomCategory.objects.all(), write_only=True, source='category'
    )

    class Meta:
        model = Interest
        fields = ['id', 'user', 'category', 'category_id', 'created_at']
        read_only_fields = ['user']


class AddUserInterestSerializer(serializers.Serializer):
    category_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        help_text="List of category IDs to add as interests"
    )


class CustomRegisterSerializer(RegisterSerializer):
    def validate_email(self, value):
        if EmailAddress.objects.filter(email=value).exists():
            raise ValidationError("Email already exists")
        return value
