from django import forms
from django.forms import inlineformset_factory
from .models import Question, Reponse
from django.forms.utils import ErrorDict

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['texte', 'tags', ]

# Formset pour gérer les réponses associées à une question
ReponseFormSet = inlineformset_factory(
    Question, Reponse, 
    fields=['texte', 'is_correct'],
    extra=1,  # Nombre de formulaires de réponse vierges à afficher par défaut
    can_delete=True  # Permettre de supprimer des réponses
)