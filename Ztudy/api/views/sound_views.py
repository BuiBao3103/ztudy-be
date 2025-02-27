from rest_framework import generics
from ..models import Sound
from ..serializers import SoundSerializer

class SoundList(generics.ListAPIView):
    queryset = Sound.objects.all()
    serializer_class = SoundSerializer




