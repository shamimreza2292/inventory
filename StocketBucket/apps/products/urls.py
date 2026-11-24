from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.products_page, name='page'),
    path('list', views.products_list, name='list'),
    path('create/', views.product_create, name='create'),
    path('<int:pk>/', views.product_detail, name='detail'),
    path('<int:pk>/edit/', views.product_update, name='update'),
    path('<int:pk>/delete/', views.product_delete, name='delete'),
]
