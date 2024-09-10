from django import forms
from django.forms import inlineformset_factory
from .models import Question, Reponse, Tag


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
        fields = ["texte", "tags", "new_tags"]
        widgets = {
            "tags": forms.CheckboxSelectMultiple(),  # Affichage des tags existants en tant que checkboxes
        }


# Formset pour gérer les réponses associées à une question
ReponseFormSet = inlineformset_factory(
    Question,
    Reponse,
    fields=["texte", "is_correct"],
    extra=1,  # Nombre de formulaires de réponse vierges à afficher par défaut
    can_delete=True,  # Permettre de supprimer des réponses
)
