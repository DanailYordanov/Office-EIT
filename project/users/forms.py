from django import forms
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.forms import LoginForm, SignupForm, ResetPasswordKeyForm, ResetPasswordForm, ChangePasswordForm, AddEmailForm
from .models import CustomUser, UserDocument, DocumentType
from main.models import Bank
from main.forms import CustomModelSelectWidget, CustomBaseInlineFormSet, TagModelChoiceField, CustomSelectTagWidget


DATE_FORMATS = ['%d-%m-%Y', '%d/%m/%Y', '%d/%m/%y', '%Y/%m/%d', '%Y-%m-%d']


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['username', 'first_name', 'middle_name', 'last_name']


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(label='Име', max_length=150, required=True)
    middle_name = forms.CharField(
        label='Презиме', max_length=150, required=False)
    last_name = forms.CharField(label='Фамилия', max_length=150, required=True)

    class Meta:
        fields = ['username', 'email', 'first_name', 'middle_name',
                  'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Потребителско име'})
        self.fields['email'].widget = forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'E-mail'})
        self.fields['first_name'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Име'})
        self.fields['middle_name'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Презиме'})
        self.fields['last_name'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Фамилия'})
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Парола'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Парола отново'})

    def save(self, request):
        user = super().save(request)
        user.middle_name = self.cleaned_data.get('middle_name')
        user.save()

        return user


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['login'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Потребителско име'})
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Парола'})


class CustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget = forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'E-mail'})


class CustomChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['oldpassword'].widget = forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Стара парола'})
        self.fields['password1'].widget = forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Парола'})
        self.fields['password2'].widget = forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Парола отново'})


class CustomAddEmailFormForm(AddEmailForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'E-mail'})


class CustomResetPasswordKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Парола'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Парола отново'})


class ProfileDetailsForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'middle_name',
            'last_name',
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
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Собствено име'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Презиме'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилно име'}),
            'personal_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ЕГН'}),
            'id_card_expiration': forms.DateInput(attrs={'class': 'form-control date-picker', 'placeholder': 'Изтичане на лична карта'}),
            'drivers_license_expiration': forms.DateInput(attrs={'class': 'form-control date-picker', 'placeholder': 'Изтичане на шофьорска книжка'}),
            'professional_competence': forms.DateInput(attrs={'class': 'form-control date-picker', 'placeholder': 'Изтичане на професионална компетентност'}),
            'adr_expiration': forms.DateInput(attrs={'class': 'form-control date-picker', 'placeholder': 'Изтичане на ADR'}),
            'digital_card_expiration': forms.DateInput(attrs={'class': 'form-control date-picker', 'placeholder': 'Изтичане на дигитална карта'}),
            'psychological_test_expiration': forms.DateInput(attrs={'class': 'form-control date-picker', 'placeholder': 'Изтичане на психотест'}),
            'pasport_expiration': forms.DateInput(attrs={'class': 'form-control date-picker', 'placeholder': 'Изтичане на паспорт'}),
            'debit_card_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер на дебитна карта'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефонен номер'}),
            'bank': CustomModelSelectWidget(
                model=Bank,
                search_fields=['name__icontains', 'iban__icontains']
            )
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not user.is_staff:
            del self.fields['bank']
            del self.fields['debit_card_number']


class UserDocumentModelForm(forms.ModelForm):
    document_type = TagModelChoiceField(
        DocumentType.objects.all(),
        label='Тип документ',
        to_field_name='document_type',
        widget=CustomSelectTagWidget(
            model=DocumentType,
            field_name='document_type',
            search_fields=['document_type__icontains'],
            data_url=reverse_lazy('main:tag-auto-select-options',
                                  args=('document_type',))
        )
    )

    class Meta:
        model = UserDocument
        exclude = ('user', )
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            if hasattr(self.instance.document_type, 'document_type'):
                self.initial['document_type'] = self.instance.document_type.document_type


UserDocumentFormset = forms.inlineformset_factory(
    get_user_model(), UserDocument, formset=CustomBaseInlineFormSet, form=UserDocumentModelForm, extra=0)
