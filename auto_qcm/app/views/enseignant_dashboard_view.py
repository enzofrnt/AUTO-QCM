import logging
from datetime import timedelta

from app.decorators import self_required, teacher_required
from app.models import (
    QCM,
    Plage,
    Question,
    ReponseQCM,
    Utilisateur,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
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
    
    # Get the selected year from the query parameters, default to current year
    selected_year = request.GET.get('year', 'all')
    
    # Base query for QCMs with questions created by the teacher
    qcms_query = QCM.objects.filter(questions__creator=enseignant).distinct()
    
    # Apply year filter if a specific year is selected
    if selected_year != 'all':
        try:
            year = int(selected_year)
            qcms_query = qcms_query.filter(date_creation__year=year)
        except ValueError:
            # Handle invalid year parameter
            pass
    
    # Get the filtered and ordered QCMs
    qcms_with_questions = (
        qcms_query
        .prefetch_related("reponses_qcm")
        .order_by("-date_modif")[:10]
    )

    # Get available years for filtering
    years = (QCM.objects
        .filter(questions__creator=enseignant)
        .dates('date_creation', 'year')
        .distinct()
    )
    years = [year.year for year in years]
    
    # Rest of the dashboard data
    today = timezone.now().date()
    three_months_later = today + timedelta(days=90)
    upcoming_qcms = QCM.objects.filter(
        date_modif__gt=today, date_modif__lte=three_months_later
    ).order_by("date_modif")

    total_qcms = QCM.objects.filter(questions__creator=enseignant).distinct().count()
    total_questions = Question.objects.filter(creator=enseignant).count()
    total_responses = (
        ReponseQCM.objects.filter(qcm__questions__creator=enseignant).distinct().count()
    )

    promotions = Group.objects.filter(plagespromo__isnull=False).distinct().order_by("name")
    groupes = Group.objects.filter(plagesgroup__isnull=False).distinct().order_by("name")

    context = {
        "enseignant": enseignant,
        "qcms_with_questions": qcms_with_questions,
        "upcoming_qcms": upcoming_qcms,
        "total_qcms": total_qcms,
        "total_questions": total_questions,
        "total_responses": total_responses,
        "promotions": promotions,
        "groupes": groupes,
        "years": years,
        "selected_year": selected_year,
    }

    return render(request, "dashboard/enseignant_dashboard.html", context)