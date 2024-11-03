from .views import *
from django.urls import path

urlpatterns = [
    path('', GroupListView.as_view(), name='group_list'),
    path('create/', GroupCreateView.as_view(), name='group_create'),
    path('update/<int:pk>/', GroupUpdateView.as_view(), name='group_update'),
    path('delete/<int:pk>/', GroupDeleteView.as_view(), name='group_delete'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('create_customer/', CreateCustomerView.as_view(), name='create_customer'),
    path('list_customer/', ListCustomerView.as_view(), name='list_customer'),
    path('update_customer/<int:pk>/', UpdateCustomerView.as_view(), name='update_customer'),
    path('delete_customer/<int:pk>/', DeleteCustomerView.as_view(), name='delete_customer'),
    path('customer/<int:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
    path('attendance/<int:group_id>/', AttendanceView.as_view(), name='attendance'),
] 
