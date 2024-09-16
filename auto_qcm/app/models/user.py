from django.db import models
from django.contrib.auth.models import User, Group, Permission

class Utilisateur(models.Model):
    USER_TYPES = (
        ('Etudiant', 'Etudiant'),
        ('Enseignant', 'Enseignant'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='Etudiant')

    groups = models.ManyToManyField(
        Group,
        related_name='utilisateur_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='utilisateur_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"
