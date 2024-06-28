from rest_framework import generics, permissions,status,filters
from .models import Employee, Equipments
from .serializers import EmployeeSerializer, EquipmentsSerializer
from utils.permissions import IsEmployeeOrAdmin
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .filters import EmployeeFilter

class EmployeeListCreateView(generics.ListCreateAPIView):
    #queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (permissions.IsAuthenticated,IsEmployeeOrAdmin,)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = EmployeeFilter
    #ordering_fields = ['first_name', 'second_name', 'department','team']
    
    def get_queryset(self):
        if str(self.request.user.role)=="staff":
            return Employee.objects.filter(email=self.request.user.email)
        return Employee.objects.all().order_by('-created_at')

    

class EmployeeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (permissions.IsAuthenticated,IsEmployeeOrAdmin,)
    
    def perform_destroy(self, instance):
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Employee successfully deleted"}, status=status.HTTP_204_NO_CONTENT) 
    
    

class EquipmentsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Equipments.objects.all()
    serializer_class = EquipmentsSerializer

class EquipmentsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Equipments.objects.all()
    serializer_class = EquipmentsSerializer
     
    def perform_destroy(self, instance):
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Equipment successfully deleted"}, status=status.HTTP_204_NO_CONTENT) 
