# clinics/urls.py
from django.urls import path
from . import views

app_name = 'clinics'

# clinics/urls.py
urlpatterns = [
    path('dashboard/', views.ClinicDashboardView.as_view(), name='dashboard'),
    path('vets/', views.VetListView.as_view(), name='vet_list'),
    path('vet/<int:pk>/', views.VetDetailView.as_view(), name='vet_detail'),
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/create/', views.ServiceCreateView.as_view(), name='service_create'),
    path('services/<int:pk>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('services/<int:pk>/edit/', views.ServiceUpdateView.as_view(), name='service_edit'),
]