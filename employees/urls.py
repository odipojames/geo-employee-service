from django.urls import path
from .views import EmployeeListCreateView, EmployeeRetrieveUpdateDestroyView,EquipmentsListCreateAPIView,EquipmentsRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('employees/<uuid:pk>', EmployeeRetrieveUpdateDestroyView.as_view(), name='employee-detail'),
    path('equipments/', EquipmentsListCreateAPIView.as_view(), name='equipments-list-create'),
    path('equipments/<uuid:pk>', EquipmentsRetrieveUpdateDestroyAPIView.as_view(), name='equipments-detail'),
]