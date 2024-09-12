from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.decorators import teacher_required

@login_required(login_url='login')
@teacher_required
def search_student(request):
    query = request.GET.get('q')
    if query:
        students = User.objects.filter(username__icontains=query)
    else:
        students = []

    return render(request, 'dashboard/search_student.html', {
        'students': students,
    })
