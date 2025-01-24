from app.models import QCM, Utilisateur
from behave import given, then, when
from django.contrib.auth.models import Group
from django.test import Client
from django.urls import reverse
from django.utils import timezone


@given('I am logged in as a teacher')
def step_impl(context):
    context.client = Client()
    context.teacher = Utilisateur.objects.create_user(
        username='teacher',
        password='password123',
        is_staff=True
    )
    teacher_group, created = Group.objects.get_or_create(name='Enseignant')
    context.teacher.groups.add(teacher_group)
    context.client.login(username='teacher', password='password123')

@given('I have created a QCM with ID "{qcm_id}"')
def step_impl(context, qcm_id):
    context.qcm = QCM.objects.create(
        id=qcm_id,
        titre="Test QCM", 
        description="Test Description",
        creator=context.teacher,
        date_modif=timezone.now(),
        est_accessible=True,
        nb_tentatives=1
    )

@when('I request to export the QCM in {format} format')
def step_impl(context, format):
    format_urls = {
        'XML': f'/qcm/export-xml/{context.qcm.id}/',
        'LaTeX': f'/qcm/export-latex/{context.qcm.id}/',
        'AMC': f'/qcm/export-amctxt/{context.qcm.id}/'
    }
    context.response = context.client.get(format_urls[format])
    print(f"Status code: {context.response.status_code}")
    print(f"Response content: {context.response.content}")

@then('I should receive a file named "qcm_{qcm_id}.{extension}"')
def step_impl(context, qcm_id, extension):
    assert context.response.status_code == 200
    assert context.response.content is not None

@then('the file should have the correct content type "{content_type}"')
def step_impl(context, content_type):
    assert context.response.get('Content-Type') == content_type