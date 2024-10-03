from django.test import TestCase
from app.models import ReponseQCM, Utilisateur, QCM, Question, Reponse, ReponseQuestion


class ReponseQCMModelTest(TestCase):
    def setUp(self):
        # Création d'un utilisateur pour le test
        self.user = Utilisateur.objects.create_user(
            username="testuser", email="test@example.com", password="password"
        )

        # Création d'un QCM pour le test
        self.qcm = QCM.objects.create(
            titre="Test QCM", description="Description du test.", creator=self.user
        )

        # Création de questions pour le QCM
        self.question1 = Question.objects.create(
            nom="Question 1",
            texte="Ceci est la première question.",
            note=2,
            melange_rep=True,
            creator=self.user,
        )
        self.question2 = Question.objects.create(
            nom="Question 2",
            texte="Ceci est la deuxième question.",
            note=3,
            melange_rep=True,
            creator=self.user,
        )

        # Ajout des questions au QCM
        self.qcm.questions.set([self.question1, self.question2])

        # Création de réponses pour les questions
        self.rep1 = Reponse.objects.create(
            question=self.question1,
            texte="Réponse correcte",
            is_correct=True,
            creator=self.user,
        )
        self.rep2 = Reponse.objects.create(
            question=self.question1,
            texte="Réponse incorrecte",
            is_correct=False,
            creator=self.user,
        )
        self.rep3 = Reponse.objects.create(
            question=self.question2,
            texte="Réponse correcte",
            is_correct=True,
            creator=self.user,
        )
        self.rep4 = Reponse.objects.create(
            question=self.question2,
            texte="Réponse incorrecte",
            is_correct=False,
            creator=self.user,
        )

        # Création de ReponseQuestion pour simuler des réponses
        self.reponse_question1 = ReponseQuestion.objects.create(
            utilisateur=self.user,
            question=self.question1,
            date=self.qcm.date_modif,  # Utilisation de la date du QCM
        )
        self.reponse_question1.reponse.set([self.rep1])  # Bonne réponse

        self.reponse_question2 = ReponseQuestion.objects.create(
            utilisateur=self.user,
            question=self.question2,
            date=self.qcm.date_modif,  # Utilisation de la date du QCM
        )
        self.reponse_question2.reponse.set([self.rep3])  # Bonne réponse

        # Création d'une instance de ReponseQCM
        self.reponse_qcm = ReponseQCM.objects.create(
            utilisateur=self.user,
            qcm=self.qcm,
            date_debut=self.qcm.date_modif,
        )
        self.reponse_qcm.reponses.set([self.reponse_question1, self.reponse_question2])

    def test_reponse_qcm_creation(self):
        """Test la création d'une instance de ReponseQCM."""
        self.assertIsInstance(self.reponse_qcm, ReponseQCM)
        self.assertEqual(self.reponse_qcm.utilisateur, self.user)
        self.assertEqual(self.reponse_qcm.qcm, self.qcm)

    def test_score_calculation(self):
        """Test le calcul du score pour les réponses du QCM."""
        self.assertEqual(self.reponse_qcm.score, 5)  # Question 1 (2) + Question 2 (3)

    def test_score_max_calculation(self):
        """Test le calcul du score maximum pour le QCM."""
        self.assertEqual(
            self.reponse_qcm.score_max, 5
        )  # Question 1 (2) + Question 2 (3)

    def test_string_representation(self):
        """Test la représentation en chaîne de l'instance ReponseQCM."""
        expected_str = f"Reponse de {self.user.username} à {self.qcm.titre}"
        self.assertEqual(str(self.reponse_qcm), expected_str)
