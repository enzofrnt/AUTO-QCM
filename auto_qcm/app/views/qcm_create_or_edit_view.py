from logging import getLogger
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from app.models import QCM, Question, Plage
from app.forms import QcmForm, PlageForm


logger = getLogger(__name__)


@login_required(login_url="login")
def create_or_edit_qcm(request, pk=None):
    if pk:
        qcm = get_object_or_404(QCM, pk=pk)
        selected_questions = qcm.questions.all()
        plages = qcm.plages.all()  # Récupérer les plages liées au QCM
        PlageFormSet = modelformset_factory(
            Plage, form=PlageForm, extra=0, can_delete=True
        )
    else:
        qcm = QCM()
        selected_questions = []
        plages = Plage.objects.none()
        PlageFormSet = modelformset_factory(
            Plage, form=PlageForm, extra=1, can_delete=True
        )

    if request.method == "POST":
        form = QcmForm(request.POST, instance=qcm)
        formset = PlageFormSet(request.POST, queryset=plages)

        if form.is_valid() and formset.is_valid():
            qcm = form.save(commit=False)
            qcm.creator = request.user
            qcm.save()

            # Gérer les questions sélectionnées
            selected_questions = request.POST.getlist("selected_questions")
            qcm.questions.set(selected_questions)
            qcm.save()

            # Sauvegarder les plages
            for formPlage in formset:
                if formPlage.cleaned_data.get("DELETE"):
                    # Si l'utilisateur a coché la suppression, supprimer l'instance
                    if formPlage.instance.pk:
                        formPlage.instance.delete()
                else:
                    # Ignorer les formulaires vides
                    if formPlage.cleaned_data and any(formPlage.cleaned_data.values()):
                        plage = formPlage.save(commit=False)
                        plage.qcm = qcm  # Associer la plage au QCM
                        plage.save()
            return redirect("qcm-list")
        else:
            # Log des erreurs du formulaire principal
            logger.error("Form errors: %s", form.errors)

            # Log des erreurs du formset
            logger.error("Formset errors:")
            for formPlage in formset:
                logger.error(formPlage.errors)

            # Log des erreurs non form spécifiques du formset
            logger.error("Formset non-form errors: %s", formset.non_form_errors())
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
