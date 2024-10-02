from django.shortcuts import render, get_object_or_404
from app.models import QCM, ReponseQCM
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


@login_required(login_url=reverse_lazy('login'))
def qcm_responses(request, qcm_id):
    qcm = get_object_or_404(QCM, id=qcm_id)
    reponses = ReponseQCM.objects.filter(qcm=qcm)

    context = {
        'qcm': qcm,
        'reponses': reponses,
    }
    
    return render(request, 'dashboard/reponse_qcm_dashboard.html', context)
