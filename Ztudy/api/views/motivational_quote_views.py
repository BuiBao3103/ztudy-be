from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from ..pagination import CustomPagination
import random
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from core.models import MotivationalQuote
from ..serializers import MotivationalQuoteSerializer

class MotivationalQuoteListCreate(generics.ListCreateAPIView):
    queryset = MotivationalQuote.objects.all()
    serializer_class = MotivationalQuoteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['quote', 'author']
    search_fields = ['quote', 'author']
    ordering_fields = ['id']
    pagination_class = CustomPagination

class MotivationalQuoteRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = MotivationalQuote.objects.all()
    serializer_class = MotivationalQuoteSerializer
    lookup_field = 'pk'

class RandomMotivationalQuoteView(APIView):
    """
    API trả về một quote ngẫu nhiên, với format giống như API GET by id.
    """

    def get(self, request, *args, **kwargs):
        count = MotivationalQuote.objects.count()
        if count == 0:
            return Response({"detail": "No quotes found"}, status=status.HTTP_404_NOT_FOUND)

        random_index = random.randint(0, count - 1)
        quote = MotivationalQuote.objects.all()[random_index]  # Lấy dòng ngẫu nhiên theo index
        serializer = MotivationalQuoteSerializer(quote)

        return Response(serializer.data, status=status.HTTP_200_OK)
