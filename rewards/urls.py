from django.urls import path
from .views import RewardListCreateView, RewardDetailView, RewardAllTeamMembersView

urlpatterns = [
    path('rewards/', RewardListCreateView.as_view(), name='reward-list-create'),
    path('rewards/<uuid:pk>', RewardDetailView.as_view(), name='reward-detail'),
    path('rewards/team/', RewardAllTeamMembersView.as_view(), name='reward-all-team-members'),
]
