from django.db import models
from employees.models import Employee
from utils.models import AbstractBaseModel
import uuid

class Reward(AbstractBaseModel,models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reward = models.DecimalField(max_digits=10,decimal_places=2)
    description = models.CharField(max_length=300)
    is_paid =models.BooleanField(default=False)
    employee = models.ForeignKey(Employee, related_name='rewards', on_delete=models.CASCADE)
        
    def __str__(self):
        return self.description