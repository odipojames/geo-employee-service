from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Advance, Employee
from .serializers import AdvanceSerializer
from django.db.models import Q
from rest_framework.exceptions import APIException
from utils.notifications import send_notification
from datetime import datetime



class EmployeeNotFound(APIException):
    status_code = 400
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
        
        return Advance.objects.filter(employee=employee).order_by('-created_at')

   

    def perform_create(self, serializer):
        try:
            employee = Employee.objects.get(email=self.request.user.email)
        except Employee.DoesNotExist:
            raise EmployeeNotFound()

        instance = serializer.save(employee=employee)
        
        # Create a structured response for notifications
        response = {
            "id": str(instance.id),
            "amount": instance.amount,
            "date": instance.date.isoformat(),# Convert date to string
            "is_approved": instance.is_approved,
            "is_cancelled": instance.is_cancelled,
            "is_rejected": instance.is_rejected,
            "created_at": instance.created_at.isoformat(), 
            "employee": {
                "id": str(instance.employee.id),
                "email": instance.employee.email,
                "first_name": instance.employee.first_name,
                "second_name": instance.employee.second_name,
                "salary": instance.employee.salary,
            },
        }

        
        
        # Prepare the notification payload and message
        payload = response  
        type = 'advance_request'

        # Convert the date string back to a datetime object 
        date_str = response['date']
        if isinstance(date_str, str):
            date_obj = datetime.fromisoformat(date_str)
        else:
            date_obj = date_str

        # Format the month and year
        month_name = date_obj.strftime('%B') 
        year = date_obj.strftime('%Y')  
        message = f'Request for salary advance for the month of {month_name} {year}.'

        # Send the notification
        token = self.request.headers.get('Authorization').split(' ')[1]
        send_notification(payload, type, message,token)

        
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
                return Response({"detail": "Staff can only cancel their advance request"}, status=status.HTTP_400_BAD_REQUEST)

        # Other roles: cannot update 'is_approved' or 'is_rejected' for their own advances
        if user.role in ['management', 'admin', 'tech_lead']:
            if instance.is_cancelled:
                return Response({"detail": "You cannot approve cancelled request!"}, status=status.HTTP_400_BAD_REQUEST)

            if instance.is_rejected:
                return Response({"detail": "You cannot approve rejected request!"}, status=status.HTTP_400_BAD_REQUEST)
            
            if instance.employee.email == user.email:
                if 'is_approved' in request.data or 'is_rejected' in request.data:
                    return Response({"detail": "You cannot approve or reject your own advance request!"}, status=status.HTTP_400_BAD_REQUEST)

        # Update the instance
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Send notifications based on the updated status
        if 'is_approved' in request.data and request.data['is_approved']:
            self.send_advance_notification(instance, "Your advance request has been approved", request)
        elif 'is_rejected' in request.data and request.data['is_rejected']:
            self.send_advance_notification(instance, "Your advance request has been rejected", request)

        return Response(serializer.data)

    def send_advance_notification(self, advance_instance, message, request):
        payload = {
            "id": str(advance_instance.id),
            "amount": str(advance_instance.amount),
            "date": advance_instance.date.isoformat(),
            "is_approved": advance_instance.is_approved,
            "is_cancelled": advance_instance.is_cancelled,
            "is_rejected": advance_instance.is_rejected,
            "created_at": advance_instance.created_at.isoformat(),
            "employee": {
                "id": str(advance_instance.employee.id),
                "email": advance_instance.employee.email,
                "first_name": advance_instance.employee.first_name,
                "second_name": advance_instance.employee.second_name
            },
        }
        token = request.headers.get('Authorization').split(' ')[1]
        type = 'advance'
        # Call the notification function
        send_notification(payload, type, message, token)

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
        
        # Filter advances
        advances = Advance.objects.filter(is_approved=False, is_rejected=False, is_cancelled=False).exclude(employee=request.user.id)
        
        # Update advances and send notifications
        updated_count = 0
        for advance in advances:
            advance.is_approved = True
            advance.save()
            self.send_advance_notification(advance, "Your advance request has been approved", request)
            updated_count += 1
        
        return Response({"detail": f"{updated_count} advances successfully approved."}, status=status.HTTP_200_OK)

    def send_advance_notification(self, advance_instance, message, request):
        payload = {
            "id": str(advance_instance.id),
            "amount": str(advance_instance.amount),
            "date": advance_instance.date.isoformat(),
            "is_approved": advance_instance.is_approved,
            "is_cancelled": advance_instance.is_cancelled,
            "is_rejected": advance_instance.is_rejected,
            "created_at": advance_instance.created_at.isoformat(),
            "employee": {
                "id": str(advance_instance.employee.id),
                "email": advance_instance.employee.email,
                "first_name": advance_instance.employee.first_name,
                "second_name": advance_instance.employee.second_name
            },
        }
        token = request.headers.get('Authorization').split(' ')[1]
        type = 'advance'
        # Call the notification function
        send_notification(payload, type, message, token)