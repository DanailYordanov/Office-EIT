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