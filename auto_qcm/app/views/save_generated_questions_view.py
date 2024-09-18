from app.models import Question
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@login_required
@csrf_exempt
def save_generated_questions(request):
    if request.method == "POST":
        questions = request.POST.getlist("questions[]")
        user = request.user  # Récupérer l'utilisateur connecté

        for question_nom in questions:
            # Ajouter le créateur lors de la création de la question
            Question.objects.get_or_create(
                nom=question_nom,
                defaults={
                    "creator": user
                },  # Utiliser l'utilisateur connecté comme créateur
            )

        return JsonResponse({"message": "Questions sauvegardées avec succès !"})

    return JsonResponse({"error": "Requête invalide"}, status=400)
