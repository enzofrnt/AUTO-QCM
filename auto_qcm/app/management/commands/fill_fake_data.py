from app.models import (
    Question,
    Tag,
    Reponse,
    QCM,
    ReponseQCM,
    Utilisateur,
)  # Assurez-vous d'importer le bon modèle
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker


class Command(BaseCommand):
    help = "Remplit la base de données avec des données factices."

    def handle(self, *args, **kwargs):
        # Création des utilisateurs
        lois = User.objects.create_user("Lois", "lois@gmail.com", "LoisLeBeau31")
        nath = User.objects.create_user("Nathan", "nath@gmail.com", "TheBest31")
        enzo = User.objects.create_user("Enzo", "enzo@gmail.com", "enzo")
        prof = User.objects.create_user("prof", "prof@gmail.com", "prof")
        kilian = User.objects.create_user("Kilian", "kiki@gmail.com", "BoisUnVerre31")
        moquette = User.objects.create_user(
            "Moquette", "moquette@gmail.com", "Moquette31"
        )
        alex = User.objects.create_user("Alexi", "alexi@gmail.com", "LPBLPM81")

        Utilisateur.objects.create(user=lois, user_type="Etudiant")
        Utilisateur.objects.create(user=nath, user_type="Enseignant")
        Utilisateur.objects.create(user=prof, user_type="Enseignant")
        Utilisateur.objects.create(user=enzo, user_type="Etudiant")
        Utilisateur.objects.create(user=kilian, user_type="Enseignant")
        Utilisateur.objects.create(user=moquette, user_type="Etudiant")
        Utilisateur.objects.create(user=alex, user_type="Enseignant")

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
            question = Question(
                nom=fake.word(), texte=fake.sentence(), creator=User.objects.get(id=6)
            )  # Créateur défini
            question.save()
            question.tags.set(fake.random_elements(elements=tags, unique=True))
            questions.append(question)

        # Créer des réponses factices
        for question in questions:
            # Créer les bonnes réponses d'abord
            for _ in range(random.randint(1, 3)):
                Reponse.objects.create(
                    question=question, texte=fake.sentence(), is_correct=True
                )

            # Créer les réponses restantes comme incorrectes
            for _ in range(random.randint(1, 3)):
                Reponse.objects.create(
                    question=question, texte=fake.sentence(), is_correct=False
                )

        # Créer un QCM avec Alexi comme auteur
        alexi = User.objects.get(id=6)

        # Créer des QCM factices
        demain = datetime.now() + timedelta(days=1)
        for _ in range(10):
            qcm = QCM(
                titre=fake.word(), description=fake.text(), date=demain, creator=alexi
            )
            qcm.save()
            qcm.questions.set(fake.random_elements(elements=questions, unique=True))

        self.stdout.write(
            self.style.SUCCESS("Données factices et QCM générés avec succès.")
        )
