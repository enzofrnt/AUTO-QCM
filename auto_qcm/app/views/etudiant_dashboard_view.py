import logging
from datetime import timedelta

from app.decorators import teacher_or_self_student_required
from app.models import QCM, Plage, ReponseQCM, Utilisateur
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import timezone

logger = logging.getLogger(__name__)


@login_required(login_url=reverse_lazy("login"))
@teacher_or_self_student_required
def etudiant_dashboard(request, pk):
    utilisateur = get_object_or_404(Utilisateur, pk=pk)

    # Récupérer les informations nécessaires pour le dashboard

    # Récupérer les réponses au QCM
    reponse_qcm = ReponseQCM.objects.filter(utilisateur=utilisateur)
    reponse_qcm = sorted(reponse_qcm, key=lambda x: x.qcm.date_modif)

    # Récupérer les QCM à venir pour les 3 prochains mois
    today = timezone.now().date()
    three_months_later = today + timedelta(days=90)
    upcoming_qcms = QCM.objects.filter(
        Q(date_modif__gte=today) & Q(date_modif__lte=three_months_later)
    ).order_by("date_modif")

    return render(
        request,
        "dashboard/etudiant_dashboard.html",
        {
            "upcoming_qcms": upcoming_qcms,
            "reponse_qcm": reponse_qcm,
            "utilisateur": utilisateur,
        },
    )
