from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.forms import PasswordChangeForm
from app.models import Utilisateur


class ChangePasswordViewTest(TestCase):
    def setUp(self):
        """Initialise un client et un utilisateur pour les tests."""
        self.client = Client()
        self.user = Utilisateur.objects.create_user(
            username="testuser", email="testuser@example.com", password="oldpassword"
        )
        self.client.login(username="testuser", password="oldpassword")

    def test_change_password_view_not_logged_in(self):
        """Teste que l'utilisateur est redirigé vers la page de connexion lorsqu'il n'est pas connecté."""
        self.client.logout()
        response = self.client.get(reverse("password_change"))
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('password_change')}"
        )

    def test_change_password_valid(self):
        """Teste le changement de mot de passe avec succès."""
        response = self.client.post(
            reverse("password_change"),
            {
                "old_password": "oldpassword",
                "new_password1": "newpassword123",
                "new_password2": "newpassword123",
            },
        )
        # Vérifie que l'utilisateur est redirigé vers la page d'accueil
        self.assertRedirects(response, reverse("home"))

        # Vérifie que l'utilisateur peut se reconnecter avec le nouveau mot de passe
        self.client.logout()
        self.assertTrue(
            self.client.login(username="testuser", password="newpassword123")
        )

        # Vérifie que le message de succès a été ajouté
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), "Votre mot de passe a été changé avec succès."
        )

    def test_change_password_invalid(self):
        """Teste le changement de mot de passe avec des données invalides."""
        response = self.client.post(
            reverse("password_change"),
            {
                "old_password": "wrongpassword",  # Mot de passe incorrect
                "new_password1": "newpassword123",
                "new_password2": "newpassword123",
            },
        )
        # Vérifie que le formulaire est rendu à nouveau avec des erreurs
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "login.html"
        )  # Vérifie que le bon template est utilisé
        self.assertContains(
            response, "Veuillez corriger les erreurs ci-dessous."
        )  # Vérifie la présence du message d'erreur
