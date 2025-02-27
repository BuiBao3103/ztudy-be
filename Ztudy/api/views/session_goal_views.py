from rest_flex_fields.views import FlexFieldsMixin
from ..models import SessionGoal
from ..serializers import SessionGoalSerializer
from .base_views import BaseListCreateView, BaseRetrieveUpdateDestroyView, SwaggerExpandMixin
from ..filters import SessionGoalFilter

class SessionGoalListCreate(FlexFieldsMixin, SwaggerExpandMixin, BaseListCreateView):
    queryset = SessionGoal.objects.all()
    serializer_class = SessionGoalSerializer
    filterset_class = SessionGoalFilter
    permit_list_expands = ['user']

class SessionGoalRetrieveUpdateDestroy(FlexFieldsMixin, SwaggerExpandMixin, BaseRetrieveUpdateDestroyView):
    queryset = SessionGoal.objects.all()
    serializer_class = SessionGoalSerializer
    permit_list_expands = ['user']


