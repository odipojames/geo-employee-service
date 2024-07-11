from rest_framework import serializers
from .models import Advance
from employees.models import Employee
from django.utils import timezone

class EmployeeMSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'id', 'first_name', 'second_name', 'last_name', 'email',
            'phone', 'id_number', 'department', 'team', 'age', 'county',
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
        
            # Check if advance amount is greater than the salary
            amount = data.get('amount')
            if amount is not None and amount > employee.salary:
                raise serializers.ValidationError({"amount": "Advance amount cannot be greater than the salary"})
            
            # Check if the date is in the past
            date = data.get('date')
            if date and date < timezone.now().date():
                raise serializers.ValidationError({"date": "The date cannot be in the past."})

            # Check if the employee has already made an advance request in the same month and year
            current_month = date.month
            current_year = date.year

            existing_advance = Advance.objects.filter(
                employee=employee,
                date__year=current_year,
                date__month=current_month
            ).exists()
            
            if existing_advance:
                raise serializers.ValidationError({"detail": "You can only make one advance request per month within the same year."})
        
        return data
