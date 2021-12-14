from django import forms
from main.models import Car, CarType, Reminder, ReminderType, Service, ServiceType, Contractor, CHARGING_VAT_CHOICES, CLIENT_TYPE_CHOICES


DATE_FORMATS = ['%d-%m-%Y', '%d/%m/%Y', '%d/%m/%y', '%Y/%m/%d', '%Y-%m-%d']


class CarModelForm(forms.ModelForm):
    car_type = forms.ModelChoiceField(
        CarType.objects.all(), label='Вид автомобил', empty_label='Избери')

    class Meta:
        model = Car
        fields = ['car_type', 'brand', 'number_plate']
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Марка'}),
            'number_plate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Регистрационен номер'}),
        }


class ReminderModelForm(forms.ModelForm):
    car = forms.ModelChoiceField(
        Car.objects.all(), label='Автомобил', empty_label='Избери')
    reminder_type = forms.ModelChoiceField(
        ReminderType.objects.all(), label='Вид напомняне', empty_label='Избери')
    expiration_date = forms.DateField(label='Дата на изтичане', input_formats=DATE_FORMATS, widget=forms.TextInput(
        attrs={'class': 'form-control date-picker', 'placeholder': 'Дата на изтичане'}))

    class Meta:
        model = Reminder
        fields = ['reminder_type', 'car', 'expiration_date']


class ServiceModelForm(forms.ModelForm):
    car = forms.ModelChoiceField(
        Car.objects.all(), label='Автомобил', empty_label='Избери')
    service_type = forms.ModelChoiceField(
        ServiceType.objects.all(), label='Вид обслужване', empty_label='Избери')
    date = forms.DateField(label='Дата', input_formats=DATE_FORMATS, widget=forms.TextInput(
        attrs={'class': 'form-control date-picker', 'placeholder': 'Дата на извършване'}))
    additional_information = forms.CharField(label='Допълнителна информация', required=False, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Допълнителна информация'}))

    class Meta:
        model = Service
        fields = ['car', 'service_type', 'run',
                  'additional_information', 'date']
        widgets = {
            'run': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Пробег'})
        }


class ContractorsModelForm(forms.ModelForm):
    client_type = forms.ChoiceField(
        label='Тип клиент', choices=CLIENT_TYPE_CHOICES)
    name = forms.CharField(label='Име', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Име'}))
    bulstat = forms.CharField(label='Булстат', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Булстат'}), required=False)
    mol = forms.CharField(label='МОЛ', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'МОЛ'}), required=False)
    country = forms.CharField(label='Държава', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Държава'}), required=False)
    city = forms.CharField(label='Град', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Град'}), required=False)
    address = forms.CharField(label='Адрес', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Адрес'}), required=False)
    phone_number = forms.CharField(label='Телефонен номер', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Телефонен номер'}), required=False)
    email = forms.CharField(label='E-mail', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'E-mail'}), required=False)
    maturity_date = forms.CharField(label='Дата на падеж', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Дата на падеж'}), required=False)
    charging_vat = forms.ChoiceField(
        label='Основание за неначисление на ДДС', choices=CHARGING_VAT_CHOICES, required=False)
    cmr_photo = forms.FileField(
        label='Прикачи ЧМР', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), required=False)
    license_photo = forms.FileField(
        label='Прикачи лиценз или друг документ', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), required=False)
    expiration_date = forms.DateField(label='Дата на изтичане', widget=forms.TextInput(
        attrs={'class': 'form-control date-picker', 'placeholder': 'Дата на изтичане'}), required=False)

    class Meta:
        model = Contractor
        fields = ['client_type', 'name', 'bulstat', 'mol', 'country', 'city', 'address',
                  'phone_number', 'email', 'maturity_date', 'charging_vat', 'cmr_photo', 'license_photo', 'expiration_date']
