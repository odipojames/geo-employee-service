from rest_framework import serializers
from .models import Employee, Documents, Equipments
from django.core.exceptions import ValidationError
from utils.validators import validate_international_phone_number

class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = '__all__'
        extra_kwargs = {"id": {"read_only": True}}
        
class EquipmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipments
        fields = '__all__'  
        extra_kwargs = {"id": {"read_only": True}}
              

class EmployeeSerializer(serializers.ModelSerializer):
    documents = DocumentsSerializer()
    equipments = EquipmentsSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = [
            'id', 'first_name', 'second_name', 'last_name', 'email',
            'phone', 'id_number', 'department','team', 'age', 'county',
            'sub_county', 'salary', 'created_at', 'updated_at',
            'documents', 'equipments'
        ]

        extra_kwargs = {"id": {"read_only": True}}
        

    def validate_phone(self, value):
        if not validate_international_phone_number(value):
            raise serializers.ValidationError("Please enter a valid international phone number.")
        return value

    def create(self, validated_data):
        documents_data = validated_data.pop('documents')
        documents = Documents.objects.create(**documents_data)
        employee = Employee.objects.create(documents=documents, **validated_data)
        return employee

    def update(self, instance, validated_data):
        documents_data = validated_data.pop('documents', {})
        equipments_data = validated_data.pop('equipments', [])

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.second_name = validated_data.get('second_name', instance.second_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.id_number = validated_data.get('id_number', instance.id_number)
        instance.age = validated_data.get('age', instance.age)
        instance.county = validated_data.get('county', instance.county)
        instance.sub_county = validated_data.get('sub_county', instance.sub_county)
        instance.salary = validated_data.get('salary', instance.salary)
        instance.department = validated_data.get('department', instance.department)
        instance.team = validated_data.get('team', instance.team)

        documents_instance = instance.documents
        documents_instance.national_id = documents_data.get('national_id', documents_instance.national_id)
        documents_instance.kra_certificate = documents_data.get('kra_certificate', documents_instance.kra_certificate)
        documents_instance.passport_photo = documents_data.get('passport_photo', documents_instance.passport_photo)
        documents_instance.others = documents_data.get('others', documents_instance.others)
        documents_instance.save()

        instance.save()

        instance.equipments.clear()
        for equipment_data in equipments_data:
            equipment, _ = Equipments.objects.get_or_create(**equipment_data)
            instance.equipments.add(equipment)

        return instance