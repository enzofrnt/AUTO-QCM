from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from app.models import Question, Reponse
from app.forms import QuestionForm, ReponseFormSet

def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        formset = ReponseFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            question = form.save(commit=False)


            question.save()
            formset.instance = question  # Lie le formset à l'objet question
            formset.save()
            #Rediriger avec le name
            return redirect('question-list')

        else:
            print(form.errors, formset.errors)

    else:
        form = QuestionForm()
        formset = ReponseFormSet()

    return render(request, 'questions/question_form.html', {'form': form, 'formset': formset})