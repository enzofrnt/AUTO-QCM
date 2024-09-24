from django import forms
from django.forms import inlineformset_factory
from django.db.models import Q
from .models import Question, Reponse, QCM, Utilisateur, Plage
from django.contrib.auth.models import Group


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
        fields = ["nom", "texte", "note", "melange_rep", "tags", "new_tags"]
        widgets = {
            "tags": forms.CheckboxSelectMultiple(),  # Affichage des tags existants en tant que checkboxes
            "texte": forms.Textarea(
                attrs={"rows": 5, "cols": 60}
            ),  # plus grand textarea
        }


# Formset pour gérer les réponses associées à une question
ReponseFormSet = inlineformset_factory(
    Question,
    Reponse,
    fields=["texte", "is_correct"],
    extra=1,  # Nombre de formulaires de réponse vierges à afficher par défaut
    can_delete=True,  # Permettre de supprimer des réponses
)


class QcmForm(forms.ModelForm):
    class Meta:
        model = QCM
        fields = ["titre", "description", "date_modif"]
        widgets = {
            "date_modif": forms.DateInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            )
        }


class PlageForm(forms.ModelForm):
    class Meta:
        model = Plage
        fields = ["debut", "fin", "promo", "groupe"]

    def __init__(self, *args, **kwargs):
        super(PlageForm, self).__init__(*args, **kwargs)

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
