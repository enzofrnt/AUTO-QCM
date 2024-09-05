from django.shortcuts import render, redirect
from app.models import Question, Reponse, Tag
from app.forms import QuestionForm, ReponseFormSet

def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        formset = ReponseFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            question = form.save(commit=False)
            question.save()

            # Sauvegarder les tags existants
            form.save_m2m()

            # Traiter les nouveaux tags et leurs couleurs
            new_tags = request.POST.getlist('new_tags[]')
            new_tag_colors = request.POST.getlist('new_tag_colors[]')
            for tag_name, tag_color in zip(new_tags, new_tag_colors):
                if tag_name:  # Vérifier que le tag n'est pas vide
                    tag, created = Tag.objects.update_or_create(name=tag_name.strip(), color=tag_color)
                    question.tags.add(tag)

            formset.instance = question
            formset.save()

            return redirect('question-list')
        else:
            print(form.errors, formset.errors)
    else:
        form = QuestionForm()
        formset = ReponseFormSet()

    return render(request, 'questions/question_form.html', {'form': form, 'formset': formset})