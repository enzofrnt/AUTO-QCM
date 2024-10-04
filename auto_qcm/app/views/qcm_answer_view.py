from logging import getLogger

from app.models import QCM, Reponse, ReponseQCM, ReponseQuestion
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone

logger = getLogger(__name__)


@login_required
def repondre_qcm(request, qcm_id, rep_id):
    qcm = get_object_or_404(QCM, id=qcm_id)
    if qcm.est_accessible == False:
        return redirect("qcm-acces", qcm_id=qcm_id)
    rep_qcm = get_object_or_404(ReponseQCM, id=rep_id)
    if (
        rep_qcm.utilisateur != request.user
        or rep_qcm.qcm != qcm
        or rep_qcm.date_fin_reponse
    ):
        return redirect("qcm-acces", qcm_id=qcm_id)
    questions = qcm.questions.all()

    for question in questions:
        if question.melange_rep:
            question.reponses_random = question.reponses.all().order_by("?")
        else:
            question.reponses_random = question.reponses.all()

    if request.method == "POST":
        rep_qcm.date_fin_reponse = timezone.now()
        rep_qcm.save()

        for question in questions:
            if question.number_of_correct_answers > 1:
                reponse_ids = request.POST.getlist(f"question_{question.id}")
            else:
                reponse_ids = [request.POST.get(f"question_{question.id}")]

            if reponse_ids:
                reponse_question = ReponseQuestion.objects.create(
                    utilisateur=request.user,
                    question=question,
                    date=timezone.now(),
                )

                for reponse_id in reponse_ids:
                    if reponse_id:
                        reponse = get_object_or_404(Reponse, id=reponse_id)
                        reponse_question.reponse.add(reponse)

                rep_qcm.reponses.add(reponse_question)
                rep_qcm.save()

        return redirect("qcm-correct", repqcm_id=rep_qcm.id)

    return render(request, "qcm/qcm_answer.html", {"qcm": qcm, "questions": questions})
