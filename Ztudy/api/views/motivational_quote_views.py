from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from ..models import MotivationalQuote
from ..pagination import CustomPagination
from ..serializers import MotivationalQuoteSerializer

class MotivationalQuoteListCreate(generics.ListCreateAPIView):
    queryset = MotivationalQuote.objects.all()
    serializer_class = MotivationalQuoteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['quote', 'author']
    search_fields = ['quote', 'author']
    ordering_fields = ['id']
    pagination_class = CustomPagination


    def perform_create(self, serializer):
        """
        Override phương thức tạo để thêm một câu quote.
        """
        serializer.save()

class MotivationalQuoteRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = MotivationalQuote.objects.all()
    serializer_class = MotivationalQuoteSerializer
    lookup_field = 'pk'
