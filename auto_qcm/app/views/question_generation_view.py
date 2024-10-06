import json
import logging

import PyPDF2
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI

logger = logging.getLogger(__name__)


@csrf_exempt
def question_generation_view(request):
    if request.method == "POST" and request.FILES.get("file"):
        # Récupérer le fichier PDF uploadé
        pdf_file = request.FILES["file"]

        # Sauvegarder le fichier temporairement
        file_path = default_storage.save(f"temp/{pdf_file.name}", pdf_file)

        # Charger les informations d'environnement
        if hasattr(settings, "OPEN_AI_TOKEN"):
            token = settings.OPEN_AI_TOKEN
        else:
            logger.error("Le token OpenAI n'est pas défini dans les settings.")
            return JsonResponse(
                {
                    "error": "Le token OpenAI n'est pas défini. La génération de questions ne peut pas être effectuée."
                },
                status=500,
            )

        # Lire le contenu du fichier PDF
        try:
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                fichier_contenu = ""
                for page in range(len(reader.pages)):
                    fichier_contenu += reader.pages[page].extract_text()

            # Supprimer le fichier temporaire après lecture
            default_storage.delete(file_path)

        except Exception as e:
            logger.error(f"Erreur lors de la lecture du fichier PDF : {str(e)}")
            return JsonResponse(
                {"error": f"Erreur lors de la lecture du fichier PDF : {str(e)}"},
                status=400,
            )

        # Vérification de la longueur du contenu
        len_fichier_contenu = len(fichier_contenu)
        if len_fichier_contenu > 4000:
            logger.warning(
                f"Le contenu du fichier PDF dépasse la limite de 4000 caractères. Il sera tronqué."
            )
        fichier_contenu = fichier_contenu[:4000]

        # Créer une instance du client OpenAI
        endpoint = "https://models.inference.ai.azure.com"
        model_name = "gpt-4o"

        client = OpenAI(
            base_url=endpoint,
            api_key=token,
        )

        # Générer des questions à partir du contenu du fichier PDF
        try:
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": """
                        Je veux que tu retournes en RAW json (Sans inclure les balise markedown) une liste donc un tableau de questions d'une longeurs aléartoire avec un nombre de réponses bonne et mauvsie aléatoires dans une liste sous chaque question.
                        Chaque réponse sera donc objet en json qui contiendra la réponse et un booléen pour indiquer si c'est la bonne réponse ou non.

                        Par exemple :
                        {
                            "nom" : "Nom de la qiestion",
                            "texte" : "Question en elle même",
                            "creator" "Chat j'ai pété",
                            "reponses" : [
                                {
                                    "texte" : "La réponse 1",
                                    "is_correct" : true,
                                    "creator" "Chat j'ai pété"
                                },
                                {
                                    "texte" : "La réponse 2",
                                    "is_correct" : false,
                                    "creator" "Chat j'ai pété"

                                },
                                (...)
                            ]
                        }

                        TU n'imrbique pas les questions dans un objet, tu les retournes directement dans un tableau.
                        """,
                    },
                    {
                        "role": "user",
                        "content": f"A partir du document fourni, génère des questions. Voici le contenu du document : {fichier_contenu}",
                    },
                ],
                model=model_name,
                temperature=1,
                max_tokens=4096,
                top_p=1,
            )
        except Exception as e:
            logger.error(
                f"Erreur lors de la génération des questions via OpenAI : {str(e)}"
            )
            return JsonResponse(
                {"error": f"Erreur lors de la génération des questions : {str(e)}"},
                status=500,
            )

        reponse = response.choices[0].message.content

        try:
            reponse_data = json.loads(reponse.replace("```json", "").replace("```", ""))
        except Exception as e:
            logger.error(
                f"Erreur lors de la conversion de la réponse en JSON : {str(e)}"
            )
            return JsonResponse(
                {
                    "error": f"Erreur lors de la conversion de la réponse en JSON : {str(e)}"
                },
                status=500,
            )

        # Renvoyer la réponse en JSON
        logger.error(f"Questions générées à partir du fichier PDF : \n{reponse_data}")
        return JsonResponse({"questions": reponse_data}, safe=False)

    return JsonResponse({"error": "Aucun fichier n'a été fourni"}, status=400)
