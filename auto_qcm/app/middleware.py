import logging
import os

from django.shortcuts import redirect
from django.urls import reverse

logger = logging.getLogger(__name__)


class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Vérifie si l'utilisateur est authentifié et doit changer son mot de passe
        if request.user.is_authenticated and request.user.must_change_password:
            # Si l'utilisateur n'est pas déjà sur la page de changement de mot de passe

            urls = [
                reverse("password_change"),
                reverse("password_change_done"),
                reverse("logout"),
            ]

            # Ajouter une vérification supplémentaire pour les URLs de rechargement dans l'environnement de dev
            if os.environ.get("env", "dev") == "dev":
                logger.error("Environnement de développement")
                if "/__reload__" in request.path:
                    urls.append(request.path)  # Ajout direct de l'URL de reload

            if request.path not in urls:
                logger.error(
                    f"Utilisateur {request.user.username} doit changer son mot de passe."
                )
                return redirect(
                    "password_change"
                )  # Redirige vers la vue de changement de mot de passe

        # Sinon, continuez normalement
        response = self.get_response(request)
        return response
