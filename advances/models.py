from django.db import models
from employees.models import Employee
from utils.models import AbstractBaseModel
import uuid

class Advance(AbstractBaseModel,models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    date = models.DateField()
    employee = models.ForeignKey(Employee, related_name='advance_requests', on_delete=models.CASCADE)
    is_approved =models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.amount} advance requested by {self.employee.first_name}'

     

