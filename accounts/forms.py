from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'w-full p-2 outline outline-blue-600 rounded-[5px]',
        'placeholder': 'Email',
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full p-2 outline outline-blue-600 rounded-[5px]',
        'placeholder': 'Password',
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full p-2 outline outline-blue-600 rounded-[5px]',
        'placeholder': 'Password again',
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full p-2 outline outline-blue-600 rounded-[5px]',
                'placeholder': 'Username',
            }),
        }
