from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def etudiant_dashboard(request, pk):
    return render(request, 'dashboard/etudiant_dashboard.html')