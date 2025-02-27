from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from .models import BackgroundVideoType, BackgroundVideo, SessionGoal, User, MotivationalQuote, Sound


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