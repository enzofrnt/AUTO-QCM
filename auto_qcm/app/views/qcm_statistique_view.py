from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count, Q, Sum
from app.models import ReponseQCM, Question, QCM, ReponseQuestion
from app.decorators import self_required, teacher_required
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.urls import reverse_lazy

import logging

logger = logging.getLogger(__name__)

@login_required(login_url=reverse_lazy('login'))
@self_required
@teacher_required
def qcm_statistics(request, pk=None):
    enseignant = get_object_or_404(User, pk=pk)

    # Récupérer les statistiques des QCM
    qcms = QCM.objects.filter(questions__creator=enseignant).distinct().prefetch_related('reponses_qcm', 'questions')
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

        # Ajouter les statistiques des questions
        questions_stats = []
        question_scores = {question.id: {'total_score': 0, 'total_responses': 0} for question in qcm.questions.all()}

        # Loop through each response to the QCM
        for reponse_qcm in reponses:
            # For each response question related to the QCM response
            for reponse_question in reponse_qcm.reponses.all():
                question_id = reponse_question.question.id
                if question_id in question_scores:
                    question_scores[question_id]['total_responses'] += 1
                    # Access the score from ReponseQuestion
                    question_scores[question_id]['total_score'] += reponse_question.score  # Corrected line

        # Calculate average percentages for each question
        for question in qcm.questions.all():
            total_question_responses = question_scores[question.id]['total_responses']
            if total_question_responses > 0:
                max_question_score = question.note if question.note > 0 else 1  # Éviter la division par zéro
                avg_question_percentage = (question_scores[question.id]['total_score'] / (max_question_score * total_question_responses)) * 100
            else:
                avg_question_percentage = 0
            
            questions_stats.append({
                'id': question.id,
                'nom': question.nom,
                'avg_score_percentage': avg_question_percentage,
                'total_responses': total_question_responses
            })

        qcms_stats.append({
            'id': qcm.id,
            'titre': qcm.titre,
            'avg_score_percentage': avg_score_percentage,
            'total_responses': total_responses,
            'questions_stats': questions_stats,  # Statistiques des questions
        })

    logger.error(f"QCM Stats: {qcms_stats}")

    context = {
        'enseignant': enseignant,
        'qcms_stats': qcms_stats,
    }

    return render(request, 'dashboard/qcm_statistics.html', context)
