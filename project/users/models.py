from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    id_card_expiration = models.DateField(null=True)
    drivers_license_expiration = models.DateField(null=True)
    professional_competence = models.DateField(null=True)
    adr_expiration = models.DateField(null=True)
    digital_card_expiration = models.DateField(null=True)
    psychological_test_expiration = models.DateField(null=True)
    pasport_expiration = models.DateField(null=True)
