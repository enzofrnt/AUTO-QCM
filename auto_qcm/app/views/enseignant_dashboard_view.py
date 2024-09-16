# views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import redirect
from app.models import ReponseQCM, Question, QCM
from app.decorators import self_required, teacher_required
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
@self_required
@teacher_required
def enseignant_dashboard(request, pk=None):
    enseignant = get_object_or_404(User, pk=pk)

    # Récupérer les informations nécessaires pour le dashboard
    reponses = ReponseQCM.objects.all()  # Par exemple, les QCM créés par l'enseignant
    questions = Question.objects.filter(creator=enseignant)
    upcoming_qcms = QCM.objects.filter(date__gte=timezone.now())
    
    return render(request, 'dashboard/enseignant_dashboard.html', {
        'enseignant': enseignant,
        'reponses': reponses,
        'questions': questions,
        'upcoming_qcms': upcoming_qcms,
    })
