from django.shortcuts import get_object_or_404
from rest_framework import generics
from django.http import StreamingHttpResponse
from ..models import Sound
from rest_framework.parsers import MultiPartParser, FormParser
from ..serializers import SoundSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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


class StreamAudioView(APIView):
    def get(self, request, pk):
        sound = get_object_or_404(Sound, id=pk)
        try:
            chunk_size = 8192  

            def file_iterator(file_object, chunk_size=chunk_size):
                while True:
                    data = file_object.read(chunk_size)
                    if not data:
                        break
                    yield data

            response = StreamingHttpResponse(
                file_iterator(sound.sound_file),
                content_type='audio/mpeg'
            )

            # Sửa audio_file thành sound_file
            response['Content-Disposition'] = f'inline; filename="{sound.sound_file.name}"'
            response['Accept-Ranges'] = 'bytes'

            return response

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
