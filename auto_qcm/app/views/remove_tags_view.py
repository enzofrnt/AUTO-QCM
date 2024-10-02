from app.decorators import teacher_required
from app.models import Question, Tag
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy


@login_required(login_url=reverse_lazy("login"))
@teacher_required
def remove_tag(request, question_id, tag_id):
    question = get_object_or_404(Question, id=question_id)
    tag = get_object_or_404(Tag, id=tag_id)
    question.tags.remove(tag)
    return redirect("question-list")
