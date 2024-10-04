from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from app.models import Utilisateur, QCM, Question, Reponse, ReponseQuestion, ReponseQCM
from datetime import timedelta


class CorrigerQCMViewTest(TestCase):
    def setUp(self):
        """Préparation des objets pour les tests."""
        self.client = Client()

        # Créer un utilisateur pour les tests
        self.user = Utilisateur.objects.create_user(
            username="testqcm", email="test@gmail.com", password="test"
        )

        # Créer un QCM
        self.qcm = QCM.objects.create(
            titre="QCM de test",
            description="Ceci est un QCM de test.",
            creator=self.user,
            date_modif=timezone.now(),
        )

        # Créer une question
        self.question = Question.objects.create(
            texte="Quelle est la capitale de la France ?",
            nom="Capitale",
            creator=self.user,
        )

        # Création de réponses associées à la question
        self.rep1 = Reponse.objects.create(
            question=self.question,
            texte="Réponse correcte",
            is_correct=True,
            creator=self.user,
        )
        self.rep2 = Reponse.objects.create(
            question=self.question,
            texte="Réponse incorrecte",
            is_correct=False,
            creator=self.user,
        )

        # Créer une réponse question
        self.reponse_question = ReponseQuestion.objects.create(
            utilisateur=self.user,
            question=self.question,
            date=timezone.now(),
        )

        # Associer les réponses à la réponse question
        self.reponse_question.reponse.set([self.rep1, self.rep2])

        # Créer une réponse QCM
        self.reponse_qcm1 = ReponseQCM.objects.create(
            utilisateur=self.user,
            qcm=self.qcm,
            date_debut=self.qcm.date_modif,
            date_fin_reponse=self.qcm.date_modif + timedelta(minutes=5),
        )

        # Associer les réponses question à la réponse QCM
        self.reponse_qcm1.reponses.set([self.reponse_question])

        # Définir l'URL pour corriger le QCM
        self.url_corriger = reverse("qcm-correct", args=[self.reponse_qcm1.id])

    def test_corriger_qcm_view_access(self):
        """Test l'accès à la vue de correction d'un QCM."""
        # Connexion de l'utilisateur
        self.client.login(username="testqcm", password="test")
        response = self.client.get(self.url_corriger)

        # Vérification du statut HTTP
        self.assertEqual(response.status_code, 200)

        # Vérification des données dans le contexte
        self.assertIn("reponse_qcm", response.context)
        self.assertIn("qcm", response.context)

    def test_access_without_login(self):
        """Test qu'un utilisateur non connecté est redirigé vers la page de connexion."""
        response = self.client.get(self.url_corriger)

        # L'utilisateur doit être redirigé vers la page de connexion
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url_corriger}")
