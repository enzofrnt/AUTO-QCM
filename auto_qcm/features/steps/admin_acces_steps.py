from behave import given, then, when
from django.contrib.auth.models import Group
from django.test import Client
from django.urls import reverse, NoReverseMatch
from app.models import Utilisateur

@given('I am a Admin')
def step_given_i_am_a_admin(context):
    username = 'admin_test'
    password = 'password'
    context.client = Client()
    
    Utilisateur.objects.filter(username=username).delete()
    
    admin_group, _ = Group.objects.get_or_create(name="Enseignant")
    
    context.teacher = Utilisateur.objects.create_user(
        username=username,
        password=password
    )
    context.teacher.groups.add(admin_group)
    context.teacher.save()
    
    context.credentials = {
        'username': username,
        'password': password,
        'user_id': context.teacher.id
    }

@when('I log in as admin')
def step_when_i_log_in(context):
    success = context.client.login(
        username=context.credentials['username'],
        password=context.credentials['password']
    )
    assert success, "Failed to login as administrator"
    context.is_authenticated = success

@then('I should have access to admin urls')
def step_then_i_should_have_access(context):
    url_params = {
        '/enseignant-dashboard/': {'pk': context.credentials['user_id']},
        '/etudiant-dashboard/': {'pk': context.credentials['user_id']},
        '/question/list/': {},
        '/qcm/create/': {},
        '/support-doc/': {},
        '/': {}
    }
    for row in context.table:
        url_pattern = row[0]
        try:
            if url_pattern in url_params:
                params = url_params[url_pattern]
                if 'pk' in params:
                    actual_url = url_pattern + str(params['pk']) + '/'
                else:
                    actual_url = url_pattern
            else:
                actual_url = url_pattern
            
            response = context.client.get(actual_url)
            
            assert response.status_code == 200, (
                f"Failed to access {actual_url}\n"
                f"Status code: {response.status_code}\n"
                f"Tested URL: {actual_url}"
            )
            
        except Exception as e:
            assert False, (
                f"Error accessing {url_pattern}: {str(e)}\n"
                f"Attempted URL: {actual_url}"
            )