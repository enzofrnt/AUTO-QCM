from app.decorators import teacher_or_self_student_required
from app.models import ReponseQCM
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy


@login_required(login_url=reverse_lazy("login"))
# @teacher_or_self_student_required
def corriger_qcm(request, repqcm_id):
    reponse_qcm = get_object_or_404(ReponseQCM, id=repqcm_id)
    qcm = reponse_qcm.qcm
    user = reponse_qcm.utilisateur
    reponses_soumis = reponse_qcm.reponses.all()
    scores = []
    for question in qcm.questions.all():
        score = "0/" + str(question.note)
        for repquestion in reponses_soumis:
            if question == repquestion.question:
                score = str(repquestion.score) + "/" + str(question.note)
        scores.append(score)
    reponsesids = []
    for repquestion in reponses_soumis:
        for reponse in repquestion.reponse.all():
            reponsesids.append(reponse.id)

    context = {
        "reponse_qcm": reponse_qcm,
        "qcm": qcm,
        "scores": scores,
        "reponsesids": reponsesids,
        "user": user,
    }

    return render(request, "qcm/qcm_correction.html", context)
