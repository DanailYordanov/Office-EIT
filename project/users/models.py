from django.db import models
from django.urls import reverse
from django.core.cache import cache
from django.contrib.auth.models import AbstractUser
from main.models import Bank


class CustomUser(AbstractUser):
    middle_name = models.CharField(
        'Презиме', max_length=150, null=True, blank=True)
    personal_id = models.CharField('ЕГН', max_length=15, null=True, blank=True)
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
    bank = models.ForeignKey(Bank, verbose_name='Банка',
                             null=True, blank=True, on_delete=models.SET_NULL)
    debit_card_number = models.IntegerField(
        'Номер на дебитна карта', null=True, blank=True)
    phone_number = models.CharField(
        'Телефонен номер', max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = 'Потребител'
        verbose_name_plural = 'Потребители'
        ordering = ['first_name', 'middle_name', 'last_name']

    def __str__(self):
        if self.middle_name:
            return f'{self.first_name} {self.middle_name} {self.last_name}'
        else:
            return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete('drivers_notifications')

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        cache.delete('drivers_notifications')

    def get_absolute_url(self):
        return reverse('profile-details', kwargs={
            'pk': self.id
        })

    def get_full_name(self):
        if self.middle_name:
            full_name = '%s %s %s' % (
                self.first_name, self.middle_name, self.last_name)
        else:
            full_name = '%s %s' % (
                self.first_name, self.last_name)

        return full_name.strip()
