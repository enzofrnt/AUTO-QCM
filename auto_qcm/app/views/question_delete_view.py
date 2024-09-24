from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from app.decorators import teacher_required
from app.models import Question


@login_required(login_url="login")
@teacher_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question.delete()

    # Récupérer l'URL de la page précédente depuis HTTP_REFERER
    previous_url = request.META.get(
        "HTTP_REFERER", "home"
    )  # Si pas de référent, rediriger vers 'question-list'
    return redirect(previous_url)
