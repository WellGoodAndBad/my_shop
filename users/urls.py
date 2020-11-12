from django.urls import path
from .views import LogInView, LogOutView, SignUpView


app_name = "users"

urlpatterns = [
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('registration/', SignUpView.as_view(), name='registration'),
]