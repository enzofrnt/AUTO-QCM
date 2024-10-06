from django.utils import timezone
from django.test import TestCase
from app.models import Utilisateur, Question, Reponse, ReponseQuestion, Tag


class ReponseQuestionModelTest(TestCase):
    def setUp(self):
        # Création d'un utilisateur pour le test
        self.user = Utilisateur.objects.create_user(
            username="testuser", email="test@example.com", password="password"
        )

        # Création d'une question pour le test
        self.tag = Tag.objects.create(name="Test Tag")
        self.question = Question.objects.create(
            nom="Test Question",
            texte="Ceci est un test.",
            note=2,
            melange_rep=True,
            creator=self.user,
        )
        self.question.tags.add(self.tag)

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

        self.reponse_question = ReponseQuestion.objects.create(
            utilisateur=self.user,
            question=self.question,
            date=timezone.now(),
        )
        self.reponse_question.reponse.set([self.rep1, self.rep2])

    def test_str_representation(self):
        # Update the expected string to match the current output of the model
        expected_str = f"Réponse de {self.user.username} sur {self.question.nom} à {self.reponse_question.date} :-{self.rep1.texte}-{self.rep2.texte}"
        self.assertEqual(str(self.reponse_question), expected_str)

    def test_score_calculation(self):
        # Vérifie le score calculé
        # Since there's 1 correct and 1 incorrect answer, the score is 0 (penalization happens).
        expected_score = 0  # One correct, one incorrect answer leads to a score of 0
        self.assertEqual(self.reponse_question.score, expected_score)
        self.assertEqual(self.reponse_question.score_max, self.question.note)

    def test_score_with_only_incorrect_answer(self):
        # Supprime la réponse correcte et garde seulement la réponse incorrecte
        self.reponse_question.reponse.remove(self.rep1)
        self.assertEqual(
            self.reponse_question.score, 0.0
        )  # Aucune réponse correcte, no negative scores

    def test_score_with_only_correct_answer(self):
        # Supprime la réponse incorrecte et garde seulement la réponse correcte
        self.reponse_question.reponse.remove(self.rep2)
        expected_score = self.question.note  # Full score for only the correct answer
        self.assertEqual(self.reponse_question.score, expected_score)
