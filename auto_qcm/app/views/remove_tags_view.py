from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from app.models import Question, Tag
from app.decorators import teacher_required

@login_required(login_url='login')
@teacher_required
def remove_tag(request, question_id, tag_id):
    question = get_object_or_404(Question, id=question_id)
    tag = get_object_or_404(Tag, id=tag_id)
    question.tags.remove(tag)
    return redirect('question-list')