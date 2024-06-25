from django.urls import path
from .views import EmployeeListCreateView, EmployeeRetrieveUpdateDestroyView,EquipmentsListCreateAPIView,EquipmentsRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('api/employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('api/employees/<int:pk>', EmployeeRetrieveUpdateDestroyView.as_view(), name='employee-detail'),
    path('api/equipments/', EquipmentsListCreateAPIView.as_view(), name='equipments-list-create'),
    path('api/equipments/<int:pk>', EquipmentsRetrieveUpdateDestroyAPIView.as_view(), name='equipments-detail'),
]