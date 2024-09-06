from django.shortcuts import get_object_or_404, redirect
from app.models import Question

def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question.delete()
    return redirect('question-list')