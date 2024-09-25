from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from app.models import QCM, Question, Plage
from app.forms import QcmForm, PlageForm


@login_required(login_url="login")
def create_or_edit_qcm(request, pk=None):
    if pk:
        qcm = get_object_or_404(QCM, pk=pk)
        selected_questions = qcm.questions.all()
        plages = qcm.plages.all()  # Récupérer les plages liées au QCM
    else:
        qcm = QCM()
        selected_questions = []
        plages = Plage.objects.none()

    # Formset pour les plages
    PlageFormSet = modelformset_factory(Plage, form=PlageForm, extra=0, can_delete=True)

    if request.method == "POST":
        form = QcmForm(request.POST, instance=qcm)
        formset = PlageFormSet(request.POST, queryset=plages)

        if form.is_valid() and formset.is_valid():
            qcm = form.save(commit=False)
            qcm.creator = request.user
            qcm.date_modif = timezone.now()
            qcm.save()

            # Gérer les questions sélectionnées
            selected_questions = request.POST.getlist("selected_questions")
            qcm.questions.set(selected_questions)
            qcm.save()

            # Sauvegarder les plages
            for form in formset:
                if form.cleaned_data.get("DELETE"):
                    if form.instance.pk:
                        form.instance.delete()
                else:
                    plage = form.save(commit=False)
                    plage.qcm = qcm
                    plage.save()
            return redirect("qcm-list")
    else:
        form = QcmForm(instance=qcm)
        formset = PlageFormSet(queryset=plages)

    questions = Question.objects.all()

    return render(
        request,
        "qcm/qcm_form.html",
        {
            "form": form,
            "formset": formset,
            "questions": questions,
            "selected_questions": selected_questions,
            "qcm": qcm,
        },
    )
