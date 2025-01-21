from app.models import QCM, Plage, Question
from behave import given, then, when
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils import timezone


@when("je crée un nouveau QCM")
def create_new_qcm(context):
    create_url = reverse("qcm-create")
    context.response = context.test.client.get(create_url)


@then("le QCM est crée")
def verify_qcm_creation(context):
    assert context.response.status_code in [
        200,
        302,
    ], f"La création a échoué avec le code {context.response.status_code}"

    new_qcm = QCM.objects.last()
    assert new_qcm is not None, "Le QCM n'a pas été créé"

    assert new_qcm.titre, "Le titre est vide"
    assert new_qcm.description, "La description est vide"
    assert new_qcm.nb_tentatives > 0, "Le nombre de tentatives doit être supérieur à 0"

    assert new_qcm.questions.exists(), "Aucune question n'est associée au QCM"

    plage = new_qcm.plages.first()
    assert plage is not None, "Aucune plage horaire n'a été créée"
    assert plage.debut is not None, "La date de début est vide"
    assert plage.fin is not None, "La date de fin est vide"
    assert plage.promo is not None, "Aucune promo n'est associée"
    assert plage.groupe is not None, "Aucun groupe n'est associé"


@given("QCM créé")
def setup_test_qcm(context):
    # Récupérer l'utilisateur connecté
    context.user = context.test.client.session.get("_auth_user_id")
    User = get_user_model()
    context.user = User.objects.get(id=context.user)

    # Utiliser les groupes existants
    promo = Group.objects.get(name="BUT1")
    groupe = Group.objects.get(name="1A")

    qcm = QCM.objects.create(
        titre="QCM de test",
        description="Description du QCM de test",
        creator=context.user,
    )

    plage = Plage.objects.create(
        debut=timezone.now(),
        fin=timezone.now() + timezone.timedelta(days=1),
        promo=promo,
        groupe=groupe,
        qcm=qcm,
    )

    question1 = Question.objects.create(
        nom="Question 1", texte="Texte de la question 1", creator=context.user
    )
    question2 = Question.objects.create(
        nom="Question 2", texte="Texte de la question 2", creator=context.user
    )

    qcm.questions.set([question1, question2])
    context.qcm = qcm
    context.selected_question = [question1, question2]


@when("je modifie un QCM")
def modify_qcm(context):
    qcm = context.qcm
    plage = qcm.plages.first()

    print(f"Plage: {plage.promo.id} - {plage.groupe.id}")

    form_data = {
        "titre": "test modifié",
        "description": "test1 modifié",
        "nb_tentatives": "1",
        "est_accessible": "on",
        "form-TOTAL_FORMS": "1",
        "form-INITIAL_FORMS": "1",
        "form-MIN_NUM_FORMS": "0",
        "form-MAX_NUM_FORMS": "1000",
        "form-0-debut": "2024-10-10T13:45",
        "form-0-fin": "2024-12-12T12:00",
        "form-0-promo": plage.promo.id,
        "form-0-groupe": plage.groupe.id,
        "form-0-id": str(plage.id),
        "form-__prefix__-debut": "",
        "form-__prefix__-fin": "",
        "form-__prefix__-promo": "",
        "form-__prefix__-groupe": "",
        "form-__prefix__-id": "",
        "selected_questions": [str(q.id) for q in context.selected_question],
    }

    update_url = reverse("qcm-edit", kwargs={"pk": qcm.id})
    context.response = context.test.client.post(update_url, form_data)


@then("le QCM est mis à jour")
def verify_qcm_update(context):
    assert context.response.status_code in [
        200,
        302,
    ], f"La mise à jour a échoué avec le code {context.response.status_code}"

    updated_qcm = QCM.objects.get(id=context.qcm.id)
    assert updated_qcm is not None, "Le QCM n'existe plus"

    assert updated_qcm.titre, "Le titre est vide"
    assert updated_qcm.description, "La description est vide"
    assert (
        updated_qcm.nb_tentatives > 0
    ), "Le nombre de tentatives doit être supérieur à 0"

    assert updated_qcm.questions.exists(), "Aucune question n'est associée au QCM"

    plage = updated_qcm.plages.first()
    assert plage is not None, "La plage horaire n'existe plus"
    assert plage.debut is not None, "La date de début est vide"
    assert plage.fin is not None, "La date de fin est vide"
    assert plage.promo is not None, "Aucune promo n'est associée"
    assert plage.groupe is not None, "Aucun groupe n'est associé"


@when("je supprime un QCM")
def delete_qcm(context):
    context.qcm_id = context.qcm.id
    delete_url = reverse("qcm-delete", kwargs={"qcm_id": context.qcm.id})
    context.response = context.test.client.post(delete_url)


@then("le QCM est supprimé")
def verify_qcm_deletion(context):
    assert context.response.status_code in [
        200,
        302,
    ], f"La suppression a échoué avec le code {context.response.status_code}"

    deleted_qcm_exists = QCM.objects.filter(id=context.qcm_id).exists()
    assert not deleted_qcm_exists, "Le QCM n'a pas été supprimé de la base de données"


@when("je consulte un QCM")
def view_qcm(context):
    qcm_url = reverse("qcm-acces", kwargs={"qcm_id": context.qcm.id})
    context.response = context.test.client.get(qcm_url)


@then("le QCM est affiché")
def verify_qcm_display(context):
    assert (
        context.response.status_code == 200
    ), f"La page n'a pas été chargée correctement (status code: {context.response.status_code})"

    content = context.response.content.decode()
    assert context.qcm.titre in content, "Le titre du QCM n'est pas affiché"
    assert (
        context.qcm.description in content
    ), "La description du QCM n'est pas affichée"
