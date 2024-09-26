from logging import getLogger

from app.forms import PlageForm, QcmForm
from app.models import QCM, Plage, Question, Tag
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

logger = getLogger(__name__)


@login_required(login_url=reverse_lazy("login"))
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
            selected_question_ids = request.POST.getlist("selected_questions")
            qcm.questions.set(selected_question_ids)
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

    # Gestion du filtrage des questions
    nom_filtre = request.GET.get("nom", "")
    tag_filtre = request.GET.getlist("tags")
    tags = Tag.objects.all()

    questions = Question.objects.all()

    # Filtrer par nom
    if nom_filtre:
        questions = questions.filter(nom__icontains=nom_filtre)

    # Filtrer par tags
    if tag_filtre:
        for tag_name in tag_filtre:
            questions = questions.filter(tags__name__icontains=tag_name)

    questions = questions.distinct()

    # Préparer les IDs des questions sélectionnées pour les utiliser dans le template
    selected_question_ids = [str(q.id) for q in selected_questions]

    context = {
        "form": form,
        "formset": formset,
        "questions": questions,
        "selected_question_ids": selected_question_ids,
        "qcm": qcm,
        "tags": tags,
        "nom_filtre": nom_filtre,
        "tag_filtre": tag_filtre,
    }

    return render(request, "qcm/qcm_form.html", context)
