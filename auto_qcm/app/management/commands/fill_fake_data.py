from django.core.management.base import BaseCommand
from faker import Faker
from app.models import Question, Tag, Reponse
import random
from django.core.exceptions import ValidationError

class Command(BaseCommand):
    help = 'Remplit la base de données avec des données factices.'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Créer des tags factices
        tags = []
        for _ in range(5):
            tag = Tag.objects.create(
                name=fake.word(),
                color=fake.hex_color()
            )
            tags.append(tag)

        # Créer des questions factices
        questions = []
        for _ in range(10):
            # Choisir un nombre aléatoire de bonnes réponses (y compris zéro)
            number_of_correct_answers = random.choice([0, 1, 2, 3])

            question = Question(
                nom = fake.word(),
                texte=fake.sentence(),
                number_of_correct_answers=number_of_correct_answers
            )
            question.save()
            question.tags.set(fake.random_elements(elements=tags, unique=True))
            questions.append(question)

        # Créer des réponses factices
        for question in questions:
            min_answers = question.number_of_correct_answers + 1
            total_answers = fake.random_int(min=min_answers, max=6)
            correct_answers_needed = question.number_of_correct_answers
            correct_answers_created = 0

            # Créer les bonnes réponses d'abord
            for _ in range(correct_answers_needed):
                Reponse.objects.create(
                    question=question,
                    texte=fake.sentence(),
                    is_correct=True
                )
                correct_answers_created += 1

            # Créer les réponses restantes comme incorrectes
            remaining_answers = total_answers - correct_answers_created
            for _ in range(remaining_answers):
                Reponse.objects.create(
                    question=question,
                    texte=fake.sentence(),
                    is_correct=False
                )

            # Validation de la question après l'ajout des réponses
            try:
                question.full_clean()  # Valide l'objet pour s'assurer que le nombre de bonnes réponses est correct
                question.save()  # Sauvegarde l'objet si la validation passe
            except ValidationError as e:
                self.stdout.write(self.style.ERROR(f"Erreur de validation pour la question '{question.texte}': {e}"))

        self.stdout.write(self.style.SUCCESS('Données factices générées avec succès.'))