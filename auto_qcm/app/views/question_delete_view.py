from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from app.decorators import teacher_required
from app.models import Question


@login_required(login_url="login")
@teacher_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question.delete()
    return redirect("question-list")
