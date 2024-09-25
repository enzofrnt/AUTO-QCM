from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


@login_required(login_url=reverse_lazy('login'))
def support_doc(request):
    return render(request, 'support_doc/support_doc.html')