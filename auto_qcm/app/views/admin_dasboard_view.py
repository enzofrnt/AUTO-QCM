from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render


# Fonction pour vérifier si l'utilisateur est un superutilisateur
def is_superuser(user):
    return user.is_superuser


# Vue admin personnalisée
@user_passes_test(is_superuser)
def custom_admin_view(request):
    # Exemple pour afficher tous les objets d'un modèle
    if request.method == "POST":
        # Si tu veux ajouter la possibilité de modifier ou supprimer des objets
        pass

    return render(request, "admin.html")
