from app.models import (
    Question,
    Tag,
    Reponse,
    QCM,
    ReponseQCM,
    ReponseQuestion,
    Utilisateur,
    Plage,
)  # Assurez-vous d'importer le bon modèle
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from faker import Faker
import random
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = "Remplit la base de données avec des données factices."

    def handle(self, *args, **kwargs):

        # Creation des groupes
        prof = Group.objects.create(name="Enseignant")
        eleve = Group.objects.create(name="Etudiant")

        promo1 = Group.objects.create(name="BUT1")
        promo2 = Group.objects.create(name="BUT2")
        promo3 = Group.objects.create(name="BUT3")

        g1a = Group.objects.create(name="1A")
        g1b = Group.objects.create(name="1B")
        g2a = Group.objects.create(name="2A")
        g2b = Group.objects.create(name="2B")
        g3a = Group.objects.create(name="3A")
        g3b = Group.objects.create(name="3B")

        # Création des utilisateurs
        lois = Utilisateur.objects.create_user("Lois", "lois@gmail.com", "LoisLeBeau31")
        nath = Utilisateur.objects.create_user("Nathan", "nath@gmail.com", "TheBest31")
        enzo = Utilisateur.objects.create_user("Enzo", "enzo@gmail.com", "AppleNul12")
        kilian = Utilisateur.objects.create_user(
            "Kilian", "kiki@gmail.com", "BoisUnVerre31"
        )
        moquette = Utilisateur.objects.create_user(
            "Moquette", "moquette@gmail.com", "Moquette31"
        )
        alex = Utilisateur.objects.create_user("Alexi", "alexi@gmail.com", "LPBLPM81")

        lois.groups.add(eleve)
        lois.groups.add(promo1)
        lois.groups.add(g1a)
        lois.save()
        nath.groups.add(prof)
        nath.save()
        enzo.groups.add(eleve)
        enzo.groups.add(promo2)
        enzo.groups.add(g2a)
        enzo.save()
        kilian.groups.add(prof)
        kilian.save()
        moquette.groups.add(eleve)
        moquette.groups.add(promo3)
        moquette.groups.add(g3a)
        moquette.save()
        alex.groups.add(prof)
        alex.save()

        # On cree des utilisateur random pour chaque groupe de chaque promo
        for i in range(3):
            for j in range(6):
                user = Utilisateur.objects.create_user(
                    username=f"User{i}{j}",
                    email=f"User{i}{j}@gmail.com",
                    password=f"User{i}{j}31",
                )
                user.groups.add(eleve)
                user.groups.add(promo1 if i == 0 else promo2 if i == 1 else promo3)
                user.groups.add(
                    g1a
                    if j == 0
                    else (
                        g1b
                        if j == 1
                        else (
                            g2a if j == 2 else g2b if j == 3 else g3a if j == 4 else g3b
                        )
                    )
                )
                user.save()

        Utilisateur.objects.create_superuser(
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
                nom=fake.word(), texte=fake.sentence(), creator=alex
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

        # Créer des QCM factices
        demain = timezone.now()
        for _ in range(10):
            qcm = QCM(
                titre=fake.word(),
                description=fake.text(),
                date_modif=demain,
                creator=alex,
            )
            qcm.save()

            for _ in range(5):
                dateDeb = timezone.make_aware(
                    fake.date_time_this_month(), timezone.get_current_timezone()
                )
                dateFin = dateDeb + timedelta(days=random.randint(1, 10))
                plage = Plage.objects.create(
                    debut=dateDeb,
                    fin=dateFin,
                    promo=random.choice([promo1, promo2, promo3]),
                    groupe=random.choice([g1a, g1b, g2a, g2b, g3a, g3b]),
                    qcm=qcm,
                )
                plage.save()

            qcm.questions.set(fake.random_elements(elements=questions, unique=True))

        # Récupérer un QCM aléatoire
        qcm_random = QCM.objects.order_by("?").first()

        # Créer une instance de ReponseQCM pour Moquette
        rep = ReponseQCM.objects.create(
            utilisateur=moquette, qcm=qcm_random, date_reponse=timezone.now()
        )

        # Récupérer des réponses aléatoires associées aux questions du QCM
        random_questions = qcm_random.questions.all()
        reponses_qcm = []

        for question in random_questions:
            # Sélectionner des réponses aléatoires pour chaque question
            reponses_random = Reponse.objects.filter(question=question).order_by("?")[
                :1
            ]
            reponse_qcm = ReponseQuestion.objects.create(
                utilisateur=moquette, question=question, date=timezone.now()
            )
            reponse_qcm.reponse.set(
                reponses_random
            )  # Associe les réponses aléatoires à la question
            reponse_qcm.save()
            reponses_qcm.append(reponse_qcm)

        rep.reponses.set(reponses_qcm)
        rep.save()

        # Récupérer un QCM aléatoire
        qcm_random = QCM.objects.order_by("?").first()

        # Créer une instance de ReponseQCM pour Moquette
        rep = ReponseQCM.objects.create(
            utilisateur=moquette, qcm=qcm_random, date_reponse=timezone.now()
        )

        # Récupérer des réponses aléatoires associées aux questions du QCM
        random_questions = qcm_random.questions.all()
        reponses_qcm = []

        for question in random_questions:
            # Sélectionner des réponses aléatoires pour chaque question
            reponses_random = Reponse.objects.filter(question=question).order_by("?")[
                :1
            ]
            reponse_qcm = ReponseQuestion.objects.create(
                utilisateur=moquette, question=question, date=timezone.now()
            )
            reponse_qcm.reponse.set(
                reponses_random
            )  # Associe les réponses aléatoires à la question
            reponse_qcm.save()
            reponses_qcm.append(reponse_qcm)

        rep.reponses.set(reponses_qcm)
        rep.save()

        self.stdout.write(
            self.style.SUCCESS("Données factices et QCM générés avec succès.")
        )
