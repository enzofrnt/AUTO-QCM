from django.test import TestCase, Client
from django.contrib.auth.models import Group
from django.urls import reverse
from app.models import Question, Tag, Utilisateur
from django.utils import timezone


class RemoveTagViewTests(TestCase):
    def setUp(self):
        """Configuration initiale des tests."""
        self.client = Client()
        self.user_teacher = Utilisateur.objects.create_user(
            username="teacher", email="teacher@example.com", password="password"
        )
        self.user_student = Utilisateur.objects.create_user(
            username="student", email="student@example.com", password="password"
        )

        self.tutor_group, created = Group.objects.get_or_create(name="Enseignant")
        self.user_teacher.groups.add(self.tutor_group)

        self.student_group, created = Group.objects.get_or_create(name="Etudiant")
        self.user_student.groups.add(self.student_group)

        # Créer une question et un tag pour les tests

        self.question = Question.objects.create(
            texte="Quelle est la capitale de la France ?",
            nom="Capitale",
            creator=self.user_teacher,  # L'utilisateur doit être un enseignant
        )
        self.tag = Tag.objects.create(name="Géographie")

        # Associer le tag à la question
        self.question.tags.add(self.tag)

        # Définir l'URL pour supprimer un tag
        self.url = reverse("remove-tag", args=[self.question.id, self.tag.id])

    def test_remove_tag_authenticated_teacher(self):
        """Tester que l'enseignant peut supprimer un tag d'une question."""
        self.client.login(username="teacher", password="password")
        response = self.client.post(self.url)

        # Vérifier la redirection
        self.assertRedirects(response, reverse("question-list"))

        # Vérifier que le tag a été supprimé
        self.question.refresh_from_db()
        self.assertNotIn(self.tag, self.question.tags.all())

    def test_remove_tag_authenticated_student(self):
        """Tester que l'étudiant ne peut pas supprimer un tag."""
        self.client.login(username="student", password="password")
        response = self.client.post(self.url)

        # Vérifier que l'accès est refusé (Forbidden)
        self.assertEqual(response.status_code, 403)

    def test_remove_tag_not_authenticated(self):
        """Tester que l'accès est refusé si l'utilisateur n'est pas authentifié."""
        response = self.client.post(self.url)

        # Vérifier la redirection vers la page de connexion
        self.assertRedirects(response, f"/login/?next={self.url}")

    def test_remove_tag_question_not_found(self):
        """Tester le comportement lorsque la question n'existe pas."""
        self.client.login(username="teacher", password="password")
        url_invalid = reverse("remove-tag", args=[9999, self.tag.id])  # ID invalide
        response = self.client.post(url_invalid)

        # Vérifier que l'utilisateur reçoit une erreur 404
        self.assertEqual(response.status_code, 404)

    def test_remove_tag_tag_not_found(self):
        """Tester le comportement lorsque le tag n'existe pas."""
        self.client.login(username="teacher", password="password")
        url_invalid = reverse(
            "remove-tag", args=[self.question.id, 9999]
        )  # ID invalide
        response = self.client.post(url_invalid)

        # Vérifier que l'utilisateur reçoit une erreur 404
        self.assertEqual(response.status_code, 404)
