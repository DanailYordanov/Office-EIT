from django.db import models


class Car(models.Model):
    number_plate = models.CharField('Регистрационен номер', max_length=50)
    brand = models.CharField('Марка', max_length=50)

    def __str__(self):
        return f'{self.brand} - {self.number_plate}'


class ReminderType(models.Model):
    reminder_type = models.CharField(max_length=50)

    def __str__(self):
        return self.reminder_type


class Reminder(models.Model):
    reminder_type = models.ForeignKey(ReminderType, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    expiration_date = models.DateField()

    def __str__(self):
        return f'{self.car.number_plate} - {self.reminder_type.reminder_type}'


class Service(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    date = models.DateField()
    service_type = models.CharField(max_length=200)
    additional_information = models.CharField(max_length=500)
    run = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.car.brand} - {self.car.number_plate} - {self.service_type}'


class Contractors(models.Model):
    client_type = models.CharField(max_length=100)
    bulstat = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    mol = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    charging_vat = models.CharField(max_length=100)
    cmr_photo = models.FileField(upload_to='cmr_photos')
    license_photo = models.FileField(upload_to='license_photos')
