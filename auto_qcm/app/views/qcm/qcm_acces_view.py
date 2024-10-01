from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from app.models import QCM


@login_required
def acces_qcm(request, qcm_id):
    qcm = get_object_or_404(QCM, id=qcm_id)
    return render(request, "qcm/qcm_acces.html", {"qcm": qcm})
