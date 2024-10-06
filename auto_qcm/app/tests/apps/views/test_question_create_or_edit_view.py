import logging
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group
from app.models import Question, Utilisateur


class CreateOrEditQuestionViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        logging.disable(logging.CRITICAL)  # Disable logging for tests

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)  # Re-enable logging
        super().tearDownClass()

    def setUp(self):
        # Create a teacher user
        self.teacher = Utilisateur.objects.create_user(
            username="teacher", email="teacher@example.com", password="password"
        )
        teacher_group, _ = Group.objects.get_or_create(name="Enseignant")
        self.teacher.groups.add(teacher_group)

        # Create an initial question for testing
        self.question = Question.objects.create(
            nom="Test Question",
            texte="What is the capital of France?",
            note=5,
            creator=self.teacher,
        )
        self.create_url = reverse("question-create")
        self.edit_url = reverse(
            "question-edit", args=[self.question.id]
        )  # Use question id here

    def test_create_question_unauthenticated(self):
        """Test qu'un utilisateur non authentifié est redirigé vers la page de connexion."""
        response = self.client.post(
            self.create_url,
            {
                "nom": "Unauthorized Question",
                "texte": "You should not be able to create this.",
            },
        )
        self.assertRedirects(response, f"{reverse('login')}?next={self.create_url}")

    def test_create_question_invalid_data(self):
        """Test la gestion des erreurs de formulaire lors de la création d'une question."""
        self.client.login(username="teacher", password="password")

        response = self.client.post(
            self.create_url,
            {
                "nom": "",  # Empty field to trigger validation error
                "texte": "This should fail.",
                "note": 5,
            },
        )

        # Check for form errors in the response context
        form = response.context["form"]
        self.assertTrue(form.errors)
        self.assertIn("nom", form.errors)  # Check for the right field
        self.assertEqual(
            form.errors["nom"], ["This field is required."]
        )  # Adjust based on your actual form
