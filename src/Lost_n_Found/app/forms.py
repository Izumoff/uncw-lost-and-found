"""
app/forms.py
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from app.models import Report


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': 'User name'
        })
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput({
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class CampusUserRegistrationForm(UserCreationForm):
    """Registration form for campus community users."""
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput({
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': 'User name'
        })
    )
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput({
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        label=_("Confirm password"),
        widget=forms.PasswordInput({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )

    def clean_email(self):
        """Validate that email is unique."""
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email


class RegistrationVerificationCodeForm(forms.Form):
    """Verification code form for placeholder registration step."""
    code = forms.CharField(
        max_length=50,
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': 'Verification code'
        })
    )


class FoundItemReportForm(forms.ModelForm):
    """Form for creating a found item report."""

    class Meta:
        model = Report
        fields = ("title", "description", "location_text")
        widgets = {
            "title": forms.TextInput({
                'class': 'form-control',
                'placeholder': 'Report title'
            }),
            "description": forms.Textarea({
                'class': 'form-control',
                'placeholder': 'Describe the found item',
                'rows': 5
            }),
            "location_text": forms.TextInput({
                'class': 'form-control',
                'placeholder': 'Location where the item was found'
            }),
        }