from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    id_card_expiration = models.DateField(
        'Изтичане на лична карта', null=True, blank=True)
    drivers_license_expiration = models.DateField(
        'Изтичане на шофьорска книжка', null=True, blank=True)
    professional_competence = models.DateField(
        'Изтичане на професионална компетентност', null=True, blank=True)
    adr_expiration = models.DateField('Изтичане на ADR', null=True, blank=True)
    digital_card_expiration = models.DateField(
        'Изтичане на дигитална карта', null=True, blank=True)
    psychological_test_expiration = models.DateField(
        'Изтичане на психотест', null=True, blank=True)
    pasport_expiration = models.DateField(
        'Изтичане на паспорт', null=True, blank=True)
    debit_card_number = models.IntegerField(
        'Номер на дебитна карта', null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
