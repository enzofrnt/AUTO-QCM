from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from app.models import QCM, ReponseQCM, ReponseQuestion, Reponse
import datetime

@login_required
def repondre_qcm(request, qcm_id):
    qcm = get_object_or_404(QCM, id=qcm_id)
    questions = qcm.questions.all()
    
    for question in questions:
        if question.melange_rep : 
            question.reponses_random = question.reponses.all().order_by('?')
        else : 
            question.reponses_random = question.reponses.all()

    if request.method == 'POST':
        reponse_qcm = ReponseQCM.objects.create(utilisateur=request.user, qcm=qcm, date_reponse=datetime.datetime.now())
        
        for question in questions:
            if question.number_of_correct_answers > 1:
                reponse_ids = request.POST.getlist(f'question_{question.id}')
            else:
                reponse_ids = [request.POST.get(f'question_{question.id}')]
            
            if reponse_ids:
                reponse_question = ReponseQuestion.objects.create(
                    utilisateur=request.user,
                    question=question,
                    date=datetime.datetime.now()
                )
                
                for reponse_id in reponse_ids:
                    if reponse_id:
                        reponse = get_object_or_404(Reponse, id=reponse_id)
                        reponse_question.reponse.add(reponse)

                reponse_qcm.reponses.add(reponse_question)
        
        return redirect('qcm-correct', repqcm_id=reponse_qcm.id)
    
    return render(request, 'qcm/qcm_answer.html', {'qcm': qcm, 'questions': questions})
