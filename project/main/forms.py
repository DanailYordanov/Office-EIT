from django import forms
from main.models import Car


class CarModelForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'number_plate']
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Марка'}),
            'number_plate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Регистрационен номер'}),
        }
