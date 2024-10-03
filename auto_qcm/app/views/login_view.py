from logging import getLogger

from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

logger = getLogger(__name__)


class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = reverse_lazy("home")  # Redirection après login

    def form_valid(self, form):
        """Gérer les actions supplémentaires après un login réussi."""
        # Déconnecter l'utilisateur actuel s'il existe
        if self.request.user.is_authenticated:
            logout(self.request)

        # Connexion du nouvel utilisateur
        user = form.get_user()
        logger.info(f"Utilisateur connecté: {user.username}")
        login(self.request, user)

        # Vérifier si l'utilisateur doit changer son mot de passe
        if user.must_change_password:
            logger.info(f"Utilisateur {user.username} doit changer son mot de passe.")
            return redirect(
                "password_change"
            )  # Redirection vers la page de changement de mot de passe

        return super().form_valid(form)

    def form_invalid(self, form):
        """Gérer les erreurs lors de la validation du formulaire."""
        messages.error(self.request, "Nom d'utilisateur ou mot de passe incorrect.")
        logger.warning("Échec de la tentative de connexion.")
        return super().form_invalid(form)
