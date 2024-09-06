from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home(request):
    # Logique de ton application
    toggle_active = True  # ou False selon ta logique

    return render(request, 'home.html', {'toggle_active': toggle_active})