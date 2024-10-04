from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from app.models import QCM
from django.contrib.auth.models import Group

# Utilisateur personnalisé
Utilisateur = get_user_model()


class DeleteQCMViewTest(TestCase):
    def setUp(self):
        # Créer un utilisateur enseignant
        self.teacher = Utilisateur.objects.create_user(
            username="teacher", email="teacher@example.com", password="password"
        )
        teacher_group, created = Group.objects.get_or_create(name="Enseignant")
        self.teacher.groups.add(teacher_group)

        # Créer un QCM associé à cet enseignant
        self.qcm = QCM.objects.create(
            titre="Test QCM",
            description="Description du QCM",
            creator=self.teacher,
        )

        # URL de suppression
        self.url = reverse("qcm-delete", args=[self.qcm.id])

    def test_delete_qcm_authenticated(self):
        """Test qu'un enseignant authentifié peut supprimer un QCM."""
        self.client.login(username="teacher", password="password")

        response = self.client.post(self.url)

        # Vérifier que le QCM a été supprimé
        self.assertFalse(QCM.objects.filter(id=self.qcm.id).exists())

        # Vérifier la redirection après suppression
        self.assertRedirects(response, reverse("qcm-list"))

    def test_delete_qcm_unauthenticated(self):
        """Test qu'un utilisateur non authentifié est redirigé vers la page de connexion."""
        response = self.client.post(self.url)

        # Vérifier la redirection vers la page de connexion
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")

    def test_delete_qcm_not_found(self):
        """Test la suppression d'un QCM inexistant (404)."""
        self.client.login(username="teacher", password="password")

        invalid_url = reverse("qcm-delete", args=[999])  # ID invalide

        response = self.client.post(invalid_url)

        # Vérifier que la page renvoie un statut 404
        self.assertEqual(response.status_code, 404)
