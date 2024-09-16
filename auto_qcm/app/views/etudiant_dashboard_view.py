from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from app.decorators import teacher_or_student_own_dashboard_required
from app.models import QCM, ReponseQCM

@login_required(login_url='login')
@teacher_or_student_own_dashboard_required
def etudiant_dashboard(request, pk):
    
    # Récupérer les informations nécessaires pour le dashboard
    upcoming_qcms = QCM.objects.filter(date__gte=timezone.now())

    return render(request, 'dashboard/etudiant_dashboard.html', {
        'upcoming_qcms': upcoming_qcms,
    })