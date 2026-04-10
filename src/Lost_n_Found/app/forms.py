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

    def clean_title(self):
        """Validate and normalize the report title."""
        title = self.cleaned_data["title"].strip()

        if not title:
            raise forms.ValidationError("Title is required.")

        if len(title) < 3:
            raise forms.ValidationError("Title must be at least 3 characters long.")

        return title

    def clean_description(self):
        """Validate and normalize the report description."""
        description = self.cleaned_data["description"].strip()

        if not description:
            raise forms.ValidationError("Description is required.")

        if len(description) < 5:
            raise forms.ValidationError(
                "Description must be at least 5 characters long."
            )

        return description

    def clean_location_text(self):
        """Validate and normalize the report location."""
        location_text = self.cleaned_data["location_text"].strip()

        if not location_text:
            raise forms.ValidationError("Location is required.")

        if len(location_text) < 2:
            raise forms.ValidationError(
                "Location must be at least 2 characters long."
            )

        return location_text