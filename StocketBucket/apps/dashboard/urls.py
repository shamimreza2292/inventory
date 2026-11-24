from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('orders/', views.orders, name='orders'),
    path('customers/', views.customers, name='customers'),
    path('reports/', views.reports, name='reports'),
]
