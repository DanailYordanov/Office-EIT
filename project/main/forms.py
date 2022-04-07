from django import forms
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.forms.models import ModelChoiceIterator
from django_select2 import forms as s2forms
from main import models


DATE_FORMATS = ['%d-%m-%Y', '%d/%m/%Y', '%d/%m/%y', '%Y/%m/%d', '%Y-%m-%d']

COURSE_DOCUMENTS_OPTIONS = [
    ('', 'Избери'),
    ('Писмо', 'Писмо'),
    ('Обратна разписка', 'Обратна разписка'),
    ('Служебни бележки', 'Служебни бележки')
]


class CustomSelectTagWidget(s2forms.ModelSelect2TagWidget):
    def __init__(self, *args, **kwargs):
        self.field_name = kwargs.pop('field_name', None)
        super().__init__(*args, **kwargs)

    def build_attrs(self, base_attrs, extra_attrs=None):
        base_attrs.update({
            'data-theme': 'bootstrap-5',
            'data-token-separators': [],
            'data-minimum-input-length': 0,
            'class': 'select-tag form-control'
        })
        return super().build_attrs(base_attrs, extra_attrs)

    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)

        if value:
            value = value[0]
            queryset = self.get_queryset()

            try:
                obj = queryset.get(**{self.field_name: value})
            except (ValueError, TypeError, queryset.model.DoesNotExist):
                obj = queryset.create(**{self.field_name: value})

            return getattr(obj, self.field_name)

        return None

    def optgroups(self, name, value, attrs=None):
        """ 
        While editing an existing object the 'value' variable is the object's id, not the to_field_name
        So that's why the field inital value should be replaced in the form's init method 
        """

        default = (None, [], 0)
        groups = [default]
        has_selected = False
        selected_choices = {str(v) for v in value}

        if not self.is_required and not self.allow_multiple_selected:
            default[1].append(self.create_option(name, "", "", False, 0))

        if not isinstance(self.choices, ModelChoiceIterator):
            return super().optgroups(name, value, attrs=attrs)

        selected_choices = {
            c for c in selected_choices if c not in self.choices.field.empty_values
        }

        query = Q(**{"%s__in" % self.field_name: selected_choices})

        for obj in self.choices.queryset.filter(query):
            option_value = self.choices.choice(obj)[0]
            option_label = self.label_from_instance(obj)

            selected = str(option_value) in value and (
                has_selected is False or self.allow_multiple_selected
            )
            if selected is True and has_selected is False:
                has_selected = True
            index = len(default[1])
            subgroup = default[1]
            subgroup.append(
                self.create_option(
                    name, option_value, option_label, selected_choices, index
                )
            )

        return groups


class CustomModelSelectWidget(s2forms.ModelSelect2Widget):
    def build_attrs(self, base_attrs, extra_attrs=None):
        base_attrs.update({
            'class': 'form-control',
            'data-theme': 'bootstrap-5',
            'data-minimum-input-length': 0
        })
        return super().build_attrs(base_attrs, extra_attrs)


class CustomSelectWidget(s2forms.Select2Widget):
    def build_attrs(self, base_attrs, extra_attrs=None):
        base_attrs.update({
            'class': 'form-control',
            'data-theme': 'bootstrap-5'
        })
        return super().build_attrs(base_attrs, extra_attrs)


class CarModelForm(forms.ModelForm):
    class Meta:
        model = models.Car
        fields = '__all__'
        widgets = {
            'car_type': CustomSelectTagWidget(
                model=models.CarType,
                field_name='car_type',
                search_fields=['car_type__icontains'],
                data_url=reverse_lazy('main:tag-auto-select-options',
                                      args=('car_type',))
            ),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Марка'}),
            'number_plate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Регистрационен номер'}),
            'vin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер на рама'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['car_type'].to_field_name = 'car_type'

        if self.instance.pk:
            if hasattr(self.instance.car_type, 'car_type'):
                self.initial['car_type'] = self.instance.car_type.car_type


class ReminderModelForm(forms.ModelForm):
    class Meta:
        model = models.Reminder
        fields = '__all__'
        widgets = {
            'reminder_type': CustomSelectTagWidget(
                model=models.ReminderType,
                field_name='reminder_type',
                search_fields=['reminder_type__icontains'],
                data_url=reverse_lazy('main:tag-auto-select-options',
                                      args=('reminder_type',))
            ),
            'car': CustomModelSelectWidget(
                model=models.Car,
                search_fields=['brand__icontains', 'number_plate__icontains']
            ),
            'expiration_date': forms.DateInput(
                attrs={'class': 'form-control date-picker', 'placeholder': 'Дата на изтичане'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['reminder_type'].to_field_name = 'reminder_type'

        if self.instance.pk:
            if hasattr(self.instance.reminder_type, 'reminder_type'):
                self.initial['reminder_type'] = self.instance.reminder_type.reminder_type


class ServiceModelForm(forms.ModelForm):
    class Meta:
        model = models.Service
        fields = '__all__'
        widgets = {
            'car': CustomModelSelectWidget(
                model=models.Car,
                search_fields=['brand__icontains', 'number_plate__icontains']
            ),
            'service_type': CustomSelectTagWidget(
                model=models.ServiceType,
                field_name='service_type',
                search_fields=['service_type__icontains'],
                data_url=reverse_lazy('main:tag-auto-select-options',
                                      args=('service_type',))
            ),
            'run': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Пробег'}),
            'date': forms.DateInput(
                attrs={'class': 'form-control date-picker', 'placeholder': 'Дата на изтичане'}),
            'additional_information': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Допълнителна информация'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['service_type'].to_field_name = 'service_type'

        if self.instance.pk:
            if hasattr(self.instance.service_type, 'service_type'):
                self.initial['service_type'] = self.instance.service_type.service_type


class ContractorsModelForm(forms.ModelForm):
    class Meta:
        model = models.Contractor
        fields = '__all__'
        widgets = {
            'client_type': CustomSelectWidget(choices=models.CLIENT_TYPE_CHOICES),

            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Име'}),
            'bulstat': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Булстат',
                    'data-populate-vat-info-url': reverse_lazy('main:populate-vat-info')
                }),
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
            'cmr_expiration_date': forms.DateInput(
                attrs={'class': 'form-control date-picker', 'placeholder': 'Дата на изтичане'}),
            'license_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'license_expiration_date': forms.DateInput(
                attrs={'class': 'form-control date-picker', 'placeholder': 'Дата на изтичане'})
        }


class CourseModelForm(forms.ModelForm):
    medical_examination_perpetrator = forms.ModelChoiceField(
        models.MedicalExaminationPerpetrator.objects.all(),
        to_field_name='perpetrator',
        widget=CustomSelectTagWidget(
            model=models.MedicalExaminationPerpetrator,
            field_name='perpetrator',
            search_fields=['perpetrator__icontains'],
            data_url=reverse_lazy('main:tag-auto-select-options',
                                  args=('perpetrator',))
        ))

    technical_inspection_perpetrator = forms.ModelChoiceField(
        models.TechnicalInspectionPerpetrator.objects.all(),
        to_field_name='perpetrator',
        widget=CustomSelectTagWidget(
            model=models.TechnicalInspectionPerpetrator,
            field_name='perpetrator',
            search_fields=['perpetrator__icontains'],
            data_url=reverse_lazy('main:tag-auto-select-options',
                                  args=('perpetrator',))
        ))

    class Meta:
        model = models.Course
        exclude = ('number', 'create_date')
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание'}),
            'course_price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Цена за курс'}),
            'driver_salary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Цена за командировка'}),
            'cargo_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Вид и тегло на товара'}),
            'export': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'mileage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Километраж'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Лице за контакт'}),
            'other_conditions': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Други условия'}),

            'driver': CustomModelSelectWidget(
                model=get_user_model(),
                queryset=get_user_model().objects.filter(
                    is_active=True, is_staff=False).order_by('first_name'),
                search_fields=['first_name__icontains']
            ),

            'car': CustomModelSelectWidget(
                model=models.Car,
                search_fields=['brand__icontains', 'number_plate__icontains']
            ),

            'company': CustomModelSelectWidget(
                model=models.Company,
                search_fields=['name__icontains'],
            ),

            'contractor': CustomModelSelectWidget(
                model=models.Contractor,
                search_fields=['name__icontains'],
                attrs={
                    'id': 'contractorID',
                    'data-load-contractor-reminder-url': reverse_lazy('main:load-contractor-reminder')
                },
            ),

            'bank': CustomModelSelectWidget(
                model=models.Bank,
                search_fields=['name__icontains',
                               'bank_code__icontains', 'iban__icontains']
            ),

            'request_number': CustomSelectTagWidget(
                model=models.RequestNumber,
                field_name='request_number',
                search_fields=['request_number__icontains'],
                data_url=reverse_lazy('main:tag-auto-select-options',
                                      args=('request_number',))
            ),

            'from_to': CustomSelectTagWidget(
                model=models.FromTo,
                field_name='from_to',
                search_fields=['from_to__icontains'],
                data_url=reverse_lazy('main:tag-auto-select-options',
                                      args=('from_to',))
            ),

            'cargo_type': CustomSelectTagWidget(
                model=models.CargoType,
                field_name='cargo_type',
                search_fields=['cargo_type__icontains'],
                data_url=reverse_lazy('main:tag-auto-select-options',
                                      args=('cargo_type',))
            ),

            'course_price_currency': CustomSelectWidget(choices=models.CURRENCY_CHOICES),
            'driver_salary_currency': CustomSelectWidget(choices=models.CURRENCY_CHOICES)
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['driver'].queryset = get_user_model().objects.filter(
            is_active=True, is_staff=False).order_by('first_name')

        self.fields['request_number'].to_field_name = 'request_number'
        self.fields['from_to'].to_field_name = 'from_to'
        self.fields['cargo_type'].to_field_name = 'cargo_type'

        if self.instance.pk:
            if self.instance.export:
                if hasattr(self.instance, 'medical_examination'):
                    self.fields['medical_examination_perpetrator'].initial = self.instance.medical_examination.perpetrator.perpetrator

                if hasattr(self.instance, 'technical_inspection'):
                    self.fields['technical_inspection_perpetrator'].initial = self.instance.technical_inspection.perpetrator.perpetrator

            if hasattr(self.instance.request_number, 'request_number'):
                self.initial['request_number'] = self.instance.request_number.request_number

            if hasattr(self.instance.from_to, 'from_to'):
                self.initial['from_to'] = self.instance.from_to.from_to

            if hasattr(self.instance.cargo_type, 'cargo_type'):
                self.initial['cargo_type'] = self.instance.cargo_type.cargo_type

        if self.data and 'export' in self.data:
            self.fields['medical_examination_perpetrator'].required = True
            self.fields['technical_inspection_perpetrator'].required = True
        else:
            self.fields['medical_examination_perpetrator'].required = False
            self.fields['technical_inspection_perpetrator'].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            technical_inspection_perpetrator = self.cleaned_data['technical_inspection_perpetrator']
            medical_examination_perpetrator = self.cleaned_data['medical_examination_perpetrator']

            if not instance.id:
                instance.save()

                models.CourseTechnicalInspection.objects.create(
                    course=instance, perpetrator=technical_inspection_perpetrator)

                models.CourseMedicalExamination.objects.create(
                    course=instance, perpetrator=medical_examination_perpetrator)
            else:
                instance.save()

                course_technical_inspection = models.CourseTechnicalInspection.objects.get(
                    course=instance)
                course_medical_examination = models.CourseMedicalExamination.objects.get(
                    course=instance)

                if self.cleaned_data['export']:
                    if 'technical_inspection_perpetrator' in self.changed_data:
                        course_technical_inspection.perpetrator = self.cleaned_data[
                            'technical_inspection_perpetrator']
                        course_technical_inspection.save()

                    if 'medical_examination_perpetrator' in self.changed_data:
                        course_medical_examination.perpetrator = self.cleaned_data[
                            'medical_examination_perpetrator']
                        course_medical_examination.save()

            self.save_m2m()
        return instance


class CourseAddresModelForm(forms.ModelForm):
    class Meta:
        model = models.CourseAddress
        fields = ['load_type', 'address', 'date']
        widgets = {
            'load_type': CustomSelectWidget(choices=models.LOADING_TYPE_CHOICES),

            'address': CustomSelectTagWidget(
                model=models.Address,
                field_name='address',
                search_fields=['address__icontains'],
                data_url=reverse_lazy('main:tag-auto-select-options',
                                      args=('address',))
            ),

            'date': forms.DateInput(
                attrs={'class': 'form-control date-picker', 'placeholder': 'Дата'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['address'].to_field_name = 'address'
        self.fields['address'].empty_label = 'Избери'

        if self.instance.pk:
            if hasattr(self.instance.address, 'address'):
                self.initial['address'] = self.instance.address.address


class CustomBaseInlineFormSet(forms.BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields['DELETE'].widget = forms.CheckboxInput(
            attrs={'class': 'form-check-input'})


CourseAddressUpdateFormset = forms.inlineformset_factory(models.Course,
                                                         models.CourseAddress, formset=CustomBaseInlineFormSet, form=CourseAddresModelForm, extra=0)

CourseAddressAddFormset = forms.inlineformset_factory(models.Course,
                                                      models.CourseAddress, form=CourseAddresModelForm, can_delete=False, extra=0)


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
    class Meta:
        model = models.Expense
        exclude = ('course',)
        widgets = {
            'expense_type': CustomSelectTagWidget(
                model=models.ExpenseType,
                field_name='expense_type',
                search_fields=['expense_type__icontains'],
                data_url=reverse_lazy('main:tag-auto-select-options',
                                      args=('expense_type',))
            ),
            'price': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Цена'}),
            'currency': CustomSelectWidget(choices=models.CURRENCY_CHOICES),
            'payment_type': CustomSelectWidget(choices=models.PAYMENT_TYPE_CHOICES),
            'additional_information': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Допълнителна информация'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['expense_type'].to_field_name = 'expense_type'

        if self.instance.pk:
            if hasattr(self.instance.expense_type, 'expense_type'):
                self.initial['expense_type'] = self.instance.expense_type.expense_type


class TripOrderModelForm(forms.ModelForm):
    driver = forms.ModelChoiceField(
        get_user_model().objects.filter(
            is_active=True, is_staff=False).order_by('first_name'),
        label='Шофьор',
        empty_label='Избери',
        widget=forms.Select(
            attrs={
                'data-load-courses-url': reverse_lazy('main:load-course-options'),
                'id': 'driverTripOrderID'
            })
    )
    course = forms.ModelChoiceField(
        models.Course.objects.none(),
        label='Курс за износ',
        empty_label='Избери',
        widget=forms.Select(
            attrs={
                'data-load-dates-url': reverse_lazy('main:load-dates'),
                'id': 'courseTripOrderID'
            })
    )

    class Meta:
        model = models.TripOrder
        fields = ['driver', 'course', 'destination', 'from_date', 'to_date']
        widgets = {
            'destination': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Дестинация'}),
            'from_date': forms.DateInput(
                attrs={'class': 'form-control date-picker', 'placeholder': 'Начална дата'}),
            'to_date': forms.DateInput(
                attrs={'class': 'form-control date-picker', 'placeholder': 'Крайна дата'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'driver' in self.data:
            try:
                driver_id = int(self.data.get('driver'))
                self.fields['course'].queryset = models.Course.objects.filter(
                    driver__id=driver_id, export=True)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['course'].queryset = models.Course.objects.filter(
                driver=self.instance.driver, export=True)


class ExpenseOrderModelForm(forms.ModelForm):
    trip_order = forms.ModelChoiceField(
        models.TripOrder.objects.all().order_by('-number'), label='Командировъчна заповед', empty_label='Избери')

    class Meta:
        model = models.ExpenseOrder
        exclude = ('number', 'creator')
        widgets = {
            'BGN_amount': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Сума в лева'}),
            'EUR_amount': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Сума в евро'}),
        }


class CourseInvoiceModelForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        models.Course.objects.all().order_by('-number'), label='Курс', empty_label='Избери')
    tax_transaction_basis = forms.ModelChoiceField(
        models.TaxTransactionBasis.objects.all(), label='Основание на сделката', empty_label='Избери')

    class Meta:
        model = models.CourseInvoice
        exclude = ('number', 'creator')
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
                attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'course_id': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Курс №'}),
            'course_invoice_id': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Фактура №'}),
            'trip_order_id': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Командировъчна заповед №'}),
            'expense_order_id': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Разходен Ордер №'}),
            'instruction_id': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Инструкция №'}),
            'course_technical_inspection_id': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Технически преглед към курс №'}),
            'course_medical_examination_id': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Медицински преглед към курс №'})
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
        get_user_model().objects.filter(is_active=True, is_staff=False).order_by('first_name'), label='Шорфьор', empty_label='Избери')
    car = forms.ModelChoiceField(
        models.Car.objects.all().order_by('brand'), label='Автомобил', empty_label='Избери')
    company = forms.ModelChoiceField(
        models.Company.objects.all().order_by('name'), label='Фирма', empty_label='Избери')

    class Meta:
        model = models.Instruction
        exclude = ('number', 'creator')
        widgets = {
            'city': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Град'})
        }


class CourseDateJournalForm(forms.Form):
    company = forms.ModelChoiceField(
        models.Company.objects.all().order_by('name'), label='Фирма', empty_label='Избери')
    from_date = forms.DateField(label='От дата', input_formats=DATE_FORMATS, widget=forms.DateInput(
        attrs={'class': 'form-control date-picker', 'placeholder': 'От дата'}))
    to_date = forms.DateField(label='До дата', input_formats=DATE_FORMATS, widget=forms.DateInput(
        attrs={'class': 'form-control date-picker', 'placeholder': 'До дата'}))
    journal_type = forms.ChoiceField(
        label='Вид дневник', choices=models.COURSE_DOCUMENT_TYPE_CHOICES)


class CourseDocumentsForm(forms.Form):
    course = forms.ModelChoiceField(
        models.Course.objects.all().order_by('-number'), label='Курс', empty_label='Избери')
    document_type = forms.ChoiceField(
        label='Тип документ', choices=COURSE_DOCUMENTS_OPTIONS)

    def clean(self):
        form_data = self.cleaned_data
        course = form_data.get('course')
        document_type = form_data.get('document_type')

        if document_type == 'Служебни бележки' and not course.export:
            raise forms.ValidationError('Избраният курс е за внос!')

        return form_data
