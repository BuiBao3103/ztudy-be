from rest_flex_fields.views import FlexFieldsMixin
from ..models import BackgroundVideo, BackgroundVideoType
from ..serializers import BackgroundVideoSerializer, BackgroundVideoTypeSerializer
from .base_views import BaseListCreateView, BaseRetrieveUpdateDestroyView, SwaggerExpandMixin
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
class BackgroundVideoListCreate(FlexFieldsMixin, SwaggerExpandMixin, BaseListCreateView):
    queryset = BackgroundVideo.objects.all()
    serializer_class = BackgroundVideoSerializer
    permit_list_expands = ['type']

class BackgroundVideoRetrieveUpdateDestroy(FlexFieldsMixin, SwaggerExpandMixin, BaseRetrieveUpdateDestroyView):
    queryset = BackgroundVideo.objects.all()
    serializer_class = BackgroundVideoSerializer
    permit_list_expands = ['type']


class BackgroundVideoTypeListCreate(BaseListCreateView):
    queryset = BackgroundVideoType.objects.all()
    serializer_class = BackgroundVideoTypeSerializer

class BackgroundVideoTypeRetrieveUpdateDestroy(BaseRetrieveUpdateDestroyView):
    queryset = BackgroundVideoType.objects.all()
    serializer_class = BackgroundVideoTypeSerializer

