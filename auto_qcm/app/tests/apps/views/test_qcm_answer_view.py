from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from app.models import Utilisateur, QCM, Question, Reponse, ReponseQuestion, ReponseQCM
from datetime import timedelta


class RepondreQCMViewTest(TestCase):
    def setUp(self):
        """Préparation des objets pour les tests."""
        self.client = Client()

        # Créer un utilisateur pour les tests
        self.user = Utilisateur.objects.create_user(
            username="testuser", email="test@gmail.com", password="test"
        )

        # Créer un QCM
        self.qcmanswer = QCM.objects.create(
            titre="QCM de test",
            description="Ceci est un QCM de test.",
            creator=self.user,
            date_modif=timezone.now(),
        )

        # Créer une question
        self.question = Question.objects.create(
            texte="Quelle est la capitale de la France ?",
            nom="Capitale",
            note=1,  # Assurez-vous de définir une note
            melange_rep=True,
            creator=self.user,
        )

        # Créer des réponses associées à la question
        self.rep1 = Reponse.objects.create(
            question=self.question,
            texte="Paris",
            is_correct=True,
            creator=self.user,
        )
        self.rep2 = Reponse.objects.create(
            question=self.question,
            texte="Lyon",
            is_correct=False,
            creator=self.user,
        )

        # Associer la question aux QCM
        self.qcmanswer.questions.add(self.question)

        # Créer une instance de ReponseQCM pour l'utiliser dans les tests
        # Vérifier que la réponse a bien été enregistrée
        self.reponse_qcm = ReponseQCM.objects.get_or_create(
            utilisateur=self.user,
            qcm=self.qcmanswer,
            date_debut=self.qcmanswer.date_modif,
            date_fin_reponse=self.qcmanswer.date_modif + timedelta(minutes=5),
        )
        self.reponse_question = ReponseQuestion.objects.get_or_create(
            utilisateur=self.user,
            question=self.question,
            date=timezone.now(),
        )

        # Définir l'URL pour répondre au QCM avec les deux IDs
        self.url_repondre = reverse(
            "qcm-answer", args=[self.qcmanswer.id, self.reponse_qcm.id]
        )

    def test_repondre_qcm_view_access(self):
        """Test l'accès à la vue de réponse d'un QCM."""
        # Connexion de l'utilisateur
        self.client.login(username="testuser", password="test")
        response = self.client.get(self.url_repondre)

        # Vérification du statut HTTP
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "qcm/qcm_answer.html")

        # Vérifier que le contexte contient le QCM et les questions
        self.assertIn("qcm", response.context)
        self.assertIn("questions", response.context)

    def test_submit_reponses(self):
        """Test la soumission des réponses pour un QCM."""
        self.client.login(username="testuser", password="test")

        # Soumettre une réponse
        # response = self.client.post(
        #     self.url_repondre,
        #     {
        #         f"question_{self.question.id}": self.rep1.id  # Sélection de la réponse correcte
        #     },
        # )

        # # Vérification de la redirection vers la page de correction
        # self.assertRedirects(
        #     response,
        #     reverse("qcm-correct", args=[self.qcmanswer.id]),
        # )

        self.assertIn(self.reponse_question, self.reponse_qcm.reponses.all())
        self.assertIn(self.rep1, self.reponse_question.reponse.all())

    def test_access_without_login(self):
        """Test qu'un utilisateur non connecté est redirigé vers la page de connexion."""
        response = self.client.get(self.url_repondre)

        # L'utilisateur doit être redirigé vers la page de connexion
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url_repondre}")
