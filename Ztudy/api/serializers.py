from datetime import datetime, timedelta

from allauth.account.models import EmailAddress
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import PasswordResetSerializer
from dj_rest_auth.serializers import UserDetailsSerializer, PasswordResetConfirmSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from .models import (BackgroundVideoType, BackgroundVideo,
                     SessionGoal, User, MotivationalQuote, Sound, RoomCategory,
                     Room, RoomParticipant, Interest, StudySession)
from .utils import generate_unique_code, encode_emoji, decode_emoji

User = get_user_model()


class BackgroundVideoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackgroundVideoType
        exclude = ['deleted_at', 'restored_at', 'transaction_id']

    def create(self, validated_data):
        if 'name' in validated_data:
            validated_data['name'] = encode_emoji(validated_data['name'])
        if 'description' in validated_data:
            validated_data['description'] = encode_emoji(
                validated_data['description'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            validated_data['name'] = encode_emoji(validated_data['name'])
        if 'description' in validated_data:
            validated_data['description'] = encode_emoji(
                validated_data['description'])
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
            validated_data['code_invite'] = generate_unique_code(
                Room, 'code_invite', 6)

        room = super().create(validated_data)

        if room.creator_user:
            RoomParticipant.objects.create(room=room, user=room.creator_user, is_admin=True, is_approved=True,
                                           is_out=True)

        return room

    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ['is_active', 'code_invite']
        expandable_fields = {
            'category': RoomCategorySerializer,
            'creator_user': UserSerializer
        }


class RoomJoinSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(required=False, allow_null=True)
    category = RoomCategorySerializer(read_only=True)

    class Meta:
        model = Room
        fields = '__all__'


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


class StudySessionSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = StudySession
        fields = "__all__"


class CustomUserDetailsSerializer(UserDetailsSerializer):
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        exclude = ['password', 'deleted_at', 'restored_at', 'transaction_id', 'is_superuser', 'is_staff', 'groups',
                   'user_permissions']


class LeaderboardUserSerializer(serializers.ModelSerializer):
    total_time = serializers.FloatField()
    rank = serializers.IntegerField()

    class Meta:
        model = User  # Assuming User is your user model
        # Add other fields you want to include
        fields = ['id', 'username', 'rank', 'total_time', 'avatar']


class CustomPasswordResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        user = context.get('user')
        if user:
            context['uid'] = urlsafe_base64_encode(force_bytes(user.pk))

        context['frontend_url'] = settings.FRONTEND_URL
        context['site_name'] = 'Ztudy'
        super().send_mail(
            subject_template_name,
            email_template_name,
            context,
            from_email,
            to_email,
            html_email_template_name
        )


class CustomPasswordResetSerializer(PasswordResetSerializer):
    password_reset_form_class = CustomPasswordResetForm

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise ValidationError("User with this email does not exist")

        cache_key = f"password_reset_{value}"
        last_attempt = cache.get(cache_key)

        if last_attempt:
            time_diff = datetime.now() - last_attempt
            if time_diff < timedelta(minutes=3):
                remaining_seconds = int((timedelta(minutes=3) - time_diff).total_seconds())
                remaining_minutes = remaining_seconds // 60
                remaining_secs = remaining_seconds % 60

                if remaining_minutes > 0:
                    message = f"Please wait {remaining_minutes} minute(s) and {remaining_secs} second(s)"
                else:
                    message = f"Please wait {remaining_seconds} second(s)"

                raise ValidationError(message)

        cache.set(cache_key, datetime.now(), timeout=180)

        return value

    def get_email_options(self):
        return {
            'subject_template_name': 'registration/custom_password_reset_subject.txt',
            'email_template_name': 'registration/custom_password_reset_email.html',
            'html_email_template_name': 'registration/custom_password_reset_email.html',
            'extra_email_context': {
                'frontend_url': settings.FRONTEND_URL,
                'site_name': 'Ztudy',
            }
        }

    def save(self):
        opts = self.get_email_options()
        form = self.password_reset_form_class(data=self.validated_data)

        if form.is_valid():
            opts['request'] = self.context.get('request')
            form.save(**opts)


class CustomPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    def validate(self, attrs):
        try:
            # Decode the uid and validate user
            uid = force_str(urlsafe_base64_decode(attrs['uid']))
            self.user = User.objects.get(pk=uid)

            # Validate token
            if not default_token_generator.check_token(self.user, attrs['token']):
                raise ValidationError({'token': ['Invalid or expired token']})

            # Validate passwords
            if attrs['new_password1'] != attrs['new_password2']:
                raise ValidationError(
                    {'new_password2': ["The two password fields didn't match."]})

            return attrs
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

    def save(self):
        if not self.user:
            raise ValidationError(
                {'error': 'No user found for password reset'})

        # Set the new password
        self.user.set_password(self.validated_data['new_password1'])
        self.user.save()

        return self.user
