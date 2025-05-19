from django.urls import path
from . import views


urlpatterns = [
    path('', views.list_products, name='product02_list'),
    path('create/', views.create_product, name='product02_create'),
    path('update/<int:pk>/', views.update_product, name='product02_update'),
    path('delete/<int:pk>/', views.delete_product, name='product02_delete'),
]