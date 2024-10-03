from django.contrib.auth.models import AbstractUser
from django.db import models


class AdminCreationFlag(models.Model):
    flag = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.flag


class Utilisateur(AbstractUser):
    must_change_password = models.BooleanField(default=False)

    @property
    def is_tutor(self):
        return self.groups.filter(name="Enseignant").exists()

    @property
    def is_student(self):
        return self.groups.filter(name="Etudiant").exists()

    @property
    def is_admin(self):
        return self.groups.filter(name="Admin").exists()

    @property
    def promotion(self):
        if self.groups.filter(name__startswith="BUT").count() != 1:
            return "Erreur"
        return self.groups.filter(name__startswith="BUT").first()

    @property
    def groupe(self):
        if self.groups.filter(name__startswith="1").count() != 1:
            if self.groups.filter(name__startswith="2").count() != 1:
                if self.groups.filter(name__startswith="3").count() != 1:
                    return "Erreur"
                return self.groups.filter(name__startswith="3").first()
            return self.groups.filter(name__startswith="2").first()
        return self.groups.filter(name__startswith="1").first()

    def __str__(self):
        return f"{self.username} - {self.is_tutor}"
