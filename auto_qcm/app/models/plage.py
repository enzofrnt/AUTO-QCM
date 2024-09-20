from django.db import models

class Plage(models.Model):
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    