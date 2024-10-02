from django.test import TestCase
from app.models import Reponse, Utilisateur, Question, Tag


class ReponseModelTest(TestCase):
    def setUp(self):
        # Create a user to associate with the question and response
        self.user = Utilisateur.objects.create_user(
            username="testuser", email="test@example.com", password="password"
        )

        # Create a tag and question to associate with the response
        self.tag = Tag.objects.create(name="Test Tag")
        self.question = Question.objects.create(
            nom="Test Question",
            texte="Ceci est une question test.",
            note=2,
            melange_rep=True,
            creator=self.user,
        )
        self.question.tags.add(self.tag)

        # Create responses
        self.correct_response = Reponse.objects.create(
            question=self.question,
            texte="Réponse correcte",
            is_correct=True,
            creator=self.user,
        )

        self.incorrect_response = Reponse.objects.create(
            question=self.question,
            texte="Réponse incorrecte",
            is_correct=False,
            creator=self.user,
        )

    def test_str_representation(self):
        """Test that the __str__ method returns the correct string."""
        self.assertEqual(str(self.correct_response), "Réponse correcte")
        self.assertEqual(str(self.incorrect_response), "Réponse incorrecte")

    def test_convertToXml_correct_answer(self):
        """Test the XML conversion for a correct response."""
        # Ensure the question has 1 correct answer
        self.assertEqual(self.question.number_of_correct_answers, 1)

        expected_xml = (
            '<answer fraction="100.0" format="html">'
            "<text>Réponse correcte</text>"
            '<feedback format="html">'
            "<text/>"
            "</feedback>"
            "</answer>"
        )
        self.assertEqual(self.correct_response.convertToXml(), expected_xml)

    def test_convertToXml_incorrect_answer(self):
        """Test the XML conversion for an incorrect response."""
        expected_xml = (
            '<answer fraction="0" format="html">'
            "<text>Réponse incorrecte</text>"
            '<feedback format="html">'
            "<text/>"
            "</feedback>"
            "</answer>"
        )
        self.assertEqual(self.incorrect_response.convertToXml(), expected_xml)

    def test_convertToXml_multiple_correct_answers(self):
        """Test the XML conversion when multiple correct answers are possible."""
        # Simulate another correct answer being added
        Reponse.objects.create(
            question=self.question,
            texte="Deuxième réponse correcte",
            is_correct=True,
            creator=self.user,
        )

        # Ensure the question now has 2 correct answers
        self.assertEqual(self.question.number_of_correct_answers, 2)

        # Check the XML conversion for the original correct answer
        expected_xml = (
            '<answer fraction="50.0" format="html">'
            "<text>Réponse correcte</text>"
            '<feedback format="html">'
            "<text/>"
            "</feedback>"
            "</answer>"
        )
        self.assertEqual(self.correct_response.convertToXml(), expected_xml)
