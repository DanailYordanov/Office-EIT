from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.forms import LoginForm, SignupForm, ResetPasswordKeyForm, ResetPasswordForm, ChangePasswordForm, AddEmailForm, SetPasswordForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget = forms.EmailInput(
            attrs={'class': 'form-control'})
        self.fields['first_name'].widget = forms.EmailInput(
            attrs={'class': 'form-control'})
        self.fields['last_name'].widget = forms.EmailInput(
            attrs={'class': 'form-control'})
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control'})


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['login'].widget = forms.EmailInput(
            attrs={'class': 'form-control'})
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'class': 'form-control'})


class CustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget = forms.EmailInput(
            attrs={'class': 'form-control'})


class CustomChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['oldpassword'].widget = forms.EmailInput(
            attrs={'class': 'form-control'})
        self.fields['password1'].widget = forms.EmailInput(
            attrs={'class': 'form-control'})
        self.fields['password2'].widget = forms.EmailInput(
            attrs={'class': 'form-control'})


class CustomAddEmailFormForm(AddEmailForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(
            attrs={'class': 'form-control'})


class CustomResetPasswordKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control'})


class UserDocumentsForm(forms.ModelForm):
    class Meta:
        models = get_user_model()
        fields = [
            'id_card_expiration',
            'drivers_license_expiration',
            'professional_competence',
            'adr_expiration',
            'digital_card_expiration',
            'psychological_test_expiration',
            'pasport_expiration'
        ]
