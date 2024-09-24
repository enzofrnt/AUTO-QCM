from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group


class Plage(models.Model):
    debut = models.DateTimeField()
    fin = models.DateTimeField()
    promo = models.ForeignKey(Group, related_name="promos", on_delete=models.CASCADE)
    groupe = models.ForeignKey(Group, related_name="groupes", on_delete=models.CASCADE)

    def clean(self):
        # Valider que la date de début est bien avant la date de fin
        if self.debut >= self.fin:
            raise ValidationError(
                "La date de début doit être antérieure à la date de fin."
            )

    def __str__(self):
        return f"{self.promo.name} - {self.groupe.name} ({self.debut} à {self.fin})"
