from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.decorators import teacher_required
from django.urls import reverse_lazy


@login_required(login_url=reverse_lazy('login'))
@teacher_required
def search_student(request):
    query = request.GET.get('q')
    if query:
        # Filtrer les utilisateurs qui contiennent la query dans leur nom d'utilisateur et qui sont de type 'etudiant'
        students = User.objects.filter(
            username__icontains=query,
            utilisateur__user_type='Etudiant'
        )
    else:
        # Si aucune query, retourner une liste vide
        students = []

    return render(request, 'dashboard/search_student.html', {
        'students': students,
    })
