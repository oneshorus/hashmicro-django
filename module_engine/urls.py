from django.urls import path
from . import views

urlpatterns = [
    path('', views.module_list, name='module-list'),
    path('modules/install/<str:module_name>/', views.install_module, name='install-module'),
    path('modules/uninstall/<str:module_name>/', views.uninstall_module, name='uninstall-module'),
    path('modules/upgrade/<str:module_name>/', views.upgrade_module, name='upgrade-module'),
]