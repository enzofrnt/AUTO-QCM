from django.utils import timezone
from app.models import Question, QCM, Plage
from behave import given,when, then
from behave.api.pending_step import StepNotImplementedError
from django.urls import reverse
from django.contrib.auth.models import Group


@when('je crée un nouveau question')
def create_question(context):

    form_data = {
            "nom": "TestQuestion",
            "texte": "QuestionText",
        }
    
    create_url = reverse("question-create")
    context.response = context.test.client.post(create_url, form_data)
    

@then(u'le question "{existe}"')
def check_question(context, existe):
    if existe=="n'existe pas":
        assert context.response.status_code not in [200, 302], f"La création n'a pas échoué: {context.response.status_code}"
        new_question = Question.objects.last()
        assert (new_question is None or new_question.nom)
        return
    assert context.response.status_code in [200, 302], f"La création a échoué avec le code {context.response.status_code}"