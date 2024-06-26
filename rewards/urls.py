from django.urls import path
from .views import RewardListCreateView, RewardDetailView, RewardAllTeamMembersView

urlpatterns = [
    path('api/rewards/', RewardListCreateView.as_view(), name='reward-list-create'),
    path('api/rewards/<int:pk>', RewardDetailView.as_view(), name='reward-detail'),
    path('api/rewards/team/', RewardAllTeamMembersView.as_view(), name='reward-all-team-members'),
]
