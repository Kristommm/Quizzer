from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        help_texts = {
            "username": (""),
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': "form-control form-control-lg",
            'placeholder': 'Username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': "form-control form-control-lg",
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': "form-control form-control-lg",
            'placeholder': "Repeat Password"
        })

    def save(self, commit: bool = ...) -> Any:
        return super().save(commit)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['course']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].widget.attrs.update({
            'class': "form-control form-control-lg",
            'placeholder': 'Pick your Course'
        })
