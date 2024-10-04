from django.test import TestCase, Client
from django.urls import reverse
from app.models import Utilisateur


class CustomAdminViewTest(TestCase):
    def setUp(self):
        """Initialise le client et crée des utilisateurs pour les tests."""
        self.client = Client()

        # Création d'un superutilisateur
        self.superuser = Utilisateur.objects.create_superuser(
            username="superuser",
            email="superuser@example.com",
            password="superpassword",
        )

        # Création d'un utilisateur normal
        self.normal_user = Utilisateur.objects.create_user(
            username="normaluser",
            email="normaluser@example.com",
            password="normalpassword",
        )

    def test_custom_admin_view_access_superuser(self):
        """Teste que le superutilisateur a accès à la vue admin personnalisée."""
        self.client.login(username="superuser", password="superpassword")
        response = self.client.get(
            reverse("admin-dashboard")
        )  # Assurez-vous que l'URL correspond à votre configuration
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin.html")

    def test_custom_admin_view_access_normal_user(self):
        """Teste que l'utilisateur normal est redirigé lorsqu'il essaie d'accéder à la vue admin personnalisée."""
        self.client.login(username="normaluser", password="normalpassword")
        response = self.client.get(
            reverse("admin-dashboard")
        )  # Assurez-vous que l'URL correspond à votre configuration
        self.assertEqual(response.status_code, 302)  # Vérifie la redirection
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('admin-dashboard')}"
        )

    def test_custom_admin_view_post_method(self):
        """Teste la méthode POST de la vue admin personnalisée pour un superutilisateur."""
        self.client.login(username="superuser", password="superpassword")
        response = self.client.post(
            reverse("admin-dashboard"),
            {
                # Simulez ici les données que vous enverriez dans le POST
                "some_field": "some_value"
            },
        )
        # Vérifiez que le POST fonctionne, même si la logique de traitement n'est pas implémentée
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin.html")

    def test_custom_admin_view_get_method(self):
        """Teste la méthode GET de la vue admin personnalisée pour un superutilisateur."""
        self.client.login(username="superuser", password="superpassword")
        response = self.client.get(reverse("admin-dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin.html")
