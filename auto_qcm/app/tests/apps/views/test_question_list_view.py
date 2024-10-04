from django.test import TestCase
from django.urls import reverse
from app.models import Utilisateur, Question, Tag
from django.contrib.auth.models import Group


class QuestionListViewTests(TestCase):
    def setUp(self):
        """Création des utilisateurs, des groupes, des questions et des tags pour les tests."""
        # Créer des groupes
        self.teacher_group, _ = Group.objects.get_or_create(name="Enseignant")
        self.student_group, _ = Group.objects.get_or_create(name="Etudiant")

        # Créer un utilisateur enseignant
        self.user_teacher = Utilisateur.objects.create_user(
            username="teacher", email="teacher@example.com", password="password"
        )
        self.user_teacher.groups.add(self.teacher_group)

        # Créer un utilisateur étudiant
        self.user_student = Utilisateur.objects.create_user(
            username="student", email="student@example.com", password="password"
        )
        self.user_student.groups.add(self.student_group)

        # Créer des tags
        self.tag1 = Tag.objects.create(name="Mat")
        self.tag2 = Tag.objects.create(name="Phy")

        # Créer des questions
        self.question1 = Question.objects.create(
            texte="Quelle est la racine carrée de 16 ?",
            nom="Math",
            creator=self.user_teacher,
        )
        self.question1.tags.add(self.tag1)

        self.question2 = Question.objects.create(
            texte="Qu'est-ce que la gravité ?",
            nom="Physique",
            creator=self.user_teacher,
        )
        self.question2.tags.add(self.tag2)

        # URL de la vue de liste des questions
        self.url = reverse(
            "question-list"
        )  # Assurez-vous que ce nom est correct dans vos URLs

    def test_question_list_view_access_for_teacher(self):
        """Test d'accès à la vue Question pour un enseignant."""
        self.client.login(username="teacher", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "questions/question_list.html")
        self.assertContains(response, self.question1.texte)
        self.assertContains(response, self.question2.texte)

    def test_question_list_view_access_for_student(self):
        """Test d'accès à la vue Question pour un étudiant."""
        self.client.login(username="student", password="password")
        response = self.client.get(self.url)
        # S'assurer que les étudiants ne peuvent pas accéder à cette vue
        self.assertEqual(
            response.status_code, 403
        )  # Vérifiez si cela redirige ou retourne une erreur 403

    def test_filter_questions_by_name(self):
        """Test du filtrage des questions par nom."""
        self.client.login(username="teacher", password="password")
        response = self.client.get(self.url, {"nom": "Math"})
        self.assertContains(response, self.question1.texte)
        self.assertNotContains(response, self.question2.texte)

    def test_ajax_request_rendering(self):
        """Test pour s'assurer que les requêtes AJAX renvoient le bon contenu."""
        self.client.login(username="teacher", password="password")
        response = self.client.get(
            self.url, {"nom": "Math"}, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 200)

        # Vérifiez que le contenu contient la question dans le bon format
        self.assertIn(
            self.question1.texte, response.json()["html"]
        )  # Vérifie que le texte de la question est dans la réponse
