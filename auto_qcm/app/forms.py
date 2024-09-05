from django import forms
from django.forms import inlineformset_factory
from .models import Question, Reponse, Tag

class QuestionForm(forms.ModelForm):
    number_of_correct_answers = forms.IntegerField(
        required=True,
        min_value=0,
        help_text="Nombre de bonnes réponses possibles.",
        label="Nombre de bonnes réponses"
    )

    class Meta:
        model = Question
        fields = ['texte', 'tags', 'number_of_correct_answers']
        widgets = {
            'tags': forms.CheckboxSelectMultiple,
        }
    
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.all()
        self.fields['tags'].widget.attrs.update({'class': 'form-check-input'})

# Formulaire pour les réponses sans champ de tag
class ReponseForm(forms.ModelForm):
    class Meta:
        model = Reponse
        fields = ['texte', 'is_correct']

# Inline formset pour gérer plusieurs réponses dans le formulaire de question
ReponseFormSet = inlineformset_factory(
    Question, Reponse, form=ReponseForm,
    fields=['texte', 'is_correct'], extra=2, can_delete=True
)