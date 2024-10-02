from django.test import TestCase
from app.models import Tag
from django.core.exceptions import ValidationError


class TagModelTest(TestCase):
    def setUp(self):
        # Création d'un tag valide
        self.valid_tag = Tag.objects.create(name="Tag Test", color="#FF5733")

    def test_tag_creation(self):
        """Test de la création d'un tag."""
        self.assertIsInstance(self.valid_tag, Tag)
        self.assertEqual(self.valid_tag.name, "Tag Test")
        self.assertEqual(self.valid_tag.color, "#FF5733")

    def test_str_method(self):
        """Test de la méthode __str__."""
        self.assertEqual(str(self.valid_tag), "Tag Test")

    def test_color_default(self):
        """Test de la couleur par défaut."""
        tag = Tag.objects.create(name="Tag Default")
        self.assertEqual(tag.color, "#FFFFFF")

    def test_invalid_color_format(self):
        """Test d'un format de couleur hexadécimale invalide."""
        tag = Tag(name="Invalid Tag", color="invalid_color")
        with self.assertRaises(ValidationError):
            tag.full_clean()  # Utiliser full_clean pour valider l'objet avant la sauvegarde

    def test_too_long_color(self):
        """Test d'un format de couleur hexadécimale trop long."""
        tag = Tag(name="Too Long Tag", color="#FF573322")
        with self.assertRaises(ValidationError):
            tag.full_clean()  # Utiliser full_clean pour valider l'objet avant la sauvegarde
