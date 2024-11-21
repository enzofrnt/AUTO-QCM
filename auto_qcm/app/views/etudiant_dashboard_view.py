import logging
from datetime import datetime, timedelta

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

    # Récupérer la promo et le groupe de l'utilisateur
    promo = utilisateur.promotion
    groupe = utilisateur.groupe

    # Date actuelle
    now = timezone.now()
    today = now.date()

    # Bornes pour la journée
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())

    # Récupérer les réponses existantes de l'utilisateur
    reponse_qcm = ReponseQCM.objects.filter(utilisateur=utilisateur)

    # QCM accessibles via plage (promo, groupe, et plage active aujourd'hui)
    accessible_today_qcms = (
        QCM.objects.filter(
            plages__debut__lte=now,  # Plage ouverte avant maintenant
            plages__fin__gte=now,  # Plage fermée après maintenant
            plages__promo=promo,  # Promo correspondante
            plages__groupe=groupe,  # Groupe correspondant
            est_accessible=True,  # QCM accessible
        )
        # .exclude(id__in=reponse_qcm_ids)
        .distinct()
    )

    # Périodes pour les 3 mois précédents et à venir
    three_months_earlier = today - timedelta(days=90)
    three_months_later = today + timedelta(days=90)

    # QCM à venir ou récents (dans les 3 mois avant ou après) accessibles via plage
    upcoming_qcms = (
        QCM.objects.filter(
            plages__debut__lte=three_months_later,  # Plage commence avant la fin des 3 mois
            plages__fin__gte=three_months_earlier,  # Plage finit après le début des 3 mois
            plages__promo=promo,  # Promo correspondante
            plages__groupe=groupe,  # Groupe correspondant
            est_accessible=True,  # QCM accessible
        )
        # .exclude(id__in=reponse_qcm_ids)
        .distinct().order_by("plages__debut")
    )

    return render(
        request,
        "dashboard/etudiant_dashboard.html",
        {
            "accessible_today_qcms": accessible_today_qcms,
            "upcoming_qcms": upcoming_qcms,
            "reponse_qcm": reponse_qcm,
            "utilisateur": utilisateur,
        },
    )
