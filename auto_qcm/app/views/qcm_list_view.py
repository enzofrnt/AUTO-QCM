from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import QCM, Tag
from django.db.models import Q


class QcmListView(LoginRequiredMixin, ListView):
    model = QCM
    template_name = "qcm/qcm_list.html"
    context_object_name = "qcm"

    def get_queryset(self):
        queryset = super().get_queryset()
        nom_filtre = self.request.GET.get("nom", "")

        # Filtrer par nom de question
        if nom_filtre:
            queryset = queryset.filter(texte__icontains=nom_filtre)

        return queryset.distinct()
