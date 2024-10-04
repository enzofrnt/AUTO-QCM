from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from app.models import Utilisateur, QCM, ReponseQCM
from datetime import timedelta


class EtudiantDashboardViewTest(TestCase):
    def setUp(self):
        """Configuration des objets pour les tests."""
        self.client = Client()

        # Créer un utilisateur pour le test
        self.user = Utilisateur.objects.create_user(
            username="testuser", email="testuser@gmail.com", password="test"
        )

        # Créer un QCM passé (30 jours dans le passé)
        self.qcm1 = QCM.objects.create(
            titre="QCM 1",
            description="Description du QCM 1",
            creator=self.user,
            date_modif=timezone.now() - timedelta(days=30),  # QCM passé
        )

        # Créer un QCM à venir (60 jours dans le futur)
        self.qcm2 = QCM.objects.create(
            titre="QCM 2",
            description="Description du QCM 2",
            creator=self.user,
            date_modif=timezone.now() + timedelta(days=60),  # QCM à venir
        )

        # Ajouter un QCM pour aujourd'hui
        self.qcm3 = QCM.objects.create(
            titre="QCM 3",
            description="Description du QCM 3",
            creator=self.user,
            date_modif=timezone.now(),  # QCM pour aujourd'hui
        )

        # Créer une réponse au QCM
        self.reponse_qcm = ReponseQCM.objects.create(
            utilisateur=self.user,
            qcm=self.qcm1,
            date_debut=self.qcm1.date_modif,
            date_fin_reponse=timezone.now() + timedelta(minutes=5),
        )

        # Définir l'URL pour le tableau de bord de l'étudiant
        self.url_dashboard = reverse("etudiant-dashboard", args=[self.user.pk])

    def test_etudiant_dashboard_access(self):
        """Test que l'étudiant peut accéder à son tableau de bord."""
        self.client.login(username="testuser", password="test")
        response = self.client.get(self.url_dashboard)

        # Vérification du statut de la réponse
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/etudiant_dashboard.html")

        # Vérifier que le contexte contient les données attendues
        self.assertIn("upcoming_qcms", response.context)
        self.assertIn("reponse_qcm", response.context)
        self.assertIn("utilisateur", response.context)

        # Vérifier que seules les QCM à venir sont retournées
        upcoming_qcms = response.context["upcoming_qcms"]

        # Vérification des QCMs
        self.assertIn(self.qcm2, upcoming_qcms)  # QCM à venir doit être là

    def test_access_without_login(self):
        """Test qu'un utilisateur non connecté est redirigé vers la page de connexion."""
        response = self.client.get(self.url_dashboard)

        # L'utilisateur doit être redirigé vers la page de connexion
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url_dashboard}")

    def test_access_for_user_without_proper_permissions(self):
        """Test que l'utilisateur sans permissions appropriées est redirigé ou reçoit une erreur 403."""
        # Créer un autre utilisateur sans permissions
        other_user = Utilisateur.objects.create_user(
            username="otheruser", email="otheruser@gmail.com", password="test"
        )

        self.client.login(username="otheruser", password="test")
        response = self.client.get(self.url_dashboard)

        # Assurez-vous que l'utilisateur est redirigé ou reçoit une erreur
        self.assertEqual(
            response.status_code, 403
        )  # Vérifiez la gestion de l'erreur 403
