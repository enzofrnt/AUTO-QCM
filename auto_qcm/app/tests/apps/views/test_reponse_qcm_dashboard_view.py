from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from app.models import QCM, ReponseQCM, Utilisateur, Reponse, Question, ReponseQuestion
from datetime import timedelta


class QcmResponsesViewTests(TestCase):
    def setUp(self):
        """Création des objets pour les tests."""
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

        # Utiliser les IDs des réponses pour l'association
        self.reponse_qcm1.reponses.set(
            [self.reponse_question]
        )  # Correction ici : utiliser les IDs

        # Définir l'URL du test
        self.url = reverse("qcm-responses", args=[self.qcm.id])

    def test_access_without_authentication(self):
        """Tester l'accès non authentifié."""
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code, 302
        )  # Devrait rediriger vers la page de login

    def test_access_with_authentication(self):
        """Tester l'accès authentifié."""
        self.client.login(username="testqcm", password="test")
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code, 200
        )  # La page doit se charger correctement
        self.assertTemplateUsed(response, "dashboard/reponse_qcm_dashboard.html")

    def test_qcm_responses_displayed(self):
        """Tester que les réponses sont bien affichées dans le contexte."""
        self.client.login(username="testqcm", password="test")
        response = self.client.get(self.url)

        # Vérifier que le QCM et les réponses sont dans le contexte
        self.assertEqual(response.context["qcm"], self.qcm)
        self.assertIn(self.reponse_qcm1, response.context["reponses"])

    def test_qcm_not_found(self):
        """Tester l'accès à un QCM qui n'existe pas."""
        self.client.login(username="testqcm", password="test")
        invalid_url = reverse("qcm-responses", args=[999])  # QCM avec un ID inexistant
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)  # Doit retourner une erreur 404
