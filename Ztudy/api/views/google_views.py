import logging

import jwt
import requests
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.jwt_auth import set_jwt_cookies
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.utils import jwt_encode
from dj_rest_auth.views import LoginView
from django.conf import settings
from django.contrib.auth import get_user_model, login as django_login
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from dj_rest_auth.app_settings import api_settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime

logger = logging.getLogger(__name__)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL


class GoogleLoginCallback(APIView):
    def get(self, request, *args, **kwargs):
        try:
            code = request.GET.get('code')
            if not code:
                logger.error("No code received in Google callback")
                return redirect(f"{settings.FRONTEND_URL}?error=no_code")

            # Exchange code for tokens
            token_response = self.get_google_token(code)
            if not token_response:
                logger.error("Failed to get Google token")
                return redirect(f"{settings.FRONTEND_URL}?error=token_error")

            # Get user info from Google
            user_info = self.get_google_user_info(
                token_response.get('access_token'))
            if not user_info:
                logger.error("Failed to get Google user info")
                return redirect(f"{settings.FRONTEND_URL}?error=user_info_error")

            # Create or update user
            User = get_user_model()
            email = user_info['email']

            try:
                # Try to get existing user by email
                user = User.objects.get(email=email)
                logger.info(f"Existing user found: {email}")
            except User.DoesNotExist:
                # Create new user if doesn't exist
                user = User.objects.create(
                    email=email,
                    username=user_info.get('name', '').lower(),
                    avatar="https://res.cloudinary.com/dloeqfbwm/image/upload/v1742014468/ztudy/avatars/default_avatar.jpg"
                )
                logger.info(f"Created new user: {email}")

                # Create EmailAddress record
                from allauth.account.models import EmailAddress
                EmailAddress.objects.create(
                    user=user,
                    email=email,
                    primary=True,
                    verified=True  # Google accounts are pre-verified
                )
            else:
                # Ensure EmailAddress exists for existing user
                from allauth.account.models import EmailAddress
                EmailAddress.objects.get_or_create(
                    user=user,
                    email=email,
                    defaults={
                        'primary': True,
                        'verified': True
                    }
                )

            # Process login with specific backend
            if api_settings.SESSION_LOGIN:
                from allauth.account.auth_backends import AuthenticationBackend
                django_login(
                    request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
                logger.info(f"User logged in via session: {email}")

            # Generate JWT tokens
            access_token, refresh_token = jwt_encode(user)
            logger.info(f"Generated JWT tokens for user: {email}")

            # Create redirect response
            redirect_response = redirect(
                settings.FRONTEND_URL+"/google-callback")

            # Log cookie settings before setting
            logger.info(f"Cookie settings - Domain: {settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN']}, "
                        f"Secure: {settings.SIMPLE_JWT['AUTH_COOKIE_SECURE']}, "
                        f"SameSite: {settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']}, "
                        f"Path: {settings.SIMPLE_JWT['AUTH_COOKIE_PATH']}")

            # Use dj-rest-auth's set_jwt_cookies function to set cookies properly
            set_jwt_cookies(redirect_response, access_token, refresh_token)

            # Log the response headers for debugging
            logger.info(f"Response headers: {redirect_response.headers}")

            return redirect_response

        except Exception as e:
            logger.exception("Error in Google callback")
            return redirect(f"{settings.FRONTEND_URL}?error=login_failed")

    def get_google_token(self, code):
        try:
            token_url = "https://oauth2.googleapis.com/token"
            data = {
                'code': code,
                'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
                'client_secret': settings.GOOGLE_OAUTH_CLIENT_SECRET,
                'redirect_uri': settings.GOOGLE_OAUTH_CALLBACK_URL,
                'grant_type': 'authorization_code'
            }
            logger.info(
                f"Requesting Google token with redirect_uri: {settings.GOOGLE_OAUTH_CALLBACK_URL}")
            response = requests.post(token_url, data=data)
            if response.status_code != 200:
                logger.error(f"Google token error: {response.text}")
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            logger.exception("Error getting Google token")
            return None

    def get_google_user_info(self, access_token):
        try:
            user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(user_info_url, headers=headers)
            if response.status_code != 200:
                logger.error(f"Google user info error: {response.text}")
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            logger.exception("Error getting Google user info")
            return None


class LoginPage(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "pages/login.html",
            {
                "google_callback_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
                "google_client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            },
        )
