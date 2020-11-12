from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'full_name',
            'delivery_address',
            'role',
            'email',
            'password1',
            'password2'

        )