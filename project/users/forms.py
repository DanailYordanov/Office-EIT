from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.forms import LoginForm, SignupForm, ResetPasswordKeyForm, ResetPasswordForm, ChangePasswordForm, AddEmailForm, SetPasswordForm
from .models import CustomUser
from main.models import Bank


DATE_FORMATS = ['%d-%m-%Y', '%d/%m/%Y', '%d/%m/%y', '%Y/%m/%d', '%Y-%m-%d']


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


class ProfileDetailsForm(forms.ModelForm):
    bank = forms.ModelChoiceField(
        Bank.objects.all(), label='Банка', empty_label='Избери')

    class Meta:
        model = get_user_model()
        fields = [
            'personal_id',
            'id_card_expiration',
            'drivers_license_expiration',
            'professional_competence',
            'adr_expiration',
            'digital_card_expiration',
            'psychological_test_expiration',
            'pasport_expiration',
            'bank',
            'debit_card_number',
            'phone_number'
        ]
        widgets = {
            'personal_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ЕГН'}),
            'id_card_expiration': forms.TextInput(attrs={'class': 'form-control date-picker'}),
            'drivers_license_expiration': forms.TextInput(attrs={'class': 'form-control date-picker'}),
            'professional_competence': forms.TextInput(attrs={'class': 'form-control date-picker'}),
            'adr_expiration': forms.TextInput(attrs={'class': 'form-control date-picker'}),
            'digital_card_expiration': forms.TextInput(attrs={'class': 'form-control date-picker'}),
            'psychological_test_expiration': forms.TextInput(attrs={'class': 'form-control date-picker'}),
            'pasport_expiration': forms.TextInput(attrs={'class': 'form-control date-picker'}),
            'debit_card_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер на дебитна карта'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефонен номер'})
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not user.is_staff:
            del self.fields['bank']
            del self.fields['debit_card_number']
