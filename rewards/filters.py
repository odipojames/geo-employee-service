
import django_filters
from .models import Reward


class RewardFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(field_name='employee__first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='employee__second_name', lookup_expr='icontains')
    team = django_filters.CharFilter(field_name='employee__team', lookup_expr='iexact')
    department = django_filters.CharFilter(field_name='employee__department', lookup_expr='iexact')

    class Meta:
        model = Reward
        fields = ['first_name', 'last_name', 'team', 'department']
