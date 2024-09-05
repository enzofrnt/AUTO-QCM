from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from app.models import Question, Reponse
from app.forms import QuestionForm, ReponseFormSet
from django.core.exceptions import ValidationError
from django.db import transaction
from logging import getLogger

logger = getLogger(__name__)

class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'questions/question_form.html'
    success_url = reverse_lazy('question-list')

    def get_context_data(self, **kwargs):
        """Ajouter le formset des réponses au contexte."""
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ReponseFormSet(self.request.POST)
        else:
            data['formset'] = ReponseFormSet()
        return data

    def form_valid(self, form):
        """Validate both the main form and the formset."""
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            try:
                with transaction.atomic():
                    # Save the question first to ensure it has a primary key
                    self.object = form.save()

                    # Associate the responses with the question
                    formset.instance = self.object
                    formset.save()

                    # Validate the question with the responses attached
                    self.object.clean()  # Call the custom validation
                    self.object.save()  # Save the validated question

            except ValidationError as e:
                form.add_error(None, e)
                return self.form_invalid(form)

            return redirect(self.success_url)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        """Gérer les erreurs de validation pour le formulaire principal et le formset."""
        context = self.get_context_data(form=form)
        return self.render_to_response(context)