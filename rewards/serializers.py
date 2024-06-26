from rest_framework import serializers
from .models import Reward
from employees.models import Employee

class EmployeeRSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'second_name', 'last_name', 'email', 'phone', 'id_number', 'department', 'team', 'age', 'county', 'sub_county', 'salary']

class RewardSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    class Meta:
        model = Reward
        fields = ['id', 'reward', 'description', 'is_paid', 'employee', 'created_at']
        read_only_fields = ['id', 'created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['employee'] = EmployeeRSerializer(instance.employee).data
        return representation
