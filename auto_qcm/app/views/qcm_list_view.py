from app.mixins import TeacherRequiredMixin
from app.models import QCM, Tag
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import ListView


class QcmListView(TeacherRequiredMixin, ListView):
    model = QCM
    template_name = "qcm/qcm_list.html"
    context_object_name = "qcms"

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    