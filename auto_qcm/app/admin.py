from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app.models import Utilisateur


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_tutor",
        "promotion",
        "groupe",
    )  # Colonnes à afficher
    list_filter = (
        "is_staff",
        "is_superuser",
        "groups",
    )  # Filtres sur le côté
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )  # Champ de recherche
    ordering = ("username",)  # Ordre d'affichage

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Informations personnelles", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Dates importantes", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "email",
                    "first_name",
                    "last_name",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "groups",
                ),
            },
        ),
    )
