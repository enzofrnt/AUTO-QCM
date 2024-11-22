from django.http import JsonResponse
from logging import getLogger
import xml.etree.ElementTree as ET
from app.models import Question, Reponse
from django.db import IntegrityError
import re

logger = getLogger(__name__)


def import_questions(request):
    """
    Gère l'import de fichier externe pour ajouter des questions à la base de données.
    """
    if request.method == "POST":
        import_type = request.POST.get("import_type")
        uploaded_file = request.FILES.get("file")

        if not uploaded_file:
            return JsonResponse({"error": "Aucun fichier téléchargé"}, status=400)

        if import_type == "moodle_xml":
            return import_xml(uploaded_file, request)
        if import_type == "latex_amc":
            return import_latex_amc(uploaded_file, request)
        if import_type == "amc_txt":
            return import_amc_txt(uploaded_file, request)
        return JsonResponse({"error": "Type d'import invalide"}, status=400)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)


def import_xml(file, request):
    nbReussi = 0
    nbEchec = 0
    erreurs = []
    try:
        xmldoc = ET.parse(file)
        quiz = xmldoc.getroot()
    except ET.ParseError:
        return JsonResponse({"error": "Erreur de parsing du fichier XML"}, status=400)

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
    return JsonResponse(
        {
            "message": "Importation terminée",
            "nbReussi": nbReussi,
            "nbEchec": nbEchec,
            "erreurs": erreurs,
        }
    )


def import_latex_amc(file, request):
    nbReussi = 0
    nbEchec = 0
    erreurs = []
    question_text = ""
    answers = []
    note = 1.0
    in_question = False
    in_reponses = False
    question_name = ""
    with file.open() as f:
        lines = f.read().decode("utf-8").splitlines()

    for line in lines:
        line = line.strip()

        try:
            # Début d'une question
            if "\\begin{question}" in line or "\\begin{questionmult}" in line:
                if question_text and answers:  # Sauvegarder la question précédente
                    try:
                        questObj = Question.objects.create(
                            nom=(
                                question_name
                                if question_name
                                else (
                                    question_text
                                    if len(question_text) < 50
                                    else "ImportAmcLatex"
                                )
                            ),
                            texte=question_text,
                            note=note,
                            melange_rep=True,
                            creator=request.user,
                        )
                        for answer_text, is_correct in answers:
                            Reponse.objects.create(
                                question=questObj,
                                texte=answer_text,
                                is_correct=is_correct,
                            )
                        nbReussi += 1
                    except Exception as e:
                        nbEchec += 1
                        erreurs.append(f"Erreur: {str(e)}")

                # Réinitialiser pour la nouvelle question
                question_text = ""
                answers = []
                note = 1.0
                in_question = True
                try:
                    question_name = line.split("{")[2].split("}")[0].strip()
                except IndexError:
                    question_name = ""

            # Barème
            elif "\\bareme" in line:
                try:
                    note = float(line.split("=")[1].strip().strip("}"))
                except (ValueError, IndexError):
                    note = 1.0

            # Début de la section réponses
            elif "\\begin{reponses}" in line:
                in_reponses = True

            # Fin de la section réponses
            elif "\\end{reponses}" in line:
                in_reponses = False

            # Fin de question
            elif "\\end{question" in line:
                in_question = False

            # Réponse correcte
            elif "\\bonne{" in line:
                if in_reponses:
                    answer_text = line.split("\\bonne{")[1].split("}")[0].strip()
                    answers.append((answer_text, True))

            # Réponse incorrecte
            elif "\\mauvaise{" in line:
                if in_reponses:
                    answer_text = line.split("\\mauvaise{")[1].split("}")[0].strip()
                    answers.append((answer_text, False))

            # Texte de la question
            elif in_question and not in_reponses and line and not line.startswith("\\"):
                question_text += " " + line

        except Exception as e:
            erreurs.append(f"Erreur ligne '{line[:50]}...': {str(e)}")

    # Traiter la dernière question
    if question_text and answers:
        try:
            questObj = Question.objects.create(
                nom=(
                    question_name
                    if question_name
                    else (
                        question_text if len(question_text) < 50 else "ImportAmcLatex"
                    )
                ),
                texte=question_text,
                note=note,
                melange_rep=True,
                creator=request.user,
            )
            for answer_text, is_correct in answers:
                Reponse.objects.create(
                    question=questObj,
                    texte=answer_text,
                    is_correct=is_correct,
                )
            nbReussi += 1
        except Exception as e:
            nbEchec += 1
            erreurs.append(f"Erreur: {str(e)}")

    return JsonResponse(
        {
            "message": "Importation terminée",
            "nbReussi": nbReussi,
            "nbEchec": nbEchec,
            "erreurs": erreurs,
        }
    )


def import_amc_txt(file, request):
    nbReussi = 0
    nbEchec = 0
    erreurs = []
    with file.open() as f:
        file_content = f.read().decode("utf-8")
        lines = file_content.splitlines()

    question_text = ""
    answers = []

    for line in lines:
        line = line.strip()

        # Détecter le début d'une question (lignes qui commencent par **)
        if line.startswith("**"):
            if question_text:  # Si une question précédente existe, enregistrer-la
                # Créer l'objet question
                try:
                    # Si la len du texte est plus grande que 50 on renomme
                    questObj = Question.objects.create(
                        nom=(
                            question_text if len(question_text) < 50 else "ImportAmcTxt"
                        ),
                        texte=question_text,
                        note=1.0,  # Vous pouvez ajuster la note ici
                        melange_rep=True,  # Indiquer si les réponses sont mélangées
                        creator=request.user,
                    )

                    # Ajouter les réponses
                    for answer in answers:
                        texte, is_correct = answer
                        Reponse.objects.create(
                            question=questObj,
                            texte=texte,
                            is_correct=is_correct,
                        )

                    nbReussi += 1
                except (AttributeError, ValueError, IntegrityError) as e:
                    erreurs.append(
                        f"Erreur lors de l'importation de la question: {str(e)}"
                    )
                    nbEchec += 1

            # Réinitialiser pour la nouvelle question
            question_text = line[2:].strip()  # La question est après le `**`
            answers = []
        elif line.startswith("+") or line.startswith("-"):
            # Réponses correctes (+) ou incorrectes (-)
            is_correct = line.startswith("+")
            answer_text = line[1:].strip()  # Enlever le + ou -
            answers.append((answer_text, is_correct))

    # Dernière question à traiter (si le fichier ne se termine pas par un retour à la ligne)
    if question_text:
        try:
            questObj = Question.objects.create(
                nom=(question_text if len(question_text) < 50 else "ImportAmcTxt"),
                texte=question_text,
                note=1.0,  # Vous pouvez ajuster la note ici
                melange_rep=True,  # Indiquer si les réponses sont mélangées
                creator=request.user,
            )

            for answer in answers:
                texte, is_correct = answer
                Reponse.objects.create(
                    question=questObj, texte=texte, is_correct=is_correct
                )

            nbReussi += 1
        except (AttributeError, ValueError, IntegrityError) as e:
            erreurs.append(f"Erreur lors de l'importation de la question: {str(e)}")
            nbEchec += 1

    return JsonResponse(
        {
            "message": "Importation terminée",
            "nbReussi": nbReussi,
            "nbEchec": nbEchec,
            "erreurs": erreurs,
        }
    )
