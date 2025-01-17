import django_filters
from .models import Employee

class EmployeeFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    second_name = django_filters.CharFilter(field_name='second_name', lookup_expr='icontains')
    department = django_filters.CharFilter(field_name='department', lookup_expr='exact')
    temam = django_filters.CharFilter(field_name='team', lookup_expr='exact')

    class Meta:
        model = Employee
        fields = ['first_name', 'second_name', 'department','team']
