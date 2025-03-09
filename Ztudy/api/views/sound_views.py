from rest_framework import generics
from ..models import Sound
from rest_framework.parsers import MultiPartParser, FormParser
from ..serializers import SoundSerializer

class SoundList(generics.ListAPIView):
    queryset = Sound.objects.all()
    serializer_class = SoundSerializer

class SoundDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sound.objects.all()
    serializer_class = SoundSerializer

class SoundUpload(generics.CreateAPIView):
    queryset = Sound.objects.all()
    serializer_class = SoundSerializer
    parser_classes = (MultiPartParser, FormParser)
