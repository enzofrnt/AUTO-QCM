import logging
from datetime import timedelta

from app.decorators import self_required, teacher_required
from app.models import QCM, Question, ReponseQCM, Utilisateur
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import timezone

logger = logging.getLogger(__name__)


@login_required(login_url=reverse_lazy("login"))
@self_required
@teacher_required
def enseignant_dashboard(request, pk=None):
    enseignant = get_object_or_404(Utilisateur, pk=pk)

    # Récupérer les QCM contenant des questions créées par cet enseignant
    qcms_with_questions = (
        QCM.objects.filter(questions__creator=enseignant)
        .distinct()
        .prefetch_related("reponses_qcm")
        .order_by("-date_modif")[:10]
    )

    # Récupérer les QCM à venir pour les 3 prochains mois
    today = timezone.now().date()
    three_months_later = today + timedelta(days=90)
    upcoming_qcms = QCM.objects.filter(
        Q(date_modif__gte=today) & Q(date_modif__lte=three_months_later)
    ).order_by("date_modif")

    # Récupérer les statistiques des QCM
    total_qcms = QCM.objects.filter(questions__creator=enseignant).distinct().count()
    total_questions = Question.objects.filter(creator=enseignant).count()
    total_responses = (
        ReponseQCM.objects.filter(qcm__questions__creator=enseignant).distinct().count()
    )

    context = {
        "enseignant": enseignant,
        "qcms_with_questions": qcms_with_questions,
        "upcoming_qcms": upcoming_qcms,
        "total_qcms": total_qcms,
        "total_questions": total_questions,
        "total_responses": total_responses,
    }

    return render(request, "dashboard/enseignant_dashboard.html", context)
