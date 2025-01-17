from behave import given, then, when
from django.contrib.auth.models import User
from django.test import Client


@given('I am a student')
def step_given_i_am_a_student(context):
    context.user = User.objects.create_user(username='student', password='password')
    context.client = Client()

@when('I log in')
def step_when_i_log_in(context):
    context.response = context.client.post('/login/', {'username': 'student', 'password': 'password'})

@then('I should have access to all student-specific pages')
def step_then_i_should_have_access_to_all_student_specific_pages(context):
    response = context.client.get('/student-specific-page/')
    assert response.status_code == 200