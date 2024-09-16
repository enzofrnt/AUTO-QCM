from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from app.models import QCM, ReponseQCM, ReponseQuestion, Question, Reponse

@login_required
def repondre_qcm(request, qcm_id):
    qcm = get_object_or_404(QCM, id=qcm_id)
    questions = qcm.questions.all()
    
    if request.method == 'POST':
        # Créer une nouvelle instance de ReponseQCM
        reponse_qcm = ReponseQCM.objects.create(eleve=request.user, qcm=qcm)
        
        for question in questions:
            reponse_id = request.POST.get(f'question_{question.id}')
            if reponse_id:
                reponse = get_object_or_404(Reponse, id=reponse_id)
                
                # Créer une ReponseQuestion pour chaque question répondue
                reponse_question = ReponseQuestion.objects.create(
                    eleve=request.user.eleve,
                    question=question
                )
                reponse_question.reponse.add(reponse)
                reponse_qcm.reponses.add(reponse_question)
        
        return redirect('')
    
    return render(request, 'qcm/qcm_answer.html', {'qcm': qcm, 'questions': questions})
