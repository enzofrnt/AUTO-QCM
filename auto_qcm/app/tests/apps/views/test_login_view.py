from django.test import TestCase
from django.urls import reverse
from app.models import (
    Utilisateur,
)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages import get_messages
import logging


class CustomLoginViewTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Désactiver la journalisation pour les tests si vous le souhaitez
        logging.disable(
            logging.CRITICAL
        )  # Désactive tous les logs de niveau CRITICAL et inférieurs

    @classmethod
    def tearDownClass(cls):
        # Réactiver la journalisation après les tests
        logging.disable(logging.NOTSET)  # Réactive les logs
        super().tearDownClass()

    def setUp(self):
        # Création d'un utilisateur pour les tests
        self.utilisateur = Utilisateur.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )

    def test_login_success(self):
        """Test de connexion réussie avec redirection vers la page d'accueil."""
        response = self.client.post(
            reverse("login"),
            data={"username": "testuser", "password": "password123"},
        )

        # Vérification que l'utilisateur est redirigé après la connexion réussie
        self.assertRedirects(response, reverse("home"))

        # Vérification que l'utilisateur est connecté
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_invalid_credentials(self):
        """Test de connexion échouée avec des identifiants incorrects."""
        response = self.client.post(
            reverse("login"),
            data={"username": "wronguser", "password": "wrongpassword"},
        )

        # Vérification que l'utilisateur n'est pas redirigé (échec)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

        # Vérification que l'utilisateur n'est pas connecté
        self.assertFalse(response.wsgi_request.user.is_authenticated)

        # Vérification du message d'erreur
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), "Nom d'utilisateur ou mot de passe incorrect."
        )

    def test_login_redirect_to_password_change(self):
        """Test de redirection vers la page de changement de mot de passe si nécessaire."""
        # Marquer l'utilisateur comme devant changer son mot de passe
        self.utilisateur.must_change_password = True
        self.utilisateur.save()

        response = self.client.post(
            reverse("login"),
            data={"username": "testuser", "password": "password123"},
        )

        # Vérification de la redirection vers la page de changement de mot de passe
        self.assertRedirects(response, reverse("password_change"))

        # Vérification que l'utilisateur est connecté
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_when_already_authenticated(self):
        """Test la déconnexion de l'utilisateur actuel s'il est déjà authentifié."""
        # Connecter initialement un utilisateur
        self.client.login(username="testuser", password="password123")

        # Création d'un autre utilisateur pour le test
        other_user = Utilisateur.objects.create_user(
            username="otheruser", email="other@example.com", password="otherpassword"
        )

        # Tenter de se connecter en tant qu'un autre utilisateur
        response = self.client.post(
            reverse("login"),
            data={"username": "otheruser", "password": "otherpassword"},
        )

        # Vérification que l'ancien utilisateur est déconnecté et le nouveau connecté
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user.username, "otheruser")

        # Vérification de la redirection après la connexion
        self.assertRedirects(response, reverse("home"))

    def test_form_invalid(self):
        """Test la gestion des erreurs de validation du formulaire."""
        form = AuthenticationForm(data={"username": "", "password": ""})
        self.assertFalse(form.is_valid())

        response = self.client.post(
            reverse("login"), data={"username": "", "password": ""}
        )

        # Vérification du message d'erreur
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), "Nom d'utilisateur ou mot de passe incorrect."
        )

        # Vérification de l'affichage du template avec le formulaire invalide
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
