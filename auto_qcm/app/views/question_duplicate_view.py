from logging import getLogger

from app.decorators import teacher_required
from app.models import Question, Reponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

logger = getLogger(__name__)


@login_required(login_url=reverse_lazy("login"))
@teacher_required
def duplicate_question(request, pk):
    quest = get_object_or_404(Question, id=pk)

    new_titre = f"{quest.nom} (copie)"
    new_quest = Question.objects.create(
        nom=new_titre if len(new_titre) <= 50 else quest.nom,
        texte=quest.texte,
        note=quest.note,
        melange_rep=quest.melange_rep,
        creator=request.user,
        image=quest.image,
    )
    new_quest.save()

    new_quest.tags.set(quest.tags.all())

    for reponse in quest.reponses.all():
        new_rep = Reponse.objects.create(
            question=new_quest,
            texte=reponse.texte,
            is_correct=reponse.is_correct,
            creator=request.user,
        )
        new_rep.save()

    return redirect("question-list")
