from rest_flex_fields.views import FlexFieldsMixin
from ..models import BackgroundVideo, BackgroundVideoType
from ..serializers import BackgroundVideoSerializer, BackgroundVideoTypeSerializer
from .base_views import BaseListCreateView, BaseRetrieveUpdateDestroyView

class BackgroundVideoListCreate(FlexFieldsMixin, BaseListCreateView):
    queryset = BackgroundVideo.objects.all()
    serializer_class = BackgroundVideoSerializer
    permit_list_expands = ['type']


class BackgroundVideoRetrieveUpdateDestroy(FlexFieldsMixin, BaseRetrieveUpdateDestroyView):
    queryset = BackgroundVideo.objects.all()
    serializer_class = BackgroundVideoSerializer
    permit_list_expands = ['type']

class BackgroundVideoTypeListCreate(BaseListCreateView):
    queryset = BackgroundVideoType.objects.all()
    serializer_class = BackgroundVideoTypeSerializer

class BackgroundVideoTypeRetrieveUpdateDestroy(BaseRetrieveUpdateDestroyView):
    queryset = BackgroundVideoType.objects.all()
    serializer_class = BackgroundVideoTypeSerializer

