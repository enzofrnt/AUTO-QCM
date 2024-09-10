from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import logout
from logging import getLogger

logger = getLogger(__name__)

class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'login/login.html'
    success_url = reverse_lazy('home')  # Redirection après login

    def form_valid(self, form):
        """Gérer les actions supplémentaires après un login réussi."""
        # Déconnecter l'utilisateur actuel s'il existe
        if self.request.user.is_authenticated:
            logout(self.request)
        
        # Connexion du nouvel utilisateur
        user = form.get_user()
        logger.info(f"Utilisateur connecté: {user.username}")
        return super().form_valid(form)

    def form_invalid(self, form):
        """Gérer les erreurs lors de la validation du formulaire."""
        messages.error(self.request, "Nom d'utilisateur ou mot de passe incorrect.")
        logger.warning("Échec de la tentative de connexion.")
        return super().form_invalid(form)

    def get_success_url(self):
        """Redirection vers l'URL de succès ou page précédente."""
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            return self.success_url
