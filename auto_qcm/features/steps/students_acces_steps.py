from app.models import Utilisateur
from behave import given, then, when
from django.test import Client


@given('I am a student')
def step_given_i_am_a_student(context):
    context.user = Utilisateur.objects.create_user(
        username='student',
        password='password'
    )
    context.client = Client()
    
@when('I log in')
def step_when_i_log_in(context):
    success = context.client.login(
        username='student',
        password='password'
    )
    assert success

@then('I should have access to')
def step_then_i_should_have_access(context):
    for row in context.table:
        url = row[0]
        response = context.client.get(url)
        assert response.status_code == 200, f"Failed to access {url}"