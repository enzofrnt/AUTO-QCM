from django.http import JsonResponse
import xml.etree.ElementTree as ET
from app.models import Question, Reponse
from django.db import IntegrityError


def import_questions(request):
    if request.method == "POST":
        import_type = request.POST.get("import_type")
        uploaded_file = request.FILES.get("file")

        if not uploaded_file:
            return JsonResponse({"error": "Aucun fichier téléchargé"}, status=400)

        if import_type == "moodle_xml":
            try:
                xmldoc = ET.parse(uploaded_file)
                quiz = xmldoc.getroot()
            except ET.ParseError:
                return JsonResponse(
                    {"error": "Erreur de parsing du fichier XML"}, status=400
                )

            nbReussi = 0
            nbEchec = 0
            erreurs = []
            for question in quiz.findall("question"):
                try:
                    if (
                        question.get("type") == "multichoice"
                        or question.get("type") == "truefalse"
                    ):
                        nom = question.find("name").find("text").text
                        texte = question.find("questiontext").find("text").text
                        note = float(question.find("defaultgrade").text)
                        melange_rep = question.find("shuffleanswers").text == "1"

                        creator = request.user

                        # Créer la question en base de données
                        questObj = Question.objects.create(
                            nom=nom,
                            texte=texte,
                            note=note,
                            melange_rep=melange_rep,
                            creator=creator,
                        )

                        # On trouve les reponses des questions
                        for answer in question.findall("answer"):
                            texte = answer.find("text").text
                            is_correct = float(answer.get("fraction")) > 0
                            Reponse.objects.create(
                                question=questObj, texte=texte, is_correct=is_correct
                            )

                        nbReussi += 1
                    else:
                        erreurs.append("Type de question non supporté")
                        nbEchec += 1
                except (AttributeError, ValueError, IntegrityError) as e:
                    erreurs.append(str(e))
                    nbEchec += 1

            # Retourner les résultats
            return JsonResponse(
                {
                    "message": "Importation terminée",
                    "nbReussi": nbReussi,
                    "nbEchec": nbEchec,
                    "erreurs": erreurs,
                }
            )
        if import_type == "latex_amc":
            # Traiter le fichier LaTeX AMC
            pass
        if import_type == "amc_txt":
            # Traiter le fichier AMC TXT
            pass
        return JsonResponse({"error": "Type d'import invalide"}, status=400)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)
