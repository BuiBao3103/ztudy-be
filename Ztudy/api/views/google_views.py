from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import logging
from django.shortcuts import redirect
from django.views import View
from django.shortcuts import render
from django.http import HttpRequest
from rest_framework.request import Request
from django.middleware.csrf import get_token
import jwt
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from api.serializers import CustomUserDetailsSerializer

logger = logging.getLogger(__name__)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL


class GoogleLoginCallback(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # 1. Lấy token từ Google
            code = request.GET.get("code")
            token_response = self.get_google_token(code)
            
            # 2. Lấy email từ id_token
            id_token = token_response.get('id_token')
            user_info = jwt.decode(id_token, options={"verify_signature": False})
            email = user_info['email']
            
            # 3. Lấy hoặc tạo user
            User = get_user_model()
            user, _ = User.objects.get_or_create(
                email=email,
                defaults={'username': email}
            )

            # 4. Tạo JWT token
            refresh = RefreshToken.for_user(user)
            
            # 5. Tạo response với redirect
            response = redirect(settings.FRONTEND_URL)

            # 6. Set cookies theo cấu hình
            response.set_cookie(
                settings.REST_AUTH['JWT_AUTH_COOKIE'],  # 'access_token'
                str(refresh.access_token),
                httponly=settings.REST_AUTH['JWT_AUTH_HTTPONLY'],  # True
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],  # 'Lax'
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],  # False
                path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],  # '/'
                domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN']  # None
            )
            
            response.set_cookie(
                settings.REST_AUTH['JWT_AUTH_REFRESH_COOKIE'],  # 'refresh_token'
                str(refresh),
                httponly=settings.REST_AUTH['JWT_AUTH_HTTPONLY'],  # True
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],  # 'Lax'
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],  # False
                path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],  # '/'
                domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN']  # None
            )

            return response

        except Exception as e:
            logger.exception("Error during Google callback")
            return redirect(f"{settings.FRONTEND_URL}?error=login_failed")

    def get_google_token(self, code):
        token_url = "https://oauth2.googleapis.com/token"
        token_payload = {
            "code": code,
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
            "grant_type": "authorization_code"
        }
        
        token_response = requests.post(token_url, data=token_payload)
        
        if token_response.status_code != 200:
            raise Exception(f"Failed to get token: {token_response.text}")
            
        return token_response.json()


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
