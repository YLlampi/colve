"""
from django.db import models
from django.contrib.auth.models import User

from .managers import UserProfileManager


# Create your models here.

class UserProfile(models.Model):
    # user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    first_name = models.CharField('Nombres', max_length=150, null=True)
    last_name = models.CharField('Apellidos', max_length=150, null=True)

    id_veterinarian = models.CharField('ID Veterinario', max_length=9, null=True, unique=True)

    pagado_hasta_month = models.PositiveSmallIntegerField(null=True, default=0)
    pagado_hasta_year = models.PositiveSmallIntegerField(null=True, default=0)

    activo_hasta_month = models.PositiveSmallIntegerField(null=True, default=0)
    activo_hasta_year = models.PositiveSmallIntegerField(null=True, default=0)

    es_activo = models.BooleanField(default=True)

    objects = UserProfileManager()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.id} - {self.first_name} {self.last_name}'
"""