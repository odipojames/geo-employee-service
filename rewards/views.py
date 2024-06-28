# views.py
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Reward
from .serializers import RewardSerializer, RewardTeamSerializer
from employees.models import Employee
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RewardListCreateView(generics.ListCreateAPIView):
    queryset = Reward.objects.all().order_by('-created_at')
    serializer_class = RewardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ["staff", "tech_lead"]:
            return Reward.objects.filter(employee__email=user.email).order_by('-created_at')
        return Reward.objects.all().order_by('-created_at')

    def create(self, request, *args, **kwargs):
        user = self.request.user
        if user.role != 'management':
            return Response({"message": "You do not have permission to reward an employee"}, status=status.HTTP_403_FORBIDDEN)

        employee_id = request.data.get('employee')
        if not employee_id:
            return Response({"employee": "This field is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response({"employee": "Employee not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the reward
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(employee=employee)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class RewardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        if user.role != 'admin':
            return Response({"message": "You do not have permission to delete rewards."}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)
    

class RewardAllTeamMembersView(views.APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=RewardTeamSerializer)
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.role != 'management':
            return Response({"message": "You do not have permission to reward all team members."}, status=status.HTTP_403_FORBIDDEN)

        serializer = RewardTeamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        team = serializer.validated_data['team']
        reward_amount = serializer.validated_data['reward']
        description = serializer.validated_data['description']

        employees = Employee.objects.filter(team=team)
        if not employees.exists():
            return Response({"message": f"Team '{team}' does not exist."}, status=status.HTTP_404_NOT_FOUND)

        rewards = []
        for employee in employees:
            rewards.append(Reward(reward=reward_amount, description=description, is_paid=False, employee=employee))

        Reward.objects.bulk_create(rewards)

        return Response({"message": f"Rewards successfully created for all team members in team {team}."}, status=status.HTTP_201_CREATED)
