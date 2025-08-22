
from .models import User_profile
from django.contrib.auth.forms import UserCreationForm

class signupForm(UserCreationForm):
    class Meta:
        model = User_profile
        fields = ['username', 'password1', 'password2', 'email', 'user_type']
