from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count, Q
from app.models import ReponseQCM, Question, QCM
from app.decorators import self_required, teacher_required
from django.contrib.auth.decorators import login_required
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

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
            total_percentage = 0
            
            for reponse in reponses:
                max_score = reponse.score_max if reponse.score_max > 0 else 1  # Éviter la division par zéro
                percentage = (reponse.score / max_score) * 100
                total_percentage += percentage
            
            avg_score_percentage = total_percentage / total_responses  # Moyenne des pourcentages
        else:
            avg_score_percentage = 0

        qcms_stats.append({
            'id': qcm.id,
            'titre': qcm.titre,
            'avg_score_percentage': avg_score_percentage,  # Utilisez le pourcentage moyen ici
            'total_responses': total_responses
        })

        logger.error(f"QCM Stats: {qcms_stats}")

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
