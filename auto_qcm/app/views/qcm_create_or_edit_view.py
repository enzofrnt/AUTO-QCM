from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from app.models import QCM, Question
from app.forms import QcmForm

@login_required(login_url='login')
def create_or_edit_qcm(request,pk = None):
    if pk :
        qcm = get_object_or_404(QCM,pk=pk)
        selected_questions = qcm.questions.all()
    else:
        qcm = QCM()
        selected_questions = []
    if request.method == 'POST':
        form = QcmForm(request.POST,instance=qcm)
        
        if form.is_valid():
            qcm = form.save(commit=False)
            print(request.user)
            qcm.creator = request.user
            qcm.save()

            selected_questions = request.POST.getlist('selected_questions')
            qcm.questions.set(selected_questions)
            qcm.save()

            return redirect('qcm-list')
        print(form.errors)
    else:
        form = QcmForm(instance=qcm)

    #On met tt les questions dans la liste du qcm
    questions = Question.objects.all()

    return render(request, 'qcm/qcm_form.html', {'form': form,"questions":questions,'selected_questions': selected_questions})