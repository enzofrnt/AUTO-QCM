from django.test import TestCase
from django.contrib.auth.models import Group
from app.models import Utilisateur


class UtilisateurModelTest(TestCase):
    def setUp(self):
        # Création d'un utilisateur de test
        self.user = Utilisateur.objects.create_user(
            "testuser", "test@gmail.com", "test"
        )

        # Création de groupes
        self.tutor_group = Group.objects.create(name="Enseignant")
        self.promo_group = Group.objects.create(name="BUT1")
        self.first_group = Group.objects.create(name="1A")
        self.second_group = Group.objects.create(name="2A")
        self.third_group = Group.objects.create(name="3A")

    def test_is_tutor(self):
        """Test si l'utilisateur est un enseignant."""
        self.assertFalse(
            self.user.is_tutor
        )  # L'utilisateur ne doit pas être enseignant par défaut

        # Ajout de l'utilisateur au groupe Enseignant
        self.user.groups.add(self.tutor_group)
        self.assertTrue(self.user.is_tutor)  # L'utilisateur doit être enseignant

    def test_promotion(self):
        """Test de la propriété promotion."""
        # L'utilisateur ne fait partie d'aucun groupe de promotion
        self.assertEqual(self.user.promotion, "Erreur")

        # Ajout de l'utilisateur au groupe BUT1
        self.user.groups.add(self.promo_group)
        self.assertEqual(self.user.promotion.name, "BUT1")  # Promotion doit être 'BUT1'

    def test_groupe(self):
        """Test de la propriété groupe."""
        # Débogage de la propriété groupe
        self.assertEqual(
            self.user.groupe, "Erreur"
        )  # L'utilisateur ne fait partie d'aucun groupe de niveau

        # Ajout de l'utilisateur au groupe de niveau 3
        self.user.groups.add(self.third_group)
        self.assertEqual(self.user.groupe.name, "3A")  # Groupe doit être 'BUT3'

        # Ajout d'un utilisateur à un groupe de niveau 2
        self.user.groups.clear()
        self.user.groups.add(self.second_group)
        self.assertEqual(self.user.groupe.name, "2A")  # Groupe doit être 'BUT2'

        # Ajout d'un utilisateur à un groupe de niveau 1
        self.user.groups.clear()
        self.user.groups.add(self.first_group)
        self.assertEqual(self.user.groupe.name, "1A")  # Groupe doit être 'BUT1'

    def test_str_method(self):
        """Test de la méthode __str__."""
        self.assertEqual(
            str(self.user), "testuser - False"
        )  # Vérification de la méthode __str__ par défaut

        # Ajout de l'utilisateur au groupe Enseignant
        self.user.groups.add(self.tutor_group)
        self.assertEqual(
            str(self.user), "testuser - True"
        )  # Vérification après avoir ajouté le groupe
