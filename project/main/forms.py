from django import forms
from django.urls import reverse_lazy
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
    class Meta:
        model = models.Contractor
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Име'}),
            'bulstat': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Булстат'}),
            'mol': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'МОЛ'}),
            'country': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Държава'}),
            'city': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Град'}),
            'address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Адрес'}),
            'postal_code': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Пощенски код'}),
            'correspondence_address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Адрес за кореспонденция'}),
            'phone_number': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Телефонен номер'}),
            'email': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'maturity_date': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Дата на падеж'}),
            'cmr_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'cmr_expiration_date': forms.TextInput(
                attrs={'class': 'form-control date-picker', 'placeholder': 'Дата на изтичане'}),
            'license_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'license_expiration_date': forms.TextInput(
                attrs={'class': 'form-control date-picker', 'placeholder': 'Дата на изтичане'})
        }


class CourseModelForm(forms.ModelForm):
    car = forms.ModelChoiceField(
        models.Car.objects.all(), label='Автомобил', empty_label='Избери')
    driver = forms.ModelChoiceField(
        get_user_model().objects.filter(is_active=True, is_staff=False), label='Шорфьор', empty_label='Избери')
    company = forms.ModelChoiceField(
        models.Company.objects.all(), label='Фирма', empty_label='Избери')
    contractor = forms.ModelChoiceField(
        models.Contractor.objects.all(),
        label='Контрагент',
        empty_label='Избери',
        widget=forms.Select(
            attrs={
                'data-load-contractor-reminder-url': reverse_lazy('main:load-contractor-reminder'),
                'id': 'contractorID'
            })
    )
    bank = forms.ModelChoiceField(
        models.Bank.objects.all(), label='Банка', empty_label='Избери')
    medical_examination_perpetrator = forms.CharField(
        label='Извършител на медицински преглед', max_length=100, required=False, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Извършител на медицински преглед', 'list': 'datalistMedicalExaminationPerpetrator'}))
    technical_inspection_perpetrator = forms.CharField(
        label='Извършител на технически преглед', max_length=100, required=False, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Извършител на технически преглед', 'list': 'datalistTechnicalInspectionPerpetrator'}))

    class Meta:
        model = models.Course
        exclude = ('create_date',)
        widgets = {
            'request_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер на заявка'}),
            'from_to': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Релация', 'list': 'datalistFromTo'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание'}),
            'course_price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Цена за курс'}),
            'driver_salary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Цена за командировка'}),
            'cargo_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Вид и тегло на товара'}),
            'export': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'mileage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Километраж'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Лице за контакт'}),
            'other_conditions': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Други условия'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            if self.instance.export:
                self.fields['medical_examination_perpetrator'].required = True
                self.fields['technical_inspection_perpetrator'].required = True
                self.fields['medical_examination_perpetrator'].initial = self.instance.medical_examination.perpetrator.perpetrator
                self.fields['technical_inspection_perpetrator'].initial = self.instance.technical_inspection.perpetrator.perpetrator

        if self.data and 'export' in self.data:
            if self.data['export'] == 'on':
                self.fields['medical_examination_perpetrator'].required = True
                self.fields['technical_inspection_perpetrator'].required = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

            if self.cleaned_data['export']:

                if 'technical_inspection_perpetrator' in self.changed_data:

                    technical_inspection_perpetrator = (
                        self.cleaned_data['technical_inspection_perpetrator']).strip()
                    try:
                        perpetrator_instance = models.TechnicalInspectionPerpetrator.objects.get(
                            perpetrator=technical_inspection_perpetrator)
                    except models.TechnicalInspectionPerpetrator.DoesNotExist:
                        perpetrator_instance = models.TechnicalInspectionPerpetrator.objects.create(
                            perpetrator=technical_inspection_perpetrator)
                    finally:

                        try:
                            techincal_inspection_instance = models.CourseTechnicalInspection.objects.get(
                                course=instance)
                        except models.CourseTechnicalInspection.DoesNotExist:
                            models.CourseTechnicalInspection.objects.create(
                                course=instance, perpetrator=perpetrator_instance)
                        else:
                            techincal_inspection_instance.perpetrator = perpetrator_instance
                            techincal_inspection_instance.save()

                if 'medical_examination_perpetrator' in self.changed_data:

                    medical_examination_perpetrator = (
                        self.cleaned_data['medical_examination_perpetrator']).strip()
                    try:
                        perpetrator_instance = models.MedicalExaminationPerpetrator.objects.get(
                            perpetrator=medical_examination_perpetrator)
                    except models.MedicalExaminationPerpetrator.DoesNotExist:
                        perpetrator_instance = models.MedicalExaminationPerpetrator.objects.create(
                            perpetrator=medical_examination_perpetrator)
                    finally:

                        try:
                            medical_examination_instance = models.CourseMedicalExamination.objects.get(
                                course=instance)
                        except models.CourseMedicalExamination.DoesNotExist:
                            models.CourseMedicalExamination.objects.create(
                                course=instance, perpetrator=perpetrator_instance)
                        else:
                            medical_examination_instance.perpetrator = perpetrator_instance
                            medical_examination_instance.save()

            self.save_m2m()
        return instance


class CourseAddresModelForm(forms.ModelForm):
    load_type = forms.ChoiceField(
        label='Товарен/Разтоварен/Митница', choices=models.LOADING_TYPE_CHOICES, required=False)
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
                                                         models.CourseAddress, formset=CustomBaseInlineFormSet, form=CourseAddresModelForm, extra=0)

CourseAddressAddFormset = forms.inlineformset_factory(models.Course,
                                                      models.CourseAddress, form=CourseAddresModelForm, can_delete=False, extra=2)


class AddressModelForm(forms.ModelForm):
    class Meta:
        model = models.Address
        fields = '__all__'
        widgets = {
            'address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Адрес'}),
            'contact_person': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Лице за контакт'}),
            'contact_phone': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Телефон за връзка'}),
            'gps_coordinates': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'GPS координати'}),
            'email': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
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


class TripOrderModelForm(forms.ModelForm):
    driver = forms.ModelChoiceField(
        get_user_model().objects.filter(is_active=True, is_staff=False),
        label='Шорфьор',
        empty_label='Избери',
        widget=forms.Select(
            attrs={
                'data-load-courses-url': reverse_lazy('main:load-course-options'),
                'id': 'driverTripOrderID'
            })
    )
    course_export = forms.ModelChoiceField(
        models.Course.objects.none(),
        label='Курс за износ',
        empty_label='Избери',
        widget=forms.Select(
            attrs={
                'data-load-dates-url': reverse_lazy('main:load-dates'),
                'id': 'courseExportTripOrderID'
            })
    )
    course_import = forms.ModelChoiceField(
        models.Course.objects.none(),
        label='Курс за внос',
        empty_label='Избери',
        widget=forms.Select(
            attrs={
                'data-load-dates-url': reverse_lazy('main:load-dates'),
                'id': 'courseImportTripOrderID'
            })
    )

    class Meta:
        model = models.TripOrder
        fields = ['driver', 'course_export', 'course_import',
                  'destination', 'from_date', 'to_date']
        widgets = {
            'destination': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Дестинация'}),
            'from_date': forms.TextInput(
                attrs={'class': 'form-control date-picker', 'placeholder': 'Начална дата'}),
            'to_date': forms.TextInput(
                attrs={'class': 'form-control date-picker', 'placeholder': 'Крайна дата'})
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if 'driver' in self.data:
            try:
                driver_id = int(self.data.get('driver'))
                self.fields['course_export'].queryset = models.Course.objects.filter(
                    driver__id=driver_id, export=True)
                self.fields['course_import'].queryset = models.Course.objects.filter(
                    driver__id=driver_id, export=False)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['course_export'].queryset = models.Course.objects.filter(
                driver=self.instance.driver, export=True)
            self.fields['course_import'].queryset = models.Course.objects.filter(
                driver=self.instance.driver, export=False)


class ExpenseOrderModelForm(forms.ModelForm):
    trip_order = forms.ModelChoiceField(
        models.TripOrder.objects.all(), label='Командировъчна заповед', empty_label='Избери')

    class Meta:
        model = models.ExpenseOrder
        exclude = ('creator',)
        widgets = {
            'BGN_amount': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Сума в лева'}),
            'EUR_amount': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Сума в евро'}),
        }


class CourseInvoiceModelForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        models.Course.objects.all(), label='Курс', empty_label='Избери')
    tax_transaction_basis = forms.ModelChoiceField(
        models.TaxTransactionBasis.objects.all(), label='Основание на сделката', empty_label='Избери')

    class Meta:
        model = models.CourseInvoice
        exclude = ('creator',)
        widgets = {
            'additional_information': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Допълнителна информация'})
        }


class CompanyModelForm(forms.ModelForm):
    class Meta:
        model = models.Company
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Име'}),
            'bulstat': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Булстат'}),
            'mol': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'МОЛ'}),
            'city': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Град'}),
            'postal_code': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Пощенски код'}),
            'province': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Област'}),
            'address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Адрес'}),
            'correspondence_address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Адрес за кореспонденция'}),
            'phone_number': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Телефонен номер'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'E-mail'})
        }


class BankModelForm(forms.ModelForm):
    class Meta:
        model = models.Bank
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Име'}),
            'bank_code': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Банков код'}),
            'iban': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'IBAN'})
        }


class InstructionModelForm(forms.ModelForm):
    driver = forms.ModelChoiceField(
        get_user_model().objects.filter(is_active=True, is_staff=False), label='Шорфьор', empty_label='Избери')
    car = forms.ModelChoiceField(
        models.Car.objects.all(), label='Автомобил', empty_label='Избери')
    company = forms.ModelChoiceField(
        models.Company.objects.all(), label='Фирма', empty_label='Избери')

    class Meta:
        model = models.Instruction
        exclude = ('creator',)
        widgets = {
            'city': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Град'})
        }


class CourseDateJournalForm(forms.Form):
    company = forms.ModelChoiceField(
        models.Company.objects.all(), label='Фирма', empty_label='Избери')
    from_date = forms.DateField(label='От дата', input_formats=DATE_FORMATS, widget=forms.TextInput(
        attrs={'class': 'form-control date-picker', 'placeholder': 'От дата'}))
    to_date = forms.DateField(label='До дата', input_formats=DATE_FORMATS, widget=forms.TextInput(
        attrs={'class': 'form-control date-picker', 'placeholder': 'До дата'}))
    journal_type = forms.ChoiceField(
        label='Вид дневник', choices=models.COURSE_DOCUMENT_TYPE_CHOICES)
