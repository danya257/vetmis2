# clinics/urls.py
from django.urls import path
from . import views

app_name = 'clinics'

urlpatterns = [
    # Публичный каталог
    path('public/', views.PublicClinicListView.as_view(), name='clinic_list_public'),
    
    # Личный кабинет (только для клиник)
    path('', views.ClinicListView.as_view(), name='clinic_list'),
    path('add/', views.ClinicCreateView.as_view(), name='clinic_add'),
    path('<int:pk>/', views.ClinicDetailView.as_view(), name='clinic_detail'),
    
    # Регистрация новой клиники
    path('register/', views.ClinicRegisterView.as_view(), name='clinic_register'),
]