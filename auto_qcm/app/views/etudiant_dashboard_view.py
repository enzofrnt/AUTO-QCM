from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.decorators import teacher_or_student_own_dashboard_required

@login_required(login_url='login')
@teacher_or_student_own_dashboard_required
def etudiant_dashboard(request, pk):
    return render(request, 'dashboard/etudiant_dashboard.html')