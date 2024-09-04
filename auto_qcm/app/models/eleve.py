from django.db import models
from django.contrib.auth.models import AbstractUser

class Eleve(AbstractUser):
    class Meta:
        verbose_name = "Élève"
        verbose_name_plural = "Élèves"
    