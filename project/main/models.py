from django.db import models


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


class Car(models.Model):
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
        ReminderType, verbose_name='Вид напомняне', on_delete=models.CASCADE)
    expiration_date = models.DateField('Дата на изтичнане')

    def __str__(self):
        return f'{self.car.number_plate} - {self.reminder_type.reminder_type}'


class Service(models.Model):
    car = models.ForeignKey(
        Car, verbose_name='Автомобил', on_delete=models.CASCADE)
    date = models.DateField('Дата')
    service_type = models.CharField('Вид обслужване', max_length=200)
    additional_information = models.CharField(
        'Допълнителна информация', max_length=500, null=True, blank=True)
    run = models.CharField('Пробег', max_length=30)

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
