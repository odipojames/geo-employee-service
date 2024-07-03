from django.urls import path
from .views import AdvanceListCreateView, AdvanceDetailView,ApproveUnapprovedAdvancesView

urlpatterns = [
    path('advances/', AdvanceListCreateView.as_view(), name='advance-list-create'),
    path('advances/<uuid:pk>', AdvanceDetailView.as_view(), name='advance-detail'),
    path('advances/approve/', ApproveUnapprovedAdvancesView.as_view(), name='approve-advances'),
]
