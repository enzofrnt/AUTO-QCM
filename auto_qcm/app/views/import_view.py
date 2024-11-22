from django.http import JsonResponse
import xml.etree.ElementTree as ET
from app.models import Question, Reponse
from django.db import IntegrityError
import re


def import_questions(request):
    """
    Gère l'import de fichier externe pour ajouter des questions à la base de données.
    """
    if request.method == "POST":
        import_type = request.POST.get("import_type")
        uploaded_file = request.FILES.get("file")

        if not uploaded_file:
            return JsonResponse({"error": "Aucun fichier téléchargé"}, status=400)

        nbReussi = 0
        nbEchec = 0
        erreurs = []

        if import_type == "moodle_xml":
            try:
                xmldoc = ET.parse(uploaded_file)
                quiz = xmldoc.getroot()
            except ET.ParseError:
                return JsonResponse(
                    {"error": "Erreur de parsing du fichier XML"}, status=400
                )

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

        elif import_type == "latex_amc":
            with uploaded_file.open() as f:
                file_content = f.read().decode("utf-8")

            # Initialiser les variables pour stocker les informations de la question courante
            question_text = ""
            answers = []
            note = 1.0  # Note par défaut

            # Trouver toutes les questions (questionmult et question simple)
            questions_mult = re.finditer(
                r"\\begin{questionmult}{([^}]+)}([^\\]+)\\bareme{b=([^}]+)}([^\\]+)\\begin{reponses}(.*?)\\end{reponses}",
                file_content,
                re.DOTALL,
            )
            questions_simple = re.finditer(
                r"\\begin{question}{([^}]+)}([^\\]+)\\bareme{b=([^}]+)}([^\\]+)\\begin{reponses}(.*?)\\end{reponses}",
                file_content,
                re.DOTALL,
            )

            def process_question(match, is_mult=True):
                nonlocal nbReussi, nbEchec
                try:
                    # Extraire les informations de la question
                    question_id = match.group(1)
                    question_text = match.group(2).strip() + match.group(4).strip()
                    note = float(match.group(3))
                    reponses_text = match.group(5)

                    # Créer l'objet question
                    questObj = Question.objects.create(
                        nom=(
                            question_text
                            if len(question_text) < 50
                            else f"ImportAmcLatex_{question_id}"
                        ),
                        texte=question_text,
                        note=note,
                        melange_rep=True,
                        creator=request.user,
                    )

                    # Extraire et traiter les réponses
                    bonnes = re.finditer(r"\\bonne{([^}]+)}", reponses_text)
                    mauvaises = re.finditer(r"\\mauvaise{([^}]+)}", reponses_text)

                    # Ajouter les bonnes réponses
                    for bonne in bonnes:
                        Reponse.objects.create(
                            question=questObj,
                            texte=bonne.group(1).strip(),
                            is_correct=True,
                        )

                    # Ajouter les mauvaises réponses
                    for mauvaise in mauvaises:
                        Reponse.objects.create(
                            question=questObj,
                            texte=mauvaise.group(1).strip(),
                            is_correct=False,
                        )

                    nbReussi += 1

                except (AttributeError, ValueError, IntegrityError) as e:
                    erreurs.append(
                        f"Erreur lors de l'importation de la question {question_id}: {str(e)}"
                    )
                    nbEchec += 1

            # Traiter toutes les questions à choix multiples
            for question in questions_mult:
                process_question(question, is_mult=True)

            # Traiter toutes les questions à choix simple
            for question in questions_simple:
                process_question(question, is_mult=False)
        elif import_type == "amc_txt":
            with uploaded_file.open() as f:
                file_content = f.read().decode("utf-8")
                lines = file_content.splitlines()

            question_text = ""
            answers = []

            for line in lines:
                line = line.strip()

                # Détecter le début d'une question (lignes qui commencent par **)
                if line.startswith("**"):
                    if (
                        question_text
                    ):  # Si une question précédente existe, enregistrer-la
                        # Créer l'objet question
                        try:
                            # Si la len du texte est plus grande que 50 on renomme

                            questObj = Question.objects.create(
                                nom=(
                                    question_text
                                    if len(question_text) < 50
                                    else "ImportAmcTxt"
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
                        nom=(
                            question_text if len(question_text) < 50 else "ImportAmcTxt"
                        ),
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
                    erreurs.append(
                        f"Erreur lors de l'importation de la question: {str(e)}"
                    )
                    nbEchec += 1
        else:
            return JsonResponse({"error": "Type d'import invalide"}, status=400)
        # Retourner les résultats
        return JsonResponse(
            {
                "message": "Importation terminée",
                "nbReussi": nbReussi,
                "nbEchec": nbEchec,
                "erreurs": erreurs,
            }
        )

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)
