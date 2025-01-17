from behave import then, when
from django.urls import reverse


@when('je visite la page "{page}"')
def step_visit_page(context, page):
    user_id = context.test.client.session.get("_auth_user_id", 1)

    urls = {
        "tableau de bord enseignant": reverse("enseignant-dashboard", args=[user_id]),
        "tableau de bord étudiant": reverse("etudiant-dashboard", args=[user_id]),
        "tableau de bord admin": reverse("admin-dashboard"),
        "liste des questions": reverse("question-list"),
        "création de QCM": reverse("qcm-create"),
    }
    print("On va visiter la page : ", urls[page])
    context.response = context.test.client.get(urls[page])


@then('je devrais voir "{resultat}"')
def step_check_response(context, resultat):
    if resultat == "une erreur d'accès 403":
        print("On devrait voir : ", resultat)
        print("On voit : ", context.response.status_code)
        assert context.response.status_code == 403
    elif resultat.startswith("le tableau de bord"):
        assert context.response.status_code == 200
        print("On devrait voir : ", resultat)
        print("On voit : ", context.response.content.decode())


@then("je devrais être redirigé vers la page de connexion")
def step_check_redirection(context):
    assert context.response.status_code == 302
    assert reverse("login") in context.response.url
