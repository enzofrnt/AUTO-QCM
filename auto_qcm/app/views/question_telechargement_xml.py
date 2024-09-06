from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import get_object_or_404
from app.models import Question


class QuestionTelechargementView(View):

    def get(self, request, question_id):
        # Récupérer la question en fonction de l'ID
        question = get_object_or_404(Question, id=question_id)

        xml_content = question.convertToXmlSingle()

        response = HttpResponse(xml_content, content_type="application/xml")

        response["Content-Disposition"] = (
            f'attachment; filename="question_{question_id}.xml"'
        )

        return response
