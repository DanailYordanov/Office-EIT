from django import forms
from main.models import Car, Reminder, ReminderType


class CarModelForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'number_plate']
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Марка'}),
            'number_plate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Регистрационен номер'}),
        }


class ReminderModelForm(forms.ModelForm):
    car = forms.ModelChoiceField(Car.objects.all(), label="Автомобил", empty_label="Избери")
    reminder_type = forms.ModelChoiceField(ReminderType.objects.all(), label="Вид напомняне", empty_label="Избери")
    expiration_date = forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Дата на изтичане'}),)
    class Meta:
        model = Reminder
        fields = ['reminder_type', 'car', 'expiration_date']