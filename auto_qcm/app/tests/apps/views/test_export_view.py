from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from app.models import Question, QCM, Utilisateur, Tag
from django.contrib.auth.models import Group

User = get_user_model()


class ExportViewTests(TestCase):
    def setUp(self):
        # Create a user and assign them to the teacher group
        self.teacher = Utilisateur.objects.create_user(
            username="teacher", email="teacher@example.com", password="password"
        )
        # Get or create the teacher group
        teacher_group, created = Group.objects.get_or_create(name="Enseignant")
        self.teacher.groups.add(teacher_group)

        # Create a student user
        self.student = Utilisateur.objects.create_user(
            username="student", email="student@example.com", password="password"
        )

        student_group, created = Group.objects.get_or_create(name="Etudiant")
        self.student.groups.add(student_group)

        # Create a question to test export functionality
        self.tag = Tag.objects.create(name="Test Tag")
        self.question = Question.objects.create(
            nom="Test Question",
            texte="Ceci est une question test.",
            note=2,
            melange_rep=True,
            creator=self.teacher,
        )
        self.question.tags.add(self.tag)

        # Create a QCM
        self.qcm = QCM.objects.create(
            titre="Test QCM",
            description="Description du QCM",
            creator=self.teacher,
        )
        self.qcm.questions.add(self.question)

    def test_export_question_xml_teacher(self):
        """Test the export_question_xml view for a teacher."""
        self.client.login(username="teacher", password="password")
        url = reverse("question-export-xml", args=[self.question.id])  # Updated URL
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")
        self.assertIn("Content-Disposition", response)
        self.assertTrue(response["Content-Disposition"].startswith("attachment;"))
        self.assertIn(
            f'filename="question_{self.question.id}.xml"',
            response["Content-Disposition"],
        )
        self.assertIn("<question", response.content.decode())  # Ensure XML content

    def test_export_question_xml_student(self):
        """Test the export_question_xml view for a student (should fail)."""
        self.client.login(username="student", password="password")
        url = reverse("question-export-xml", args=[self.question.id])  # Updated URL
        response = self.client.get(url)

        # Ensure access is forbidden for non-teachers
        self.assertEqual(response.status_code, 403)

    def test_export_qcm_xml_teacher(self):
        """Test the export_qcm_xml view for a teacher."""
        self.client.login(username="teacher", password="password")
        url = reverse("qcm-export-xml", args=[self.qcm.id])  # Updated URL
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")
        self.assertIn("Content-Disposition", response)
        self.assertTrue(response["Content-Disposition"].startswith("attachment;"))
        self.assertIn(
            f'filename="qcm_{self.qcm.id}.xml"', response["Content-Disposition"]
        )
        self.assertIn("<quiz", response.content.decode())  # Ensure XML content

    def test_export_qcm_latex_teacher(self):
        """Test the export_qcm_latex view for a teacher."""
        self.client.login(username="teacher", password="password")
        url = reverse("qcm-export-latex", args=[self.qcm.id])  # Updated URL
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/x-latex")
        self.assertIn("Content-Disposition", response)
        self.assertTrue(response["Content-Disposition"].startswith("attachment;"))
        self.assertIn(
            f'filename="qcm_{self.qcm.id}.tex"', response["Content-Disposition"]
        )
        self.assertIn(
            "\\begin{document}", response.content.decode()
        )  # Ensure LaTeX content

    def test_export_qcm_latex_student(self):
        """Test the export_qcm_latex view for a student (should fail)."""
        self.client.login(username="student", password="password")
        url = reverse("qcm-export-latex", args=[self.qcm.id])  # Updated URL
        response = self.client.get(url)

        # Ensure access is forbidden for non-teachers
        self.assertEqual(response.status_code, 403)
