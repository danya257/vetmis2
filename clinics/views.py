# clinics/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User
from .models import Clinic
from .forms import ClinicForm


# === 1. Публичный каталог (доступен всем) ===
class PublicClinicListView(ListView):
    model = Clinic
    template_name = 'clinics/clinic_list_public.html'
    context_object_name = 'clinics'
    ordering = ['name']


# === 2. Личный кабинет клиники (только для vet / clinic_admin) ===
class ClinicListView(LoginRequiredMixin, ListView):
    model = Clinic
    template_name = 'clinics/clinic_list.html'
    context_object_name = 'clinics'

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type not in ['vet', 'clinic_admin']:
            raise PermissionDenied("Только сотрудники клиник могут просматривать этот раздел.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Clinic.objects.filter(admins=self.request.user)


class ClinicDetailView(LoginRequiredMixin, DetailView):
    model = Clinic
    template_name = 'clinics/clinic_detail.html'
    context_object_name = 'clinic'

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type not in ['vet', 'clinic_admin']:
            raise PermissionDenied("Доступ запрещён.")
        return super().dispatch(request, * args, **kwargs)


class ClinicCreateView(LoginRequiredMixin, CreateView):
    model = Clinic
    form_class = ClinicForm
    template_name = 'clinics/clinic_form.html'
    success_url = reverse_lazy('clinics:clinic_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != 'clinic_admin':
            raise PermissionDenied("Только администраторы клиник могут создавать клиники.")
        return super().dispatch(request, *args, **kwargs)


# === 3. Регистрация новой клиники (B2B) ===
class ClinicRegisterForm(UserCreationForm):
    clinic_name = forms.CharField(
        max_length=200,
        label='Название ветеринарной клиники',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    clinic_address = forms.CharField(
        label='Адрес клиники',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'clinic_admin'
        if commit:
            user.save()
        return user


class ClinicRegisterView(CreateView):
    form_class = ClinicRegisterForm
    template_name = 'clinics/clinic_register.html'
    success_url = reverse_lazy('clinics:clinic_list')

    def form_valid(self, form):
        # Сохраняем пользователя
        user = form.save()
        # Создаём клинику
        clinic = Clinic.objects.create(
            name=form.cleaned_data['clinic_name'],
            address=form.cleaned_data['clinic_address']
        )
        clinic.admins.add(user)
        login(self.request, user)
        return redirect(self.success_url)