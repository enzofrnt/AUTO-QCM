from django.test import TestCase
from django.urls import reverse
from app.models import Utilisateur, QCM, Question, Tag, Plage
from django.contrib.auth.models import Group
import logging

# from auto_qcm.app.forms import QcmForm, PlageFormSet


class CreateOrEditQcmViewTests(TestCase):
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
        """Préparation des données pour les tests."""
        # Création d'un utilisateur enseignant
        self.user_teacher = Utilisateur.objects.create_user(
            username="teacher", email="teacher@example.com", password="password"
        )
        self.teacher_group, created = Group.objects.get_or_create(name="Enseignant")
        self.user_teacher.groups.add(self.teacher_group)

        # Création d'un utilisateur étudiant
        self.user_student = Utilisateur.objects.create_user(
            username="student", email="student@example.com", password="password"
        )
        self.student_group, created = Group.objects.get_or_create(name="Etudiant")
        self.user_student.groups.add(self.student_group)

        self.promo_group, created = Group.objects.get_or_create(name="BUT3")
        self.groupe_group, created = Group.objects.get_or_create(name="1A")

        # Création d'une question et d'un tag
        self.question1 = Question.objects.create(
            nom="Question 1", texte="Texte Q1", creator=self.user_teacher
        )
        self.tag1 = Tag.objects.create(name="Tag1")
        self.question1.tags.add(self.tag1)

        # Création d'un QCM existant pour les tests d'édition
        self.qcm = QCM.objects.create(
            titre="QCM Test", description="Description Test", creator=self.user_teacher
        )
        self.qcm.questions.add(self.question1)

        # Création de plage pour ce QCM
        self.plage1 = Plage.objects.create(
            qcm=self.qcm,
            promo=self.promo_group,
            groupe=self.groupe_group,
            debut="2021-01-01 00:00:00",
            fin="2021-01-01 00:00:00",
        )

        # URL pour créer ou éditer un QCM
        self.url_create = reverse("qcm-create")
        self.url_edit = reverse("qcm-edit", args=[self.qcm.pk])

    def test_create_qcm_view_access_for_teacher(self):
        """Test d'accès à la vue de création d'un QCM pour un enseignant."""
        self.client.login(username="teacher", password="password")
        response = self.client.get(self.url_create)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "qcm/qcm_form.html")

    def test_create_qcm_view_access_for_student(self):
        """Test que les étudiants ne peuvent pas accéder à la vue de création de QCM."""
        self.client.login(username="student", password="password")
        response = self.client.get(self.url_create)
        self.assertEqual(response.status_code, 403)

    def test_edit_qcm_view_access_for_teacher(self):
        """Test d'accès à la vue d'édition d'un QCM pour un enseignant."""
        self.client.login(username="teacher", password="password")
        response = self.client.get(self.url_edit)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "qcm/qcm_form.html")
        self.assertContains(response, self.qcm.titre)

    def test_edit_qcm_view_access_for_student(self):
        """Test que les étudiants ne peuvent pas accéder à la vue d'édition de QCM."""
        self.client.login(username="student", password="password")
        response = self.client.get(self.url_edit)
        self.assertEqual(response.status_code, 403)

    def test_create_qcm_post_valid_data(self):
        """Test de création d'un QCM avec des données valides."""
        self.client.login(username="teacher", password="password")
        post_data = {
            "titre": "Nouveau QCM",
            "description": "Description du nouveau QCM",
            "selected_questions": [self.question1.pk],  # Sélection d'une question
            "form-0-debut": "2024-01-01 09:00",
            "nb_tentatives": 3,  # Ajout de la valeur pour nb_tentatives
            "form-0-fin": "2024-01-01 11:00",
            "form-0-promo": self.promo_group.pk,
            "form-0-groupe": self.groupe_group.pk,
            "form-TOTAL_FORMS": "1",
            "form-INITIAL_FORMS": "0",
        }

        response = self.client.post(self.url_create, post_data)

        # Log form errors if there are any
        if response.status_code != 302:  # Not redirected
            print(response.context["form"].errors)
            print(response.context["formset"].errors)

        self.assertEqual(response.status_code, 302)  # Redirection après succès
