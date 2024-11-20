from app.models import QCM, Plage, Question, Reponse
from django import forms
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db.models import Q


class QuestionForm(forms.ModelForm):
    # Champ pour ajouter de nouveaux tags
    new_tags = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Ajouter des tags séparés par des virgules"}
        ),
        help_text="Vous pouvez ajouter plusieurs tags séparés par des virgules.",
    )

    class Meta:
        model = Question
        fields = ["nom", "texte", "note", "melange_rep", "tags", "new_tags","image"]
        widgets = {
            "tags": forms.CheckboxSelectMultiple(),  # Affichage des tags existants en tant que checkboxes
            "texte": forms.Textarea(
                attrs={"rows": 5, "cols": 60}
            ),  # plus grand textarea
        }


class BaseReponseFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        # Vérifier qu'il y a au moins une réponse correcte
        has_correct_answer = False
        for form in self.forms:
            if form.cleaned_data.get("is_correct") and not form.cleaned_data.get(
                "DELETE", False
            ):
                has_correct_answer = True
                break

        if not has_correct_answer:
            raise ValidationError("Il doit y avoir au moins une réponse correcte.")


class QcmForm(forms.ModelForm):
    class Meta:
        model = QCM
        fields = ["titre", "description", "est_accessible", "nb_reponses"]


class PlageForm(forms.ModelForm):
    class Meta:
        model = Plage
        fields = ["debut", "fin", "promo", "groupe"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["debut"].required = True
        self.fields["fin"].required = True
        self.fields["promo"].required = True
        self.fields["promo"].queryset = Group.objects.filter(name__startswith="BUT")

        self.fields["groupe"].queryset = Group.objects.filter(
            Q(name__startswith="1") | Q(name__startswith="2") | Q(name__startswith="3")
        )

        # Widget pr pas mettre un textfield
        self.fields["debut"].widget = forms.DateTimeInput(
            attrs={"type": "datetime-local"}
        )
        self.fields["fin"].widget = forms.DateTimeInput(
            attrs={"type": "datetime-local"}
        )
