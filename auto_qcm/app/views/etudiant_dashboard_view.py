from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from app.decorators import teacher_or_self_student_required
from app.models import QCM, ReponseQCM, Utilisateur
from django.db.models import Q
from django.urls import reverse_lazy

from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


@login_required(login_url=reverse_lazy("login"))
@teacher_or_self_student_required

def etudiant_dashboard(request, pk):
    utilisateur = get_object_or_404(Utilisateur, pk=pk)

    # Récupérer les informations nécessaires pour le dashboard

    # Récupérer les réponses au QCM
    reponse_qcm = ReponseQCM.objects.filter(utilisateur=utilisateur)
    reponse_qcm = sorted(reponse_qcm, key=lambda x: x.qcm.date)

    # Récupérer les QCM à venir pour les 3 prochains mois
    today = timezone.now().date()
    three_months_later = today + timedelta(days=90)
    upcoming_qcms = QCM.objects.filter(

        Q(date__gte=today) & Q(date__lte=three_months_later)
    ).order_by('date')

    logger.error(utilisateur)


    return render(request, 'dashboard/etudiant_dashboard.html', {
        'upcoming_qcms': upcoming_qcms,
        'reponse_qcm': reponse_qcm,
        'utilisateur': utilisateur,
    })

