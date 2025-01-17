from app.decorators import admin_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.urls import reverse_lazy


# Fonction pour vérifier si l'utilisateur est un superutilisateur
def is_superuser(user):
    return user.is_superuser


# Vue admin personnalisée
@login_required(login_url=reverse_lazy("login"))
@admin_required
@user_passes_test(is_superuser)
def custom_admin_view(request):
    # Exemple pour afficher tous les objets d'un modèle
    if request.method == "POST":
        # Si tu veux ajouter la possibilité de modifier ou supprimer des objets
        pass

    return render(request, "admin.html")
