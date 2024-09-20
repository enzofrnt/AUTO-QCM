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
    reponses_utilisateur = {}

    for repquestion in reponses_soumis:
        if repquestion not in reponses_utilisateur:
            reponses_utilisateur[repquestion] = []
        for reponse in repquestion.reponse.all():
            reponses_utilisateur[repquestion].append(reponse.id)

    context = {
        'reponse_qcm': reponse_qcm,
        'qcm': qcm,
        'reponses_utilisateur': reponses_utilisateur,
        'user': user
    }
    
    return render(request, 'qcm/qcm_correction.html', context)


def is_int(x):
    '''Verifie si un nombre est un entier, car la fonction is_integer ne marche pas sur les entiers'''
    if(isinstance(x,int)):
        return True
    if x == int(x): 
        return True
    return False
