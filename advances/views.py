from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Advance, Employee
from .serializers import AdvanceSerializer
from django.db.models import Q
from rest_framework.exceptions import APIException

class EmployeeNotFound(APIException):
    status_code = 500
    default_detail = "Employee does not exist, please create or update the employee object for this user account."
    default_code = 'employee_not_found'

class AdvanceListCreateView(generics.ListCreateAPIView):
    queryset = Advance.objects.all().order_by('-created_at')
    serializer_class = AdvanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            employee = Employee.objects.get(email=self.request.user.email)
        except Employee.DoesNotExist:
            raise EmployeeNotFound()

        if str(self.request.user.role) in ["management", "admin", "tech_lead"]:
            return Advance.objects.filter(Q(employee=employee) | Q(is_approved=False) & Q(is_cancelled=False)).order_by('-created_at')
        
        return Advance.objects.filter(employee=employee)

    def perform_create(self, serializer):
        try:
            employee = Employee.objects.get(email=self.request.user.email)
        except Employee.DoesNotExist:
            raise EmployeeNotFound()

        serializer.save(employee=employee)



class AdvanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Advance.objects.all()
    serializer_class = AdvanceSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        """override update method based on employee role"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user = request.user
       
    

        # Staff role: can only update their own advance and only 'is_cancelled' field
        if user.role == 'staff':
        
            if instance.employee.email != user.email:
                return Response({"detail": "You do not have permission to update this advance."}, status=status.HTTP_403_FORBIDDEN)
            
            # Check if only 'is_cancelled' is being updated
            if 'is_cancelled' not in request.data or len(request.data) > 1:
                return Response({"detail": "Staff can only cancell thier advance request"}, status=status.HTTP_400_BAD_REQUEST)

        # Other roles: cannot update 'is_approved' or 'is_rejected' for their own advances
        if user.role in ['management', 'admin', 'tech_lead']:
            
            if instance.is_cancelled == True:
                return Response({"detail": "You cannot approve cancelled request!"}, status=status.HTTP_400_BAD_REQUEST)

            if instance.is_rejected == True:
                return Response({"detail": "You cannot approve rejected request!"}, status=status.HTTP_400_BAD_REQUEST)        
            
            if instance.employee.email == user.email:
                if 'is_approved' in request.data or 'is_rejected' in request.data:
                    return Response({"detail": "You cannot approve or reject  your own advance request!"}, status=status.HTTP_400_BAD_REQUEST)
                
           
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_destroy(self, instance):
        if self.request.user.role != 'admin':
            return Response({"detail": "You do not have permission to delete this advance."}, status=status.HTTP_403_FORBIDDEN)
        
        instance.delete()
        return Response({"detail": "Advance successfully deleted"}, status=status.HTTP_204_NO_CONTENT)


class ApproveUnapprovedAdvancesView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Check user role
        if str(request.user.role) not in ["management", "admin", "tech_lead"]:
            return Response({"detail": "You do not have permission to approve advances."}, status=status.HTTP_403_FORBIDDEN)
        
        # Filter and update advances
        advances = Advance.objects.filter(is_approved=False, is_rejected=False, is_cancelled=False).exclude(employee=request.user)
        updated_count = advances.update(is_approved=True)
        
        return Response({"detail": f"{updated_count} advances successfully approved."}, status=status.HTTP_200_OK)