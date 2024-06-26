from rest_framework import serializers
from .models import Advance
from employees.models import Employee

class EmployeeMSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'id', 'first_name', 'second_name', 'last_name', 'email',
            'phone', 'id_number', 'department', 'team','age', 'county',
            'sub_county', 'salary'
        ]

class AdvanceSerializer(serializers.ModelSerializer):
    date = serializers.DateField(input_formats=['%d/%m/%Y'])
    employee = EmployeeMSerializer(read_only=True)
    
    class Meta:
        model = Advance
        fields = ['id', 'amount', 'date', 'is_approved', 'is_cancelled', 'is_rejected', 'employee']
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        request = self.context.get('request')
        if request:
            employee = Employee.objects.get(email=request.user.email)
            
            # Use data.get() to safely retrieve 'amount' from data
            amount = data.get('amount')
            if amount is not None and amount > employee.salary:
                raise serializers.ValidationError({"amount": "Advance amount cannot be greater than the salary"})
        return data
