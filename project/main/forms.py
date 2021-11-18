from django import forms
from main.models import Car, Reminder, ReminderType, Service


DATE_FORMATS = ['%d-%m-%Y', '%d/%m/%Y', '%d/%m/%y', '%Y/%m/%d', '%Y-%m-%d']


class CarModelForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'number_plate']
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Марка'}),
            'number_plate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Регистрационен номер'}),
        }


class ReminderModelForm(forms.ModelForm):
    car = forms.ModelChoiceField(
        Car.objects.all(), label="Автомобил", empty_label="Избери")
    reminder_type = forms.ModelChoiceField(
        ReminderType.objects.all(), label="Вид напомняне", empty_label="Избери")
    expiration_date = forms.DateField(input_formats=DATE_FORMATS, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Дата на изтичане'}))

    class Meta:
        model = Reminder
        fields = ['reminder_type', 'car', 'expiration_date']


class ServiceModelForm(forms.ModelForm):
    car = forms.ModelChoiceField(
        Car.objects.all(), label="Автомобил", empty_label="Избери")
    date = forms.DateField(input_formats=DATE_FORMATS, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Дата на извършване'}))

    class Meta:
        model = Service
        fields = ['car', 'service_type', 'run',
                  'additional_information', 'date']
        widgets = {
            'service_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Вид на обслужване'}),
            'additional_information': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Допълнителна информация'}),
            'run': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Пробег'})
        }
