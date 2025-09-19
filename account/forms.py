# forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User

class CustomUserCreationForm(forms.ModelForm):
    """Form for creating new users, with repeated password entry and hashing."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'role')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don’t match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # ✅ Hashing here
        if commit:
            user.save()
        return user

# forms.py (continued)
class CustomUserChangeForm(forms.ModelForm):
    """Form for updating users — shows the hashed password as read-only."""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'role', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]
