from app.models import QCM, ReponseQCM
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone


@login_required
def acces_qcm(request, qcm_id):
    qcm = get_object_or_404(QCM, id=qcm_id)
    reponsesqcm = ReponseQCM.objects.filter(qcm=qcm, utilisateur=request.user).order_by(
        "-date_debut"
    )[:5]
    est_accessible = qcm.est_accessible
    if request.method == "POST":
        if qcm.est_accessible:
            rep_qcm = ReponseQCM.objects.create(
                utilisateur=request.user,
                qcm=qcm,
                date_debut=self.qcm.date_modif,
            )
            return redirect("qcm-answer", qcm_id=qcm_id, rep_id=rep_qcm.id)
    return render(
        request,
        "qcm/qcm_acces.html",
        {"qcm": qcm, "est_accessible": est_accessible, "repqcm": reponsesqcm},
    )
