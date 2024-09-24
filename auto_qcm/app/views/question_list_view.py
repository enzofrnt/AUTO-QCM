from app.mixins import TeacherRequiredMixin
from app.models import Question, Tag
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView


class QuestionListView(TeacherRequiredMixin, ListView):
    model = Question
    template_name = "questions/question_list.html"
    context_object_name = "questions"

    def get_queryset(self):
        queryset = super().get_queryset()
        nom_filtre = self.request.GET.get("nom", "")
        tags_filtre = self.request.GET.getlist(
            "tags"
        )  # Utiliser getlist pour obtenir plusieurs tags

        # Filtrer par nom de question
        if nom_filtre:
            queryset = queryset.filter(nom__icontains=nom_filtre)

        # Filtrer par plusieurs tags (et logique pour avoir tous les tags)
        if tags_filtre:
            # Filtrer les questions qui ont tous les tags sélectionnés
            for tag in tags_filtre:
                queryset = queryset.filter(tags__name__icontains=tag)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = (
            Tag.objects.all()
        )  # Passer les tags au template pour le filtre
        context["nom_filtre"] = self.request.GET.get("nom", "")
        context["tag_filtre"] = self.request.GET.getlist(
            "tags"
        )  # Récupérer plusieurs tags pour la pré-sélection
        return context
