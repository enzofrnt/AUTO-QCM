from app.decorators import teacher_required
from app.models import QCM
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy


@login_required(login_url=reverse_lazy("login"))
@teacher_required
def delete_qcm(request, qcm_id):
    """Supprime le qcm dont l'id est passé en paramètre."""
    qcm = get_object_or_404(QCM, id=qcm_id)
    qcm.delete()
    return redirect("qcm-list")
