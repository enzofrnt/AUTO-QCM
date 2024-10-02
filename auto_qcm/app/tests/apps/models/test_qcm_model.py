from django.test import TestCase
from django.utils import timezone
from app.models import (
    QCM,
    Question,
    Utilisateur,
)  # Assurez-vous d'importer les modèles nécessaires


class QCMModelTest(TestCase):
    def setUp(self):
        """Création des objets pour les tests."""
        self.user = Utilisateur.objects.create_user("testqcm", "test@gamil.com", "test")
        self.user.save()

        self.qcm = QCM.objects.create(
            titre="QCM Test",
            description="Description du QCM",
            creator=self.user,
            date_modif=timezone.now(),
        )
        self.qcm.save()
        self.question1 = Question.objects.create(
            nom="Question 1", texte="Texte 1", creator=self.user
        )
        self.question2 = Question.objects.create(
            nom="Question 2", texte="Texte 2", creator=self.user
        )
        self.reponse1 = self.question1.reponses.create(
            texte="Réponse 1", is_correct=True, creator=self.user
        )
        self.reponse2 = self.question1.reponses.create(
            texte="Réponse 2", is_correct=False, creator=self.user
        )
        self.qcm.questions.add(self.question1, self.question2)

    def test_qcm_creation(self):
        """Test de la création d'un QCM."""
        self.assertEqual(self.qcm.titre, "QCM Test")
        self.assertEqual(self.qcm.description, "Description du QCM")
        self.assertEqual(self.qcm.creator, self.user)
        self.assertIsNotNone(self.qcm.date_modif)

    def test_save_updates_date_modif(self):
        """Test que la date de modification est mise à jour lors de la sauvegarde."""
        old_date_modif = self.qcm.date_modif
        self.qcm.titre = "Nouveau Titre"
        self.qcm.save()
        self.assertNotEqual(self.qcm.date_modif, old_date_modif)

    def test_number_of_questions(self):
        """Test que la méthode number_of_questions retourne le bon nombre."""
        self.assertEqual(self.qcm.number_of_questions, 2)

    def test_convert_to_xml(self):
        """Test de la conversion en XML."""
        expected_xml = '<?xml version="1.0"?><quiz>'
        expected_xml += self.question1.convertToXml()
        expected_xml += self.question2.convertToXml()
        expected_xml += "</quiz>"
        self.assertEqual(self.qcm.convertToXml(), expected_xml)

    def test_convert_to_latex(self):
        """Test de la conversion en LaTeX."""
        # Ajouter des réponses à la question

        # Tester la génération LaTeX
        latex_content = self.qcm.convert_to_latex()

        # Vérifier que le LaTeX contient les informations attendues
        self.assertIn(r"\documentclass{article}", latex_content)
        self.assertIn(self.question1.nom, latex_content)
        self.assertIn(self.reponse1.texte, latex_content)
        self.assertIn(r"\bonne{Réponse 1}", latex_content)
        self.assertIn(self.reponse2.texte, latex_content)  # Utilisation de reponse2
        self.assertIn(r"\mauvaise{Réponse 2}", latex_content)  # Assertion pour reponse2
