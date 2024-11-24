import logging

from app.models import Question, Tag  # Assurez-vous que vous avez ces modèles
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)


def delete_tag(request, tag_id):
    if request.method == "POST":
        tag = get_object_or_404(Tag, id=tag_id)

        # Dissocier ce tag de toutes les questions associées
        tag.questions.clear()

        # Supprimer le tag de la base de données
        tag.delete()

        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "error"}, status=400)
