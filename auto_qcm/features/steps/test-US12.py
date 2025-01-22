from behave import given,when, then
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile


@when("J'envoie un pdf")
def generate_questions(context):

    file_ob = {'file': open('features/TP5 Lecture données-Slug ETU.pdf', 'rb')}
    
    create_url = reverse("generate-questions")
    tmpfile = SimpleUploadedFile(
        "tp5.pdf", file_ob['file'].read(), content_type="application/pdf"
    )
    context.response = context.test.client.post(
                      create_url, {'file': tmpfile}, format='multipart')
    #context.response = context.test.client.post(create_url, FILES=file_ob, format='multipart')
    

@then(u'Les questions "{existe}"')
def check_questions(context, existe):
    assert context.response.status_code != 500, f"Le token OpenAI n'est pas défini / valide (500)"
    if existe=="n'existent pas":
        assert context.response.status_code not in [200, 302], f"La création n'a pas échoué: {context.response.status_code}"
        return
    assert context.response.status_code in [200, 302], f"La création a échoué avec le code {context.response.content}"