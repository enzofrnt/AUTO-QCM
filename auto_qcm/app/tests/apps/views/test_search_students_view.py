from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group
from app.models import Utilisateur, Tag, Question, QCM


class SearchStudentViewTests(TestCase):
    def setUp(self):
        # Créer un utilisateur enseignant et l'ajouter au groupe Enseignant
        self.teacher = Utilisateur.objects.create_user(
            username="teacher", email="teacher@example.com", password="password"
        )
        teacher_group, created = Group.objects.get_or_create(name="Enseignant")
        self.teacher.groups.add(teacher_group)

        # Créer un utilisateur étudiant et l'ajouter au groupe Étudiant
        self.student = Utilisateur.objects.create_user(
            username="student", email="student@example.com", password="password"
        )
        student_group, created = Group.objects.get_or_create(name="Etudiant")
        self.student.groups.add(student_group)

        # Créer un tag, une question et un QCM pour le contexte
        self.tag = Tag.objects.create(name="Test Tag")
        self.question = Question.objects.create(
            nom="Test Question",
            texte="Ceci est une question test.",
            note=2,
            melange_rep=True,
            creator=self.teacher,
        )
        self.question.tags.add(self.tag)

        self.qcm = QCM.objects.create(
            titre="Test QCM",
            description="Description du QCM",
            creator=self.teacher,
        )
        self.qcm.questions.add(self.question)

    def test_search_student_access_teacher(self):
        """Test que l'enseignant peut accéder à la vue search_student."""
        self.client.login(username="teacher", password="password")
        response = self.client.get(reverse("search-student"), {"q": "student"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/search_student.html")
        self.assertContains(
            response, "student"
        )  # Vérifier que le nom de l'étudiant est dans la réponse

    def test_search_student_access_student(self):
        """Test que l'étudiant ne peut pas accéder à la vue search_student."""
        self.client.login(username="student", password="password")
        response = self.client.get(reverse("search-student"), {"q": "student"})

        self.assertEqual(response.status_code, 403)  # Attendre un statut Interdit

    def test_search_student_without_query(self):
        """Test que la réponse est vide lorsqu'il n'y a pas de requête."""
        self.client.login(username="teacher", password="password")
        response = self.client.get(reverse("search-student"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/search_student.html")
        self.assertEqual(
            response.context["students"], []
        )  # La liste des étudiants doit être vide

    def test_search_student_no_results(self):
        """Test que la liste des étudiants est vide lorsque la requête ne correspond à aucun étudiant."""
        self.client.login(username="teacher", password="password")
        response = self.client.get(reverse("search-student"), {"q": "nonexistent"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/search_student.html")
        self.assertEqual(
            len(response.context["students"]), 0
        )  # Vérifier que la longueur est 0

    def test_search_student_partial_match(self):
        """Test que la recherche par correspondance partielle fonctionne."""
        self.client.login(username="teacher", password="password")
        response = self.client.get(reverse("search-student"), {"q": "stud"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/search_student.html")
        self.assertContains(
            response, "student"
        )  # Vérifier que le nom de l'étudiant est dans la réponse

    def test_redirect_unauthenticated_user(self):
        """Test que l'utilisateur non authentifié est redirigé vers la page de connexion."""
        response = self.client.get(reverse("search-student"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('search-student')}",
            status_code=302,
            target_status_code=200,
        )
