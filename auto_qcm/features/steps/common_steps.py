from behave import given
from django.core.management import call_command


@given("la base de données est remplie avec des données de test")
def step_fill_fake_data(context):
    call_command("flush", interactive=False)
    call_command("fill_fake_data")


@given('je suis connecté en tant que "{username}"')
def step_login(context, username):
    context.test.client.logout()
    context.test.client.session.flush()

    passwords = {
        "prof": "prof",
        "Lois": "LoisLeBeau31",
        "Nathan": "TheBest31",
        "Moquette": "Moquette31",
    }
    success = context.test.client.login(username=username, password=passwords[username])
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
