from rest_flex_fields.views import FlexFieldsMixin
from core.models import BackgroundVideo, BackgroundVideoType
from api.serializers import BackgroundVideoSerializer, BackgroundVideoTypeSerializer, BackgroundVideoUploadSerializer
from .base_views import BaseListCreateView, BaseRetrieveUpdateDestroyView, SwaggerExpandMixin
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status, generics
import cloudinary.uploader
import imghdr
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404


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
        responses={201: openapi.Response('Image uploaded successfully', BackgroundVideoUploadSerializer)},
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
