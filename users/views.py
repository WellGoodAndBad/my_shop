from django import forms
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView


class LogInView(LoginView):
    template_name = 'users/login.html'

    class Meta:
        widgets = {'email': forms.TextInput(attrs={'class': 'from-control'}),
                   'password': forms.TextInput(attrs={'class': 'from-control'})}


class LogOutView(LogoutView):
    next_page = 'shop:home_page'


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('shop:home_page')
    template_name = 'users/registration.html'

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)

        return valid