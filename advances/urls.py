from django.urls import path
from .views import AdvanceListCreateView, AdvanceDetailView,ApproveUnapprovedAdvancesView

urlpatterns = [
    path('api/advances/', AdvanceListCreateView.as_view(), name='advance-list-create'),
    path('api/advances/<int:pk>', AdvanceDetailView.as_view(), name='advance-detail'),
    path('api/advances/approve/', ApproveUnapprovedAdvancesView.as_view(), name='approve-advances'),
]
