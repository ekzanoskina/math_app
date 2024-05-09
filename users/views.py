from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm
from exam.models import *


# Create your views here.
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': "Вход"}
    def form_valid(self, form):
        # Вызываем базовый метод form_valid для обработки авторизации
        response = super().form_valid(form)

        # Получаем параметр 'next' из GET запроса
        next_url = self.request.GET.get('next', None)
        if next_url:
            return redirect(next_url)
        else:
            # Если параметр 'next' не указан, перенаправляем на главную страницу или другую страницу по умолчанию
            return redirect('home')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}

    def get_success_url(self):
        # Получаем параметр 'next' из запроса
        next_url = self.request.GET.get('next', '')
        login_url = reverse_lazy('users:login')

        # Если параметр 'next' есть, добавляем его к URL авторизации
        if next_url:
            login_url = f"{login_url}?next={next_url}"
        return login_url


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': "Профиль пользователя"}

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
    extra_context = {'title': "Изменение пароля"}




