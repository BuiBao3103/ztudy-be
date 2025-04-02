import imghdr
import cloudinary.uploader
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Room, RoomCategory
from ..serializers import ThumbnailUploadSerializer, CategoryThumbnailUploadSerializer


class BaseThumbnailUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def validate_image(self, file):
        if not file:
            return False, "No file uploaded"
        if not imghdr.what(file):
            return False, "Invalid image format"
        return True, None


class UploadRoomThumbnailView(BaseThumbnailUploadView):
    @swagger_auto_schema(
        request_body=ThumbnailUploadSerializer,
        responses={
            201: openapi.Response(
                "Thumbnail uploaded successfully", ThumbnailUploadSerializer
            )
        },
        operation_description="Upload an thumbnail image to Cloudinary",
    )
    def post(self, request, *args, **kwargs):
        room = get_object_or_404(Room, id=kwargs["pk"])
        file = request.FILES.get("thumbnail")

        is_valid, error_message = self.validate_image(file)
        if not is_valid:
            return Response(
                {"detail": error_message},
                status=status.HTTP_400_BAD_REQUEST
            )

        upload_result = cloudinary.uploader.upload(
            file,
            folder="ztudy/thumbnails/",
            public_id=f"room_{room.id}_thumbnail",
            overwrite=True,
        )

        room.thumbnail = upload_result["secure_url"]
        room.save()

        return Response({"thumbnail": room.thumbnail}, status=status.HTTP_201_CREATED)


class UploadCategoryThumbnailView(BaseThumbnailUploadView):
    @swagger_auto_schema(
        request_body=CategoryThumbnailUploadSerializer,
        responses={201: openapi.Response(
            'Thumbnail uploaded successfully', CategoryThumbnailUploadSerializer)},
        operation_description="Upload an thumbnail image to Cloudinary",
    )
    def post(self, request, *args, **kwargs):
        category = get_object_or_404(RoomCategory, id=kwargs['pk'])
        file = request.FILES.get('thumbnail')

        is_valid, error_message = self.validate_image(file)
        if not is_valid:
            return Response(
                {"detail": error_message},
                status=status.HTTP_400_BAD_REQUEST
            )

        upload_result = cloudinary.uploader.upload(
            file,
            folder="ztudy/category_thumbnails/",
            public_id=f"category_{category.id}_thumbnail",
            overwrite=True
        )

        category.thumbnail = upload_result['secure_url']
        category.save()

        return Response({'thumbnail': category.thumbnail}, status=status.HTTP_201_CREATED) 