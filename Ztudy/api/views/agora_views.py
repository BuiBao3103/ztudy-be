import logging
import random
import time

from agora_token_builder import RtcTokenBuilder
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
logger = logging.getLogger(__name__)


# Create your views here.
class AgoraTokenView(APIView):
    """
    View to generate Agora token for a given channel.
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'channel',
                openapi.IN_QUERY,
                description="identifier of the channel(code-invite)",
                type=openapi.TYPE_STRING
            )
        ]
    )

    def get(self, request, *args, **kwargs):
        try:
            # Log request details
            logger.info(f"Token request received - Method: {request.method}, Path: {request.path}")
            logger.info(f"Headers: {dict(request.headers)}")

            # Validate Agora credentials
            app_id = settings.AGORA_APP_ID
            app_certificate = settings.AGORA_APP_CERTIFICATE

            if not app_id or not app_certificate:
                logger.error("Agora credentials not configured")
                return JsonResponse({
                    'error': 'Agora credentials not properly configured'
                }, status=500)

            # Get and validate channel name
            channel_name = request.GET.get('channel')
            if not channel_name:
                return JsonResponse({
                    'error': 'Channel name is required'
                }, status=400)

            logger.info(f"Generating token for channel: {channel_name}")

            # Generate a random uid between 1 and 230
            uid = random.randint(1, 230)

            # Set role as publisher
            role = 1  # RtcRole.PUBLISHER

            # Set expiry time as 24 hours from now
            expiration_time_in_seconds = 3600 * 24
            current_timestamp = int(time.time())
            privilegeExpiredTs = current_timestamp + expiration_time_in_seconds

            # Generate token
            token = RtcTokenBuilder.buildTokenWithUid(
                app_id, app_certificate,
                channel_name, uid, role, privilegeExpiredTs
            )

            logger.info(f"Token generated successfully for channel: {channel_name}, uid: {uid}")

            return JsonResponse({
                'token': token,
                'uid': uid,
                'app_id': app_id,
                'channel': channel_name,
                'expires_in': expiration_time_in_seconds
            })

        except Exception as e:
            logger.error(f"Error generating token: {str(e)}", exc_info=True)
            return JsonResponse({
                'error': f'Failed to generate token: {str(e)}'
            }, status=500)
