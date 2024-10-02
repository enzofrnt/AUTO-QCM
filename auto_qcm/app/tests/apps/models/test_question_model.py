from django.test import TestCase
from django.contrib.auth.models import Group
from app.models import Utilisateur, Question, Tag, Reponse


class QuestionModelTest(TestCase):
    def setUp(self):
        # Création d'un utilisateur pour le test
        self.user = Utilisateur.objects.create_user(
            "testuser", "test@example.com", "password"
        )

        # Création d'un tag pour la question
        self.tag = Tag.objects.create(name="Test Tag")

        # Création d'une question
        self.question = Question.objects.create(
            nom="Test Question",
            texte="Ceci est un test.",
            note=1,
            melange_rep=True,
            creator=self.user,
        )
        # Ajout des tags à la question
        self.question.tags.add(self.tag)

        # Création de réponses associées
        self.rep1 = Reponse.objects.create(
            question=self.question,
            texte="Réponse 1",
            is_correct=True,
            creator=self.user,
        )
        self.rep2 = Reponse.objects.create(
            question=self.question,
            texte="Réponse 2",
            is_correct=False,
            creator=self.user,
        )

    def test_question_creation(self):
        """Test la création d'une question."""
        self.assertIsInstance(self.question, Question)
        self.assertEqual(self.question.nom, "Test Question")
        self.assertEqual(self.question.texte, "Ceci est un test.")
        self.assertEqual(self.question.note, 1)
        self.assertTrue(self.question.melange_rep)

    def test_get_correct_answers(self):
        """Test de la méthode get_correct_answers."""
        correct_answers = self.question.get_correct_answers()
        self.assertEqual(
            list(correct_answers), [self.rep1]
        )  # Doit retourner uniquement la réponse correcte

    def test_number_of_correct_answers(self):
        """Test de la propriété number_of_correct_answers."""
        self.assertEqual(
            self.question.number_of_correct_answers, 1
        )  # Une réponse correcte

    def test_convert_to_xml(self):
        """Test de la conversion en XML."""
        xml_output = self.question.convertToXml()
        self.assertIn('<question type="multichoice">', xml_output)
        self.assertIn("<name><text>Test Question</text></name>", xml_output)
        self.assertIn('<questiontext format="html">', xml_output)

    def test_convert_to_xml_single(self):
        """Test de la conversion en XML pour téléchargement."""
        xml_output_single = self.question.convertToXmlSingle()
        self.assertIn('<?xml version="1.0"?><quiz>', xml_output_single)
        self.assertIn('<question type="multichoice">', xml_output_single)

    def test_str_method(self):
        """Test de la méthode __str__."""
        self.assertEqual(
            str(self.question), "Ceci est un test."
        )  # Vérification de la méthode __str__
