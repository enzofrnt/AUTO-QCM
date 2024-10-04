from django.test import TestCase
from django.contrib.auth.models import Group
from django.urls import reverse
from app.models import Utilisateur, QCM


class QcmListViewTests(TestCase):
    def setUp(self):
        """Création des utilisateurs et des QCM pour les tests."""
        # Création d'un utilisateur enseignant
        self.user_teacher = Utilisateur.objects.create_user(
            username="teacher", email="teacher@example.com", password="password"
        )

        # Création d'un utilisateur étudiant
        self.user_student = Utilisateur.objects.create_user(
            username="student", email="student@example.com", password="password"
        )

        self.teacher_group, created = Group.objects.get_or_create(name="Enseignant")
        self.user_teacher.groups.add(self.teacher_group)

        self.student_group, created = Group.objects.get_or_create(name="Etudiant")
        self.user_student.groups.add(self.student_group)

        # Création de QCM
        self.qcm1 = QCM.objects.create(
            titre="QCM 1", description="Description QCM 1", creator=self.user_teacher
        )
        self.qcm2 = QCM.objects.create(
            titre="QCM 2", description="Description QCM 2", creator=self.user_teacher
        )

        # URL de la vue de liste des QCM
        self.url = reverse(
            "qcm-list"
        )  # Assurez-vous que ce nom est correct dans vos URLs

    def test_qcm_list_view_access_for_teacher(self):
        """Test d'accès à la vue QCM pour un enseignant."""
        self.client.login(username="teacher", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "qcm/qcm_list.html")
        self.assertContains(response, self.qcm1.titre)
        self.assertContains(response, self.qcm2.titre)

    def test_qcm_list_view_access_for_student(self):
        """Test d'accès à la vue QCM pour un étudiant."""
        self.client.login(username="student", password="password")
        response = self.client.get(self.url)
        # S'assurer que les étudiants ne peuvent pas accéder à cette vue
        self.assertEqual(
            response.status_code, 403
        )  # Vérifiez si cela redirige ou retourne une erreur 403
