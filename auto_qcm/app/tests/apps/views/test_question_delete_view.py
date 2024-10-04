from django.test import TestCase
from django.urls import reverse
from app.models import Question, Utilisateur
from django.contrib.auth.models import Group


class DeleteQuestionViewTest(TestCase):
    def setUp(self):
        # Créer un utilisateur enseignant
        self.teacher = Utilisateur.objects.create_user(
            username="teacher", email="teacher@example.com", password="password"
        )
        teacher_group, created = Group.objects.get_or_create(name="Enseignant")
        self.teacher.groups.add(teacher_group)

        # Créer une question associée à cet enseignant
        self.question = Question.objects.create(
            nom="Test Question",
            texte="Description de la question",
            creator=self.teacher,
        )

        # URL de suppression
        self.url = reverse("question-delete", args=[self.question.id])

    def test_delete_question_authenticated(self):
        """Test qu'un enseignant authentifié peut supprimer une question."""
        self.client.login(username="teacher", password="password")

        response = self.client.post(self.url)

        # Vérifier que la question a été supprimée
        self.assertFalse(Question.objects.filter(id=self.question.id).exists())

        # Vérifier la redirection après suppression vers la liste des questions
        self.assertRedirects(
            response, reverse("home")
        )  # Redirection vers la page de liste

    def test_delete_question_unauthenticated(self):
        """Test qu'un utilisateur non authentifié est redirigé vers la page de connexion."""
        response = self.client.post(self.url)

        # Vérifier la redirection vers la page de connexion
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")

    def test_delete_question_not_found(self):
        """Test la suppression d'une question inexistant (404)."""
        self.client.login(username="teacher", password="password")

        invalid_url = reverse("question-delete", args=[999])  # ID invalide

        response = self.client.post(invalid_url)

        # Vérifier que la page renvoie un statut 404
        self.assertEqual(response.status_code, 404)
