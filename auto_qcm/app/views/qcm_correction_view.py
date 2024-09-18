from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from app.models import ReponseQCM
from app.decorators import teacher_or_student_own_dashboard_required

@login_required(login_url='login')
@teacher_or_student_own_dashboard_required
def corriger_qcm(request, repqcm_id):
    reponse_qcm = get_object_or_404(ReponseQCM, id=repqcm_id)
    qcm = reponse_qcm.qcm
    user = reponse_qcm.utilisateur
    questions = qcm.questions.all()
    reponses_soumis = reponse_qcm.reponses.all()

    reponses_utilisateur = {}
    for reponse in reponses_soumis:
        question = reponse.question
        if question.id not in reponses_utilisateur:
            reponses_utilisateur[question] = []
        reponses_utilisateur[question].append(reponse)

    context = {
        'qcm': qcm,
        'questions': questions,
        'reponses_utilisateur': reponses_utilisateur,
        'user': user
    }
    
    return render(request, 'qcm/qcm_correction.html', context)
