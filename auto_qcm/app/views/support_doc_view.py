from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def support_doc(request):
    return render(request, 'support_doc/support_doc.html')