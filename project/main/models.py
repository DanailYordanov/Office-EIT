from django.db import models
from django.conf import settings


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

    def __str__(self):
        return self.name


class Course(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Шофьор', null=True, on_delete=models.SET_NULL)
    car = models.ForeignKey(
        Car, verbose_name='Автомобил', null=True, on_delete=models.SET_NULL)
    contractor = models.ForeignKey(
        Contractor, verbose_name='Контрагент', null=True, on_delete=models.SET_NULL)
    bank = models.ForeignKey(Bank, verbose_name='Банка',
                             null=True, on_delete=models.SET_NULL)
    from_to = models.CharField('Релация', max_length=100)
    description = models.CharField(
        'Описание', max_length=1000, null=True, blank=True)
    price = models.IntegerField('Цена')
    currency = models.CharField(
        'Валута', choices=CURRENCY_CHOICES, max_length=5)
    cargo_type = models.CharField('Вид и тегло на товара', max_length=100)
    other_conditions = models.CharField(
        'Други условия', max_length=1000, null=True, blank=True)
    create_date = models.DateField('Дата на създаване', auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.contractor} - {self.from_to}'


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
    date = models.DateField('Дата')

    def __str__(self):
        return f'{self.course} - {self.address_input} - {self.date}'
