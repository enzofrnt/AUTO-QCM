import json
import os
import sys

import openai


def define_us_of_an_issue(api_key, us, issue_title, issue_body):
    """
    L'objectif de cette fonction est de choisir parmi les user stories celle qui correspond le plus à l'issue.
    À la suite de ce traitement, on retourne en markdown les user stories qui correspondent le plus à l'issue sous la forme :

    # UserStory lié
    - #<id_user_story>
    - #<id_user_story>
    - #<id_user_story>

    api_key : str : OpenAI API key
    us : list : Toutes les user stories sous la forme [{id: 1, title: "En tant que dev..."}, ...]
    issue_title : str : Le titre de l'issue
    issue_body : str : Le corps de l'issue
    """
    if not issue_title or not issue_body:
        return "Erreur: Le titre ou le corps de l'issue est vide."

    endpoint = "https://models.inference.ai.azure.com"
    model_name = "gpt-4o"

    client = openai.OpenAI(
        base_url=endpoint,
        api_key=api_key,  # Clé API passée en paramètre
    )

    # Générer des user stories en fonction du contenu de l'issue
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """
                    Tu vas recevoir une liste de User Stories et une issue (titre + description).
                    Tu dois retourner en markdown le body d'origine de l'issue puis. les User Stories qui correspondent le plus à l'issue fournie.
                    En ce qui concerne le body de l'issue, tu dois le retourner tel quel ou à la limite corriger les fautes d'orthographe.
                    Par contre si le body contenait déjà des User Stories on tines compte de ce qui avait été proposé mais ensuite on retourne les User stories sous notre format donc on ne garde pas l'ancien affichage des User Stories.

                    Tu retourneras sous la forme :

                    <body de l'issue qui ne comporte pas le tiltle n'y les anceinne US>

                    # UserStory lié <!-- ALREADY DONE -->
                    - #<id_user_story>
                    - #<id_user_story>
                    - #<id_user_story>

                    Même si cela semble étrange, il faut trouver à minima une user story ou toutes si c'est trop absurde, qui concernent l'issue. Après, s'il s'agit de tâches très générales dont toute l'application a besoin, il faut toutes les retourner.
                    """,
                },
                {
                    "role": "user",
                    "content": f"Issue Title: {issue_title}\nIssue Body: {issue_body}\nUser Stories: {us}",
                },
            ],
            model=model_name,
            temperature=1,
            max_tokens=1500,  # Ajusté pour éviter de dépasser les limites
            top_p=1,
        )
    except Exception as e:
        return f"Erreur lors de la génération des User Stories via OpenAI : {str(e)}"

    # Extraire le contenu de la réponse
    result = response.choices[0].message.content

    return result


if __name__ == "__main__":
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    issue_number = os.environ.get("ISSUE_NUMBER")
    issue_title = os.environ.get("ISSUE_TITLE")
    issue_body = os.environ.get("ISSUE_BODY")
    us = os.environ.get("US")

    if not all([openai_api_key, issue_number, issue_title, issue_body, us]):
        print("Erreur: Une ou plusieurs variables d'environnement sont manquantes.")
        sys.exit(1)

    try:
        us = json.loads(us)
    except json.JSONDecodeError as e:
        print(f"Erreur lors du décodage du JSON des User Stories: {str(e)}")
        sys.exit(1)

    # Nettoyage des caractères problématiques directement en Python
    issue_title = (
        "".join(c for c in issue_title if ord(c) < 128)
        .replace('"', "")
        .replace("'", "")
    )
    issue_body = (
        "".join(c for c in issue_body if ord(c) < 128).replace('"', "").replace("'", "")
    )

    # Appeler la fonction principale
    result = define_us_of_an_issue(
        api_key=openai_api_key, us=us, issue_title=issue_title, issue_body=issue_body
    )

    # Écrire le résultat dans un fichier pour l'afficher ultérieurement
    with open(".github/workflows/auto_us/result.txt", "w", encoding="utf-8") as f:
        f.write(result)
