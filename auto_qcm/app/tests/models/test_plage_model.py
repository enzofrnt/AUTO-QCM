from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from django.utils import timezone
from app.models import Plage, QCM, Utilisateur


class PlageModelTest(TestCase):
    def setUp(self):
        # Création des groupes pour les tests
        self.promo_group = Group.objects.create(name="PromoGroup")
        self.groupe_group = Group.objects.create(name="GroupeGroup")

        self.user = Utilisateur.objects.create_user("test", "test@gmail.com", "test")
        self.user.save()

        # Création d'un QCM pour le test
        self.qcm = QCM.objects.create(
            titre="QCM Test",
            description="Description du QCM",
            creator=self.user,
            date_modif=timezone.now(),
        )

        # Création des dates de début et de fin
        self.dateDeb = timezone.make_aware(
            timezone.datetime(2024, 10, 1, 9, 0, 0), timezone.get_current_timezone()
        )
        self.dateFin = timezone.make_aware(
            timezone.datetime(2024, 10, 1, 10, 0, 0), timezone.get_current_timezone()
        )

    def test_create_plage_valid(self):
        """Test la création d'une plage valide."""
        plage = Plage.objects.create(
            debut=self.dateDeb,
            fin=self.dateFin,
            promo=self.promo_group,
            groupe=self.groupe_group,
            qcm=self.qcm,
        )
        self.assertIsInstance(plage, Plage)
        self.assertEqual(plage.promo, self.promo_group)
        self.assertEqual(plage.groupe, self.groupe_group)
        self.assertEqual(plage.debut, self.dateDeb)  # Comparaison avec l'objet datetime
        self.assertEqual(plage.fin, self.dateFin)  # Comparaison avec l'objet datetime

    def test_create_plage_invalid_dates(self):
        """Test la validation lorsque la date de début n'est pas antérieure à la date de fin."""
        plage = Plage(
            debut=self.dateFin,  # Inversion des dates pour provoquer une erreur
            fin=self.dateDeb,
            promo=self.promo_group,
            groupe=self.groupe_group,
            qcm=self.qcm,
        )
        with self.assertRaises(ValidationError) as context:
            plage.clean()  # Appel de la méthode clean pour valider
            plage.save()  # Tentative de sauvegarde
        self.assertIn(
            "La date de début doit être antérieure à la date de fin.",
            str(context.exception),
        )

    def test_str_method(self):
        """Test de la méthode __str__."""
        plage = Plage.objects.create(
            debut=self.dateDeb,
            fin=self.dateFin,
            promo=self.promo_group,
            groupe=self.groupe_group,
            qcm=self.qcm,
        )
        expected_str = f"{self.promo_group.name} - {self.groupe_group.name} ({self.dateDeb} à {self.dateFin})"
        self.assertEqual(str(plage), expected_str)
