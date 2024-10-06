from django.test import TestCase, Client
from django.urls import reverse
from app.models import Question, Reponse, Utilisateur
import json
from django.utils import timezone
import logging


class SaveGeneratedQuestionsViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Désactiver la journalisation pour les tests si vous le souhaitez
        logging.disable(
            logging.CRITICAL
        )  # Désactive tous les logs de niveau CRITICAL et inférieurs

    @classmethod
    def tearDownClass(cls):
        # Réactiver la journalisation après les tests
        logging.disable(logging.NOTSET)  # Réactive les logs
        super().tearDownClass()

    def setUp(self):
        """Création des objets pour les tests."""
        self.user = Utilisateur.objects.create_user("testqcm", "test@gamil.com", "test")
        self.user.save()

        self.client = Client()
        self.url = reverse("save-questions")

    def test_access_without_authentication(self):
        # Tester l'accès non authentifié
        response = self.client.post(self.url)
        self.assertEqual(
            response.status_code, 302
        )  # Devrait rediriger vers la page de login

    def test_access_with_authentication(self):
        # Tester l'accès authentifié
        self.client.login(username="testqcm", password="test")

        # Exemple de données JSON
        questions_data = {
            "questions": [
                {
                    "nom": "Question 1",
                    "texte": "Texte de la question 1",
                    "reponses": [
                        {"texte": "Réponse 1", "is_correct": True},
                        {"texte": "Réponse 2", "is_correct": False},
                    ],
                },
                {
                    "nom": "Question 2",
                    "texte": "Texte de la question 2",
                    "reponses": [
                        {"texte": "Réponse A", "is_correct": True},
                        {"texte": "Réponse B", "is_correct": False},
                    ],
                },
            ]
        }

        # Envoyer une requête POST avec les données JSON
        response = self.client.post(
            self.url,
            data=json.dumps(questions_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content, {"message": "Questions sauvegardées avec succès !"}
        )

        # Vérifier que les questions ont été créées
        self.assertEqual(Question.objects.count(), 2)
        self.assertEqual(Reponse.objects.count(), 4)

    def test_invalid_json(self):
        # Tester avec un JSON mal formé
        self.client.login(username="testqcm", password="test")
        response = self.client.post(
            self.url,
            data="{'invalid': 'json'}",  # JSON mal formé
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {"error": "Invalid JSON format"})
