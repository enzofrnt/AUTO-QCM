from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from app.forms import PlageForm
from app.models import Plage


@login_required(login_url="login")
def create_or_edit_plage(request, plage_id=None):
    """Créer ou éditer une plage"""
    if plage_id:
        plage = get_object_or_404(Plage, id=plage_id)
    else:
        plage = None

    if request.method == "POST":
        form = PlageForm(request.POST, instance=plage)
        if form.is_valid():
            form.save()
            return redirect("plage_list")
    else:
        form = PlageForm(instance=plage)

    return render(request, "plage_form.html", {"form": form, "plage": plage})
