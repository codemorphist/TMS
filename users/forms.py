from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class PanelUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2',
                  'first_name', 'last_name', 'email')
        labels = {
            'username': 'Username',
            'password1': 'Password',
            'password2': 'Repeat Password',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'E-mail',
        }
