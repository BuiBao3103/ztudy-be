from rest_flex_fields.views import FlexFieldsMixin
from core.models import BackgroundVideo, BackgroundVideoType, UserFavoriteVideo
from api.serializers import BackgroundVideoSerializer, BackgroundVideoTypeSerializer, BackgroundVideoUploadSerializer, UserFavoriteVideoSerializer, UserFavoriteVideoUploadSerializer
from .base_views import BaseListCreateView, BaseRetrieveUpdateDestroyView, SwaggerExpandMixin
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status, generics
import cloudinary.uploader
import imghdr
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
import re
import urllib.request
import urllib.parse
import json


class BackgroundVideoListCreate(FlexFieldsMixin, SwaggerExpandMixin, BaseListCreateView):
    queryset = BackgroundVideo.objects.all()
    serializer_class = BackgroundVideoSerializer
    filterset_fields = ['type']
    permit_list_expands = ['type']


class BackgroundVideoRetrieveUpdateDestroy(FlexFieldsMixin, SwaggerExpandMixin, BaseRetrieveUpdateDestroyView):
    queryset = BackgroundVideo.objects.all()
    serializer_class = BackgroundVideoSerializer
    permit_list_expands = ['type']


class UploadBackgroundVideoView(generics.CreateAPIView):
    queryset = BackgroundVideo.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        request_body=BackgroundVideoUploadSerializer,
        responses={201: openapi.Response(
            'Image uploaded successfully', BackgroundVideoUploadSerializer)},
        operation_description="Upload an image to Cloudinary",
    )
    def post(self, request, *args, **kwargs):
        background_video = get_object_or_404(BackgroundVideo, id=kwargs['pk'])
        file = request.FILES.get('image')

        if not file:
            return Response({'detail': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        if not imghdr.what(file):
            return Response({'detail': 'Invalid image format'}, status=status.HTTP_400_BAD_REQUEST)

        upload_result = cloudinary.uploader.upload(
            file,
            folder="ztudy/background-video-images/",
            public_id=f"background-video_{background_video.id}_image",
            overwrite=True
        )

        background_video.image = upload_result['secure_url']
        background_video.save()

        return Response({'thumbnail': background_video.image}, status=status.HTTP_201_CREATED)


class BackgroundVideoTypeListCreate(BaseListCreateView):
    queryset = BackgroundVideoType.objects.all()
    serializer_class = BackgroundVideoTypeSerializer


class BackgroundVideoTypeRetrieveUpdateDestroy(BaseRetrieveUpdateDestroyView):
    queryset = BackgroundVideoType.objects.all()
    serializer_class = BackgroundVideoTypeSerializer


class UserFavoriteVideoListCreate(FlexFieldsMixin, SwaggerExpandMixin, BaseListCreateView):
    queryset = UserFavoriteVideo.objects.all()
    serializer_class = UserFavoriteVideoSerializer
    filterset_fields = ['user']
    permit_list_expands = ['user']

    def perform_create(self, serializer):
        youtube_url = self.request.data.get('youtube_url', '').strip()
        name = self.request.data.get('name', '').strip()

        video_id = self.extract_video_id(youtube_url)
        author_name = ""
        author_url = ""
        image = ""

        if video_id:
            metadata = self.get_youtube_metadata(video_id)
            name = name or metadata["title"] or f"Video_{video_id}"
            author_name = metadata["author_name"]
            author_url = metadata["author_url"]
            image = metadata["thumbnail_url"]

        serializer.save(
            name=name,
            author_name=author_name,
            author_url=author_url,
            image = image
    )

    def extract_video_id(self, url):
        match = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", url)
        return match.group(1) if match else ""

    def get_youtube_metadata(self, video_id):
        oembed_url = "https://www.youtube.com/oembed"
        params = {
            "format": "json",
            "url": f"https://www.youtube.com/watch?v={video_id}"
        }
        query_string = urllib.parse.urlencode(params)
        full_url = f"{oembed_url}?{query_string}"

        try:
            with urllib.request.urlopen(full_url) as response:
                data = json.loads(response.read().decode())
                return {
                    "title": data.get("title", ""),
                    "author_name": data.get("author_name", ""),
                    "author_url": data.get("author_url", ""),
                    "thumbnail_url": data.get("thumbnail_url",""),
                }
        except Exception as e:
            print("Error fetching YouTube metadata:", e)
            return {
                "title": "",
                "author_name": "",
                "author_url": "",
                "thumbnail_url": ""
            }


class UserFavoriteVideoRetrieveUpdateDestroy(FlexFieldsMixin, SwaggerExpandMixin, BaseRetrieveUpdateDestroyView):
    queryset = UserFavoriteVideo.objects.all()
    serializer_class = UserFavoriteVideoSerializer
    permit_list_expands = ['user']


class UploadUserFavoriteVideoView(generics.CreateAPIView):
    queryset = UserFavoriteVideo.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        request_body=UserFavoriteVideoUploadSerializer,
        responses={201: openapi.Response(
            'Image uploaded successfully', UserFavoriteVideoUploadSerializer)},
        operation_description="Upload an image to Cloudinary",
    )
    def post(self, request, *args, **kwargs):
        user_favorite_video = get_object_or_404(
            UserFavoriteVideo, id=kwargs['pk'])
        file = request.FILES.get('image')

        if not file:
            return Response({'detail': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        if not imghdr.what(file):
            return Response({'detail': 'Invalid image format'}, status=status.HTTP_400_BAD_REQUEST)

        upload_result = cloudinary.uploader.upload(
            file,
            folder="ztudy/user-favorite-video-images/",
            public_id=f"user-favorite-video_{user_favorite_video.id}_image",
            overwrite=True
        )

        user_favorite_video.image = upload_result['secure_url']
        user_favorite_video.save()

        return Response({'thumbnail': user_favorite_video.image}, status=status.HTTP_201_CREATED)
