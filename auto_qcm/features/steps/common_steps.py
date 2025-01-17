from behave import given
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.urls import reverse


@given("la base de données est remplie avec des données de test")
def step_fill_fake_data(context):
    print("Début du remplissage de la base de données")
    call_command("flush", interactive=False)
    call_command("fill_fake_data")
    print("Fin du remplissage de la base de données")


@given('je suis connecté en tant que "{username}"')
def step_login(context, username):
    context.test.client.logout()
    context.test.client.session.flush()
    print(f"Tentative de connexion pour l'utilisateur: {username}")

    passwords = {
        "prof": "prof",
        "Lois": "LoisLeBeau31",
        "Nathan": "TheBest31",
        "Moquette": "Moquette31",
        "admin": "changeme",
    }

    if username == "admin":
        print("Tentative de première connexion admin")
        success = context.test.client.login(
            username=username, password=passwords[username]
        )
        print(f"Première connexion admin: {'réussie' if success else 'échouée'}")

        if not success:
            print(
                "Échec de la connexion admin - Vérification de l'existence de l'utilisateur"
            )
            from django.contrib.auth import get_user_model

            User = get_user_model()
            admin_user = User.objects.filter(username="admin").first()
            if admin_user:
                print(
                    f"Admin trouvé: {admin_user.username}, must_change_password: {admin_user.must_change_password}"
                )
            else:
                print("Utilisateur admin non trouvé dans la base de données")
                user = User.objects.create_superuser(
                    username="admin",
                    email="admin@example.com",
                    password="changeme",
                    must_change_password=True,
                )

                enseignant_goup, _ = Group.objects.update_or_create(name="Enseignant")
                user.groups.add(enseignant_goup)
                user.save()

                # Nouvelle tentative de connexion après création
                success = context.test.client.login(
                    username=username, password=passwords[username]
                )
                print(
                    f"Connexion après création admin: {'réussie' if success else 'échouée'}"
                )

                if not success:
                    assert (
                        False
                    ), "Impossible de se connecter même après création de l'admin"

        print("Tentative de changement de mot de passe admin")
        response = context.test.client.post(
            reverse("password_change"),
            {
                "old_password": passwords[username],
                "new_password1": "NewAdminPass123",
                "new_password2": "NewAdminPass123",
            },
        )
        print(f"Changement de mot de passe - status code: {response.status_code}")

        context.test.client.logout()
        success = context.test.client.login(
            username=username, password="NewAdminPass123"
        )
        print(
            f"Reconnexion admin avec nouveau mot de passe: {'réussie' if success else 'échouée'}"
        )
    else:
        success = context.test.client.login(
            username=username, password=passwords[username]
        )
        print(
            f"Connexion utilisateur standard {username}: {'réussie' if success else 'échouée'}"
        )

    assert success, f"Échec de la connexion pour l'utilisateur {username}"
    assert context.test.client.session.get("_auth_user_id") is not None


@given("je me deconnecte")
def step_logout(context):
    context.test.client.logout()
    context.test.client.session.flush()


@given("je ne suis pas connecté")
def step_not_logged_in(context):
    context.test.client.logout()
    context.test.client.session.flush()
