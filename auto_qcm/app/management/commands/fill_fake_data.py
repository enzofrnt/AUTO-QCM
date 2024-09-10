from django.core.management.base import BaseCommand
from faker import Faker
from app.models import Question, Tag, Reponse
import random
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from app.models.profile import Profile


class Command(BaseCommand):
    help = "Remplit la base de données avec des données factices."

    def handle(self, *args, **kwargs):
        lois = User.objects.create_user("Lois", "lois@gmail.com", "LoisLeBeau31")
        nath = User.objects.create_user("Nathan", "nath@gmail.com", "TheBest31")
        enzo = User.objects.create_user("Enzo", "enzo@gmail.com", "AppleNul12")
        kilian = User.objects.create_user("Kilian", "kiki@gmail.com", "BoisUnVerre31")
        moquette = User.objects.create_user(
            "Moquette", "moquette@gmail.com", "Moquette31"
        )
        alex = User.objects.create_user("Alexi", "alexi@gmail.com", "LPBLPM81")

        Profile.objects.create(user=lois, user_type="Etudiant")
        Profile.objects.create(user=nath, user_type="Enseignant")
        Profile.objects.create(user=enzo, user_type="Etudiant")
        Profile.objects.create(user=kilian, user_type="Enseignant")
        Profile.objects.create(user=moquette, user_type="Etudiant")
        Profile.objects.create(user=alex, user_type="Enseignant")

        User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpassword"
        )

        self.stdout.write(self.style.SUCCESS("Utilisateurs créés avec succès."))

        fake = Faker()

        # Créer des tags factices
        tags = []
        for _ in range(5):
            tag = Tag.objects.create(name=fake.word(), color=fake.hex_color())
            tags.append(tag)

        # Créer des questions factices
        questions = []
        for _ in range(10):
            question = Question(nom=fake.word(), texte=fake.sentence())
            question.save()
            question.tags.set(fake.random_elements(elements=tags, unique=True))
            questions.append(question)

        # Créer des réponses factices
        for question in questions:
            total_answers = fake.random_int(min=0, max=6)
            correct_answers_needed = random.choice(
                range(total_answers + 1)
            )  # Nombre aléatoire de bonnes réponses
            correct_answers_created = 0

            # Créer les bonnes réponses d'abord
            for _ in range(correct_answers_needed):
                Reponse.objects.create(
                    question=question, texte=fake.sentence(), is_correct=True
                )
                correct_answers_created += 1

            # Créer les réponses restantes comme incorrectes
            remaining_answers = total_answers - correct_answers_created
            for _ in range(remaining_answers):
                Reponse.objects.create(
                    question=question, texte=fake.sentence(), is_correct=False
                )

        self.stdout.write(self.style.SUCCESS("Données factices générées avec succès."))
