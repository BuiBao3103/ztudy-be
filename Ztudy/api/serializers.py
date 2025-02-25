from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from .models import BackgroundVideoType, BackgroundVideo, SessionGoal, User, MotivationalQuote

class BackgroundVideoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackgroundVideoType
        fields = '__all__'
        read_only_fields = ['deleted_at', 'restored_at', 'transaction_id']


class BackgroundVideoSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = BackgroundVideo
        fields = '__all__'
        expandable_fields = {
            'type': BackgroundVideoTypeSerializer
        }



class SessionGoalSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Display the related User's string representation

    class Meta:
        model = SessionGoal
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    goals = SessionGoalSerializer(many=True, read_only=True)  # Nested serializer for user's goals

    class Meta:
        model = User
        fields = '__all__'


class MotivationalQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotivationalQuote
        fields = '__all__'
