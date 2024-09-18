import json
import logging

from app.models import Question, Reponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


@login_required
@csrf_exempt
def save_generated_questions(request):
    if request.method == "POST":
        try:
            # Charger les données JSON du POST
            questions_data = json.loads(request.body)
            logger.error(f"Questions générées : {questions_data}")
            user = request.user  # Récupérer l'utilisateur connecté

            for question_data in questions_data["questions"]:
                question = Question.objects.create(
                    texte=question_data["texte"],
                    nom=question_data["nom"],
                    creator=user,
                )

                for reponse in question_data["reponses"]:
                    Reponse.objects.create(
                        texte=reponse["texte"],
                        is_correct=reponse["is_correct"],
                        question=question,
                    )

            return JsonResponse({"message": "Questions sauvegardées avec succès !"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Requête invalide"}, status=400)
