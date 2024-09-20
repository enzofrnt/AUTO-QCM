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
    reponses_soumis = reponse_qcm.reponses.all()
    score = 0
    max_score = 0
    reponses_utilisateur = {}

    for repquestion in reponses_soumis:
        score_question = 0
        question = repquestion.question
        max_score += question.note
        if question not in reponses_utilisateur:
            reponses_utilisateur[question] = ['', []]
        for reponse in repquestion.reponse.all():
            if reponse.is_correct:
                score_question += question.note / question.number_of_correct_answers
            reponses_utilisateur[question][1].append(reponse.id)
        score += score_question
        reponses_utilisateur[question][0] = str(int(score_question)) if is_int(score_question) else f"{score_question:.2f}"

    if is_int(score):
        score_str = str(int(score))
    else:
        score_str = f"{score:.2f}"

    note = f"{score_str}/{max_score}"

    context = {
        'qcm': qcm,
        'reponses_utilisateur': reponses_utilisateur,
        'user': user,
        'note':note
    }
    
    return render(request, 'qcm/qcm_correction.html', context)


def is_int(x):
    '''Verifie si un nombre est un entier, car la fonction is_integer ne marche pas sur les entiers'''
    if(isinstance(x,int)):
        return True
    if x == int(x): 
        return True
    return False
