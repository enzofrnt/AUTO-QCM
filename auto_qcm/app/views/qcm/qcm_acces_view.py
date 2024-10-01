from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from app.models import QCM, ReponseQCM
from django.utils import timezone


@login_required
def acces_qcm(request, qcm_id):
    qcm = get_object_or_404(QCM, id=qcm_id)
    if request.method == "POST":
        if qcm.est_accessible:
            rep_qcm = ReponseQCM.objects.create(
                utilisateur=request.user,
                qcm=qcm,
                date_debut=timezone.now(),
            )
            return redirect("qcm-answer", qcm_id=qcm_id, rep_id=rep_qcm.id)
    return render(request, "qcm/qcm_acces.html", {"qcm": qcm})
