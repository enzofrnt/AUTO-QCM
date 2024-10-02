from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render


@login_required(login_url="login")
def change_password_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(
                request, user
            )  # Met à jour la session pour éviter la déconnexion
            user.must_change_password = (
                False  # Indiquer que le mot de passe a été changé
            )
            user.save()
            messages.success(request, "Votre mot de passe a été changé avec succès.")
            return redirect("home")
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "login.html", {"form": form, "must_change_password": True})
