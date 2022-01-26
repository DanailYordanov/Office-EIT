from django.db import models
from django.conf import settings
from django.shortcuts import reverse


CLIENT_TYPE_CHOICES = [
    ('', 'Избери'),
    ('Български', 'Български'),
    ('Чуждестранен', 'Чуждестранен')
]

CHARGING_VAT_CHOICES = [
    ('', 'Избери'),
    ('чл.21 ал.2 от ЗДДС', 'чл.21 ал.2 от ЗДДС'),
    ('чл. 30, ал.1 от ЗДДС', 'чл. 30, ал.1 от ЗДДС')
]

CURRENCY_CHOICES = [
    ('', 'Избери'),
    ('BGN', 'BGN'),
    ('EUR', 'EUR'),
    ('USD', 'USD'),
    ('GBP', 'GBP'),
    ('CAD', 'CAD')
]

LOADING_TYPE_CHOICES = [
    ('', 'Избери'),
    ('loading_address', 'Адрес на товарене'),
    ('unloading_address', 'Адрес на разтоварване')
]

PAYMENT_TYPE_CHOICES = [
    ('', 'Избери'),
    ('Кеш', 'Кеш'),
    ('Дебитна карта', 'Дебитна карта'),
    ('Кредитна карта', 'Кредитна карта'),
    ('Банков превод', 'Банков превод')
]


MEASURE_TYPE_CHOICES = [
    ('', 'Избери'),
    ('Тон', 'Тон'),
    ('Курс', 'Курс'),
    ('Брой', 'Брой'),
    ('Километър', 'Километър')
]


INVOICE_TYPE_CHOICES = [
    ('', 'Избери'),
    ('Фактура', 'Фактура'),
    ('Кредитно известие', 'Кредитно известие'),
    ('Дебитно известие', 'Дебитно известие')
]


TAX_TYPE_CHOICES = [
    ('', 'Избери'),
    ('Стандартна фактура', 'Стандартна фактура'),
    ('Фактура без начисление на ДДС', 'Фактура без начисление на ДДС')
]


class CarType(models.Model):
    car_type = models.CharField('Вид автомобил', max_length=50)

    def __str__(self):
        return self.car_type


class Car(models.Model):
    car_type = models.ForeignKey(
        CarType, verbose_name='Вид автомобил', null=True, on_delete=models.SET_NULL)
    number_plate = models.CharField('Регистрационен номер', max_length=50)
    brand = models.CharField('Марка', max_length=50)

    def __str__(self):
        return f'{self.brand} - {self.number_plate}'


class ReminderType(models.Model):
    reminder_type = models.CharField('Вид напомняне', max_length=50)

    def __str__(self):
        return self.reminder_type


class Reminder(models.Model):
    car = models.ForeignKey(
        Car, verbose_name='Автомобил', on_delete=models.CASCADE)
    reminder_type = models.ForeignKey(
        ReminderType, verbose_name='Вид напомняне', null=True, on_delete=models.SET_NULL)
    expiration_date = models.DateField('Дата на изтичнане')

    def __str__(self):
        return f'{self.car.number_plate} - {self.reminder_type.reminder_type}'


class ServiceType(models.Model):
    service_type = models.CharField('Вид обслужване', max_length=100)

    def __str__(self):
        return self.service_type


class Service(models.Model):
    car = models.ForeignKey(
        Car, verbose_name='Автомобил', on_delete=models.CASCADE)
    service_type = models.ForeignKey(
        ServiceType, verbose_name='Вид обслужване', null=True, on_delete=models.SET_NULL)
    additional_information = models.CharField(
        'Допълнителна информация', max_length=500, null=True, blank=True)
    run = models.CharField('Пробег', max_length=20)
    date = models.DateField('Дата')

    def __str__(self):
        return f'{self.car.brand} - {self.car.number_plate} - {self.service_type}'


class Contractor(models.Model):
    client_type = models.CharField(
        'Тип клиент', max_length=100, choices=CLIENT_TYPE_CHOICES)
    name = models.CharField('Име', max_length=100)
    bulstat = models.CharField(
        'Булстат', max_length=100, null=True, blank=True)
    mol = models.CharField('МОЛ', max_length=100, null=True, blank=True)
    country = models.CharField(
        'Държава', max_length=100, null=True, blank=True)
    city = models.CharField('Град', max_length=100, null=True, blank=True)
    address = models.CharField('Адрес', max_length=100, null=True, blank=True)
    correspondence_address = models.CharField(
        'Адрес за кореспонденция', max_length=100, null=True, blank=True)
    phone_number = models.CharField(
        'Телефонен номер', max_length=100, null=True, blank=True)
    email = models.CharField('E-mail', max_length=100, null=True, blank=True)
    maturity_date = models.CharField(
        'Дата на падеж', max_length=50, null=True, blank=True)
    charging_vat = models.CharField('Основание за неначисление на ДДС',
                                    max_length=100, choices=CHARGING_VAT_CHOICES, null=True, blank=True)
    cmr_photo = models.FileField(
        'Прикачи ЧМР', upload_to='cmr_photos', null=True, blank=True)
    license_photo = models.FileField(
        'Прикачи лиценз или друг документ', upload_to='license_photos', null=True, blank=True)
    expiration_date = models.DateField(
        'Дата на изтичане', null=True, blank=True)

    def __str__(self):
        return self.name


class Bank(models.Model):
    name = models.CharField('Име', max_length=50)
    bank_code = models.CharField(
        'Банков код', max_length=50, null=True, blank=True)
    iban = models.CharField('IBAN', max_length=50)

    def __str__(self):
        return f'{self.name} - {self.bank_code} - {self.iban}'


class Company(models.Model):
    name = models.CharField('Име', max_length=100)
    bulstat = models.CharField(
        'Булстат', max_length=100, null=True, blank=True)
    mol = models.CharField('МОЛ', max_length=100, null=True, blank=True)
    city = models.CharField('Град', max_length=100, null=True, blank=True)
    address = models.CharField('Адрес', max_length=100, null=True, blank=True)
    correspondence_address = models.CharField(
        'Адрес за кореспонденция', max_length=100, null=True, blank=True)
    phone_number = models.CharField(
        'Телефонен номер', max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class TaxTransactionBasis(models.Model):
    name = models.CharField('Име', max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Шофьор', null=True, on_delete=models.SET_NULL)
    car = models.ForeignKey(
        Car, verbose_name='Автомобил', null=True, on_delete=models.SET_NULL)
    company = models.ForeignKey(
        Company, verbose_name='Фирма', null=True, on_delete=models.SET_NULL)
    contractor = models.ForeignKey(
        Contractor, verbose_name='Контрагент', null=True, on_delete=models.SET_NULL)
    bank = models.ForeignKey(Bank, verbose_name='Банка',
                             null=True, on_delete=models.SET_NULL)
    request_number = models.CharField(
        'Номер на заявка', max_length=50, null=True, blank=True)
    from_to = models.CharField('Релация', max_length=100)
    description = models.CharField(
        'Описание', max_length=1000, null=True, blank=True)
    price = models.FloatField('Цена')
    currency = models.CharField(
        'Валута', choices=CURRENCY_CHOICES, max_length=5)
    cargo_type = models.CharField('Вид и тегло на товара', max_length=100)
    contact_person = models.CharField(
        'Лице за контакт', max_length=50, null=True, blank=True)
    other_conditions = models.CharField(
        'Други условия', max_length=1000, null=True, blank=True)
    create_date = models.DateField('Дата на създаване', auto_now_add=True)

    def __str__(self):
        return f'№{self.pk} - {self.driver} - {self.contractor} - {self.from_to}'

    def get_absolute_url(self):
        return reverse('main:course-information', kwargs={
            'pk': self.id,
        })


class Address(models.Model):
    address = models.CharField('Адрес', max_length=200)
    contact_person = models.CharField(
        'Лице за контакт', max_length=50, null=True, blank=True)
    contact_phone = models.CharField(
        'Телефон за връзка', max_length=30, null=True, blank=True)
    gps_coordinates = models.CharField(
        'GPS координати', max_length=100, null=True, blank=True)

    def __str__(self):
        return self.address


class CourseAddress(models.Model):
    course = models.ForeignKey(
        Course, verbose_name='Курс', on_delete=models.CASCADE)
    address_obj = models.ForeignKey(
        Address, verbose_name='Свързан адрес', null=True, blank=True, on_delete=models.SET_NULL)
    address_input = models.CharField(
        'Въведен адрес', max_length=200, null=True, blank=True)
    load_type = models.CharField('Вид на товарене',
                                 choices=LOADING_TYPE_CHOICES, max_length=30)
    date = models.DateField('Дата', null=True, blank=True)

    def __str__(self):
        return f'{self.course} - {self.address_input} - {self.date}'


class ExpenseType(models.Model):
    expense_type = models.CharField('Вид разход', max_length=50)

    def __str__(self):
        return self.expense_type


class Expense(models.Model):
    course = models.ForeignKey(
        Course, verbose_name='Курс', on_delete=models.CASCADE)
    expense_type = models.ForeignKey(
        ExpenseType, verbose_name='Вид разход', on_delete=models.CASCADE)
    price = models.FloatField('Цена')
    currency = models.CharField(
        'Валута', choices=CURRENCY_CHOICES, max_length=5)
    payment_type = models.CharField(
        'Вид плащане', max_length=50, choices=PAYMENT_TYPE_CHOICES)
    additional_information = models.CharField(
        'Допълнителна информация', max_length=500, null=True, blank=True)

    def __str__(self):
        return f'{self.course} - {self.expense_type} - {self.price}'


class TripOrder(models.Model):
    course = models.ForeignKey(
        Course, verbose_name='Курс', null=True, on_delete=models.SET_NULL)
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Шофьор', null=True, on_delete=models.SET_NULL)
    destination = models.CharField('Дестинация', max_length=100)
    from_date = models.DateField('Начална дата')
    to_date = models.DateField('Крайна дата')
    creation_date = models.DateField('Дата на създаване', auto_now_add=True)

    def __str__(self):
        return f'Командировъчна заповед № - {self.id}'


class ExpenseOrder(models.Model):
    trip_order = models.ForeignKey(
        TripOrder, verbose_name='Командировъчна заповед', null=True, on_delete=models.SET_NULL)
    BGN_amount = models.FloatField('Сума в лева', null=True, blank=True)
    EUR_amount = models.FloatField('Сума в евро', null=True, blank=True)
    creation_date = models.DateField('Дата на създаване', auto_now_add=True)

    def __str__(self):
        return f'Разходен ордер № - {self.id}'


class CourseInvoice(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Създател', null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(
        Course, verbose_name='Курс', null=True, on_delete=models.SET_NULL)
    payment_type = models.CharField(
        'Вид плащане', max_length=50, choices=PAYMENT_TYPE_CHOICES)
    measure_type = models.CharField(
        'Мярка', max_length=15, choices=MEASURE_TYPE_CHOICES)
    invoice_type = models.CharField(
        'Вид документ', max_length=30, choices=INVOICE_TYPE_CHOICES)
    tax_type = models.CharField(
        'ДДС', max_length=30, choices=TAX_TYPE_CHOICES)
    tax_transaction_basis = models.ForeignKey(
        TaxTransactionBasis, verbose_name='Основане на сделка', null=True, on_delete=models.SET_NULL)
    quantity = models.FloatField('Количество')
    price = models.FloatField('Цена')
    additional_information = models.CharField(
        'Допълнителна информация', max_length=500, null=True, blank=True)
    creation_date = models.DateField('Дата на създаване', auto_now_add=True)

    def __str__(self):
        return f'Фактура за курс № - {self.id}'
