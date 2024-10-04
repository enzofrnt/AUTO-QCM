from django.test import TestCase, Client
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from app.models import (
    Utilisateur,
    Question,
    QCM,
    ReponseQCM,
)  # Adjust this import based on your app structure


class CustomErrorViewsTest(TestCase):
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

        # Créer des QCMs pour les tests
        self.qcm1 = QCM.objects.create(
            titre="QCM 1",
            description="Description du QCM 1",
            creator=self.enseignant,
            date_modif=timezone.now() - timedelta(days=30),
        )
        self.qcm1.questions.add(self.question1)

        self.qcm2 = QCM.objects.create(
            titre="QCM 2",
            description="Description du QCM 2",
            creator=self.enseignant,
            date_modif=timezone.now() + timedelta(days=60),
        )
        self.qcm2.questions.add(self.question2)

        self.qcm3 = QCM.objects.create(
            titre="QCM 3",
            description="Description du QCM 3",
            creator=self.enseignant,
            date_modif=timezone.now(),
        )
        self.qcm3.questions.add(self.question1, self.question2)

        self.reponse_qcm = ReponseQCM.objects.create(
            utilisateur=self.etudiant,
            qcm=self.qcm1,
            date_debut=self.qcm1.date_modif,
            date_fin_reponse=self.qcm1.date_modif + timedelta(minutes=5),
        )

    def test_custom_page_not_found_view(self):
        """Test de la vue de page non trouvée (404)."""
        response = self.client.get("/nonexistent-url/")  # URL qui n'existe pas
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "errors/404.html")

    def test_custom_permission_denied_view(self):
        """Test de la vue d'accès refusé (403)."""
        # Create a new student user without permissions
        student_user = Utilisateur.objects.create_user(
            username="teststudent",
            email="teststudent@gmail.com",
            password="test",
        )

        # Log in as the student
        self.client.login(username="teststudent", password="test")

        # Attempt to access the enseignant dashboard
        response = self.client.get(
            reverse("enseignant-dashboard", args=[self.enseignant.pk])
        )

        # Assert that the response status code is 403
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "errors/403.html")
