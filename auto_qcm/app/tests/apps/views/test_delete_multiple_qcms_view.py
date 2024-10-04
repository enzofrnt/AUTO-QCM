from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from app.models.qcm import QCM
from app.models import Utilisateur
from django.contrib.auth.models import Group


class DeleteMultipleQCMsViewTests(TestCase):
    def setUp(self):
        # Création d'un utilisateur enseignant pour le test
        self.teacher = Utilisateur.objects.create_user(
            username="teacher", email="teacher@example.com", password="password"
        )
        teacher_group, _ = Group.objects.get_or_create(name="Enseignant")
        self.teacher.groups.add(teacher_group)
        self.client.login(username="teacher", password="password")

        # Création de quelques QCMs pour les tests
        self.qcm1 = QCM.objects.create(
            titre="QCM 1", description="Description 1", creator=self.teacher
        )
        self.qcm2 = QCM.objects.create(
            titre="QCM 2", description="Description 2", creator=self.teacher
        )
        self.qcm3 = QCM.objects.create(
            titre="QCM 3", description="Description 3", creator=self.teacher
        )

    def test_delete_multiple_qcms_success(self):
        """Test de suppression de plusieurs QCM avec succès."""
        # Liste des QCM sélectionnés à supprimer
        selected_qcms = [self.qcm1.id, self.qcm2.id]
        response = self.client.post(
            reverse("qcm-delete-multiple"), {"selected_qcms": selected_qcms}
        )

        # Vérification que les QCM ont été supprimés
        self.assertFalse(QCM.objects.filter(id=self.qcm1.id).exists())
        self.assertFalse(QCM.objects.filter(id=self.qcm2.id).exists())
        self.assertTrue(QCM.objects.filter(id=self.qcm3.id).exists())

        # Vérification du message de succès
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "2 QCM supprimé(s) avec succès.")

        # Vérification de la redirection
        self.assertRedirects(response, reverse("qcm-list"))

    def test_delete_multiple_qcms_no_selection(self):
        """Test quand aucun QCM n'est sélectionné pour suppression."""
        response = self.client.post(
            reverse("qcm-delete-multiple"), {"selected_qcms": []}
        )

        # Vérification que les QCM existent toujours
        self.assertTrue(QCM.objects.filter(id=self.qcm1.id).exists())
        self.assertTrue(QCM.objects.filter(id=self.qcm2.id).exists())
        self.assertTrue(QCM.objects.filter(id=self.qcm3.id).exists())

        # Vérification du message d'avertissement
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Aucun QCM sélectionné.")

        # Vérification de la redirection
        self.assertRedirects(response, reverse("qcm-list"))

    def test_delete_multiple_qcms_partial_selection(self):
        """Test de suppression partielle des QCM (un seul sélectionné)."""
        selected_qcms = [self.qcm3.id]
        response = self.client.post(
            reverse("qcm-delete-multiple"), {"selected_qcms": selected_qcms}
        )

        # Vérification que le QCM sélectionné a été supprimé et les autres non
        self.assertFalse(QCM.objects.filter(id=self.qcm3.id).exists())
        self.assertTrue(QCM.objects.filter(id=self.qcm1.id).exists())
        self.assertTrue(QCM.objects.filter(id=self.qcm2.id).exists())

        # Vérification du message de succès
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "1 QCM supprimé(s) avec succès.")

        # Vérification de la redirection
        self.assertRedirects(response, reverse("qcm-list"))
