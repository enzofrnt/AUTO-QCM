from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import Group
from app.models import Utilisateur, QCM, Question, ReponseQCM
from datetime import timedelta


class EnseignantDashboardViewTest(TestCase):
    def setUp(self):
        """Configuration des objets pour les tests."""
        self.client = Client()

        # Création des groupes
        self.teacher_group, _ = Group.objects.get_or_create(name="Enseignant")
        self.student_group, _ = Group.objects.get_or_create(name="Etudiant")

        # Créer un enseignant pour le test
        self.enseignant = Utilisateur.objects.create_user(
            username="testenseignant",
            email="testenseignant@gmail.com",
            password="test",
        )
        self.enseignant.groups.add(self.teacher_group)

        # Créer un étudiant pour le test
        self.etudiant = Utilisateur.objects.create_user(
            username="testetudiant",
            email="testetudiant@gmail.com",
            password="test",
        )
        self.etudiant.groups.add(self.student_group)

        # Créer des questions
        self.question1 = Question.objects.create(
            texte="Question 1",
            creator=self.enseignant,
        )
        self.question2 = Question.objects.create(
            texte="Question 2",
            creator=self.enseignant,
        )

        # Créer un QCM passé (30 jours dans le passé)
        self.qcm1 = QCM.objects.create(
            titre="QCM 1",
            description="Description du QCM 1",
            creator=self.enseignant,
            date_modif=timezone.now() - timedelta(days=30),
        )
        self.qcm1.questions.add(self.question1)

        # Créer un QCM à venir (60 jours dans le futur)
        self.qcm2 = QCM.objects.create(
            titre="QCM 2",
            description="Description du QCM 2",
            creator=self.enseignant,
            date_modif=timezone.now() + timedelta(days=60),
        )
        self.qcm2.questions.add(self.question2)

        # Créer un QCM pour aujourd'hui
        self.qcm3 = QCM.objects.create(
            titre="QCM 3",
            description="Description du QCM 3",
            creator=self.enseignant,
            date_modif=timezone.now(),
        )
        self.qcm3.questions.add(self.question1, self.question2)

        # Créer une réponse au QCM
        self.reponse_qcm = ReponseQCM.objects.create(
            utilisateur=self.etudiant,
            qcm=self.qcm1,
            date_debut=self.qcm1.date_modif,
            date_fin_reponse=self.qcm1.date_modif + timedelta(minutes=5),
        )

        # Définir l'URL pour le tableau de bord de l'enseignant
        self.url_dashboard = reverse("enseignant-dashboard", args=[self.enseignant.pk])

    def test_enseignant_dashboard_access(self):
        """Test que l'enseignant peut accéder à son tableau de bord."""
        self.client.login(username="testenseignant", password="test")
        response = self.client.get(self.url_dashboard)

        # Vérification du statut de la réponse
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/enseignant_dashboard.html")

        # Vérifier que le contexte contient les données attendues
        self.assertIn("qcms_with_questions", response.context)
        self.assertIn("upcoming_qcms", response.context)
        self.assertIn("total_qcms", response.context)
        self.assertIn("total_questions", response.context)
        self.assertIn("total_responses", response.context)
        self.assertIn("enseignant", response.context)

        # Vérifier les QCMs à venir
        upcoming_qcms = response.context["upcoming_qcms"]
        self.assertIn(self.qcm2, upcoming_qcms)  # QCM à venir doit être là
        self.assertIn(self.qcm3, upcoming_qcms)  # QCM d'aujourd'hui doit être là

        # # Vérifier les statistiques
        # self.assertEqual(response.context["total_qcms"], 3)
        # self.assertEqual(response.context["total_questions"], 2)
        # self.assertEqual(response.context["total_responses"], 1)

    def test_access_without_login(self):
        """Test qu'un utilisateur non connecté est redirigé vers la page de connexion."""
        response = self.client.get(self.url_dashboard)

        # L'utilisateur doit être redirigé vers la page de connexion
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url_dashboard}")

    def test_access_for_non_teacher(self):
        """Test qu'un utilisateur non enseignant ne peut pas accéder au dashboard enseignant."""
        self.client.login(username="testetudiant", password="test")
        response = self.client.get(self.url_dashboard)

        # L'accès devrait être refusé
        self.assertEqual(response.status_code, 403)

    def test_access_for_other_teacher(self):
        """Test qu'un enseignant ne peut pas accéder au dashboard d'un autre enseignant."""
        other_teacher = Utilisateur.objects.create_user(
            username="otherteacher",
            email="otherteacher@gmail.com",
            password="test",
        )
        other_teacher.groups.add(self.teacher_group)
        self.client.login(username="otherteacher", password="test")
        response = self.client.get(self.url_dashboard)

        # L'accès devrait être refusé
        self.assertEqual(response.status_code, 403)
