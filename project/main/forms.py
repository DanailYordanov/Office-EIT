from django import forms
from django.contrib.auth import get_user_model
from main import models


DATE_FORMATS = ['%d-%m-%Y', '%d/%m/%Y', '%d/%m/%y', '%Y/%m/%d', '%Y-%m-%d']


class CarModelForm(forms.ModelForm):
    car_type = forms.ModelChoiceField(
        models.CarType.objects.all(), label='Вид автомобил', empty_label='Избери')

    class Meta:
        model = models.Car
        fields = ['car_type', 'brand', 'number_plate']
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Марка'}),
            'number_plate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Регистрационен номер'}),
        }


class ReminderModelForm(forms.ModelForm):
    car = forms.ModelChoiceField(
        models.Car.objects.all(), label='Автомобил', empty_label='Избери')
    reminder_type = forms.ModelChoiceField(
        models.ReminderType.objects.all(), label='Вид напомняне', empty_label='Избери')
    expiration_date = forms.DateField(label='Дата на изтичане', input_formats=DATE_FORMATS, widget=forms.TextInput(
        attrs={'class': 'form-control date-picker', 'placeholder': 'Дата на изтичане'}))

    class Meta:
        model = models.Reminder
        fields = ['reminder_type', 'car', 'expiration_date']


class ServiceModelForm(forms.ModelForm):
    car = forms.ModelChoiceField(
        models.Car.objects.all(), label='Автомобил', empty_label='Избери')
    service_type = forms.ModelChoiceField(
        models.ServiceType.objects.all(), label='Вид обслужване', empty_label='Избери')
    date = forms.DateField(label='Дата', input_formats=DATE_FORMATS, widget=forms.TextInput(
        attrs={'class': 'form-control date-picker', 'placeholder': 'Дата на извършване'}))
    additional_information = forms.CharField(label='Допълнителна информация', required=False, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Допълнителна информация'}))

    class Meta:
        model = models.Service
        fields = ['car', 'service_type', 'run',
                  'additional_information', 'date']
        widgets = {
            'run': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Пробег'})
        }


class ContractorsModelForm(forms.ModelForm):
    client_type = forms.ChoiceField(
        label='Тип клиент', choices=models.CLIENT_TYPE_CHOICES)
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
        label='Основание за неначисление на ДДС', choices=models.CHARGING_VAT_CHOICES, required=False)
    cmr_photo = forms.FileField(
        label='Прикачи ЧМР', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), required=False)
    license_photo = forms.FileField(
        label='Прикачи лиценз или друг документ', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), required=False)
    expiration_date = forms.DateField(label='Дата на изтичане', widget=forms.TextInput(
        attrs={'class': 'form-control date-picker', 'placeholder': 'Дата на изтичане'}), required=False)

    class Meta:
        model = models.Contractor
        fields = ['client_type', 'name', 'bulstat', 'mol', 'country', 'city', 'address',
                  'phone_number', 'email', 'maturity_date', 'charging_vat', 'cmr_photo', 'license_photo', 'expiration_date']


class CourseModelForm(forms.ModelForm):
    car = forms.ModelChoiceField(
        models.Car.objects.all(), label='Автомобил', empty_label='Избери')
    driver = forms.ModelChoiceField(
        get_user_model().objects.filter(is_active=True, is_staff=False), label='Шорфьор', empty_label='Избери')
    contractor = forms.ModelChoiceField(
        models.Contractor.objects.all(), label='Контрагент', empty_label='Избери')
    bank = forms.ModelChoiceField(
        models.Bank.objects.all(), label='Банка', empty_label='Избери')

    class Meta:
        model = models.Course
        fields = ['driver', 'car', 'contractor', 'bank', 'from_to',
                  'description', 'price', 'currency', 'cargo_type', 'other_conditions']
        widgets = {
            'from_to': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Релация'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Цена'}),
            'cargo_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Вид и тегло на товара'}),
            'other_conditions': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Други условия'})
        }


class CourseAddresModelForm(forms.ModelForm):
    load_type = forms.ChoiceField(
        label='Вид на товарене', choices=models.LOADING_TYPE_CHOICES, required=False)
    save = forms.BooleanField(label='Запази', widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}), required=False)

    class Meta:
        model = models.CourseAddress
        fields = ['load_type', 'address_input', 'date', 'save']
        widgets = {
            'address_input': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Адрес', 'list': 'datalistAddresses'}),
            'date': forms.TextInput(
                attrs={'class': 'form-control date-picker', 'placeholder': 'Дата'})
        }


class CustomBaseInlineFormSet(forms.BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields['DELETE'].widget = forms.CheckboxInput(
            attrs={'class': 'form-check-input'})


CourseAddressUpdateFormset = forms.inlineformset_factory(models.Course,
                                                         models.CourseAddress, formset=CustomBaseInlineFormSet, form=CourseAddresModelForm, extra=1)

CourseAddressAddFormset = forms.inlineformset_factory(models.Course,
                                                      models.CourseAddress, form=CourseAddresModelForm, can_delete=False, extra=2)


class AddressModelForm(forms.ModelForm):
    class Meta:
        model = models.Address
        fields = ['address', 'contact_person',
                  'contact_phone', 'gps_coordinates']
        widgets = {
            'address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Адрес'}),
            'contact_person': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Лице за контакт'}),
            'contact_phone': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Телефон за връзка'}),
            'gps_coordinates': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'GPS координати'})
        }


class ExpenseModelForm(forms.ModelForm):
    expense_type = forms.ModelChoiceField(
        models.ExpenseType.objects.all(), label='Вид разход', empty_label='Избери')

    class Meta:
        model = models.Expense
        fields = ['expense_type', 'price', 'currency',
                  'payment_type', 'additional_information']
        widgets = {
            'price': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Цена'}),
            'additional_information': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Допълнителна информация'}),
        }
