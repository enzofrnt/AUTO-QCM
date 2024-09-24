from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from app.models import Question, Reponse, Tag
from app.forms import QuestionForm, ReponseFormSet
from app.decorators import teacher_required

@login_required(login_url='login')
@teacher_required
def create_or_edit_question(request, pk=None):
    # Si un pk est passé, c'est une modification, sinon c'est une création
    if pk:
        question = get_object_or_404(Question, pk=pk)
    else:
        question = Question()

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = ReponseFormSet(request.POST, instance=question)

        if form.is_valid() and formset.is_valid():
            # Sauvegarder la question
            question = form.save(commit=False)
            question.creator = request.user
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

            # Sauvegarder les réponses associées
            formset.instance = question
            formset.save()

            # Rediriger vers l'URL précédente ou vers une URL par défaut
            next_url = request.POST.get('next', request.META.get('HTTP_REFERER', 'home'))
            return redirect(next_url)

        # Affiche les erreurs de formulaire s'il y en a
        print(form.errors, formset.errors)
    else:
        form = QuestionForm(instance=question)
        formset = ReponseFormSet(instance=question)

    return render(request, 'questions/question_form.html', {
        'form': form,
        'formset': formset,
        'question': question,  # Passer l'objet question pour gérer le titre et le bouton dynamiquement
        'next': request.META.get('HTTP_REFERER', 'question-list')  # Passer la prochaine URL pour redirection
    })
