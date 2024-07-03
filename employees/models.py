from django.db import models
from utils.validators import validate_file_extension
from utils.models import AbstractBaseModel
from utils.validators import validate_international_phone_number
from django.core.exceptions import ValidationError
import uuid


DEPARTMENT_CHOICES = (
    ('geo', 'geo'),
    ('it', 'it'),
    ('system_dev', 'system_dev'),
    ('training', 'training'),
       
)



class Documents(AbstractBaseModel, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    national_id = models.FileField(
        upload_to="documents/", validators=[validate_file_extension]
    )
    kra_certificate = models.FileField(
        upload_to="documents/", validators=[validate_file_extension]
    )
    passport_photo = models.ImageField(upload_to="documents/")
    others = models.FileField(
        upload_to="documents/", validators=[validate_file_extension], blank=True
    )

class Equipments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    employee = models.ForeignKey('Employee', related_name='equipments', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Employee(AbstractBaseModel, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=100)
    id_number = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True,choices=DEPARTMENT_CHOICES)
    team = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField()
    county = models.CharField(max_length=100)
    sub_county = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    documents = models.OneToOneField(Documents, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def clean(self):
        super().clean()
        phone = self.phone

        if not validate_international_phone_number(phone):
            raise ValidationError(
                {"phone": "Please enter a valid international phone number."}
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
