from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count, Q, Avg, F, FloatField
from django.db.models.functions import Cast
from app.models import ReponseQCM, Question, QCM
from app.decorators import self_required, teacher_required
from django.contrib.auth.decorators import login_required
from datetime import timedelta

@login_required(login_url='login')
@self_required
@teacher_required
def enseignant_dashboard(request, pk=None):
    enseignant = get_object_or_404(User, pk=pk)
    
    # Récupérer les QCM contenant des questions créées par cet enseignant
    qcms_with_questions = QCM.objects.filter(questions__creator=enseignant).distinct().prefetch_related('reponses_qcm').order_by('-date')[:10]

    # Récupérer les QCM à venir pour les 3 prochains mois
    today = timezone.now().date()
    three_months_later = today + timedelta(days=90)
    upcoming_qcms = QCM.objects.filter(
        Q(date__gte=today) & Q(date__lte=three_months_later)
    ).order_by('date')

    # Récupérer les statistiques des QCM
    total_qcms = QCM.objects.filter(questions__creator=enseignant).distinct().count()
    total_questions = Question.objects.filter(creator=enseignant).count()
    total_responses = ReponseQCM.objects.filter(qcm__questions__creator=enseignant).distinct().count()

    # Calculer les statistiques pour chaque QCM
    qcms = QCM.objects.filter(questions__creator=enseignant).distinct().prefetch_related('reponses_qcm')
    qcms_stats = []
    for qcm in qcms:
        reponses = qcm.reponses_qcm.all()
        total_responses = reponses.count()
        if total_responses > 0:
            avg_score = sum(reponse.score for reponse in reponses) / total_responses
        else:
            avg_score = 0
        qcms_stats.append({
            'id': qcm.id,
            'titre': qcm.titre,
            'avg_score': avg_score,
            'total_responses': total_responses
        })

    context = {
        'enseignant': enseignant,
        'qcms_with_questions': qcms_with_questions,
        'upcoming_qcms': upcoming_qcms,
        'total_qcms': total_qcms,
        'total_questions': total_questions,
        'total_responses': total_responses,
        'qcms_stats': qcms_stats,
    }

    return render(request, 'dashboard/enseignant_dashboard.html', context)
