from app.models import QCM
from django.contrib import messages
from django.shortcuts import redirect


def delete_multiple_qcms(request):
    if request.method == "POST":
        selected_qcms = request.POST.getlist("selected_qcms")
        if selected_qcms:
            QCM.objects.filter(id__in=selected_qcms).delete()
            messages.success(
                request, f"{len(selected_qcms)} QCM supprimé(s) avec succès."
            )
        else:
            messages.warning(request, "Aucun QCM sélectionné.")
    return redirect("qcm-list")  # Redirige vers la liste des QCM
