import django_filters
from .models import SessionGoal

class SessionGoalFilter(django_filters.FilterSet):
    user = django_filters.NumberFilter(field_name="user", lookup_expr="exact")  # user = value
    # user_gt = django_filters.NumberFilter(field_name="user", lookup_expr="gt")  # user > value
    # user_gte = django_filters.NumberFilter(field_name="user", lookup_expr="gte")  # user >= value
    # user_lt = django_filters.NumberFilter(field_name="user", lookup_expr="lt")  # user < value
    # user_lte = django_filters.NumberFilter(field_name="user", lookup_expr="lte")  # user <= value

    class Meta:
        model = SessionGoal
        # fields = ['user', 'user_gt', 'user_gte', 'user_lt', 'user_lte']
        fields = ['user']