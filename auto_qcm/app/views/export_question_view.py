from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from app.models import Question
from django.http import HttpResponse
from app.decorators import teacher_required


@login_required(login_url="login")
@teacher_required
def export_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    xml_content = question.convertToXmlSingle()

    response = HttpResponse(xml_content, content_type="application/xml")

    response["Content-Disposition"] = (
        f'attachment; filename="question_{question_id}.xml"'
    )

    return response
