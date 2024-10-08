import json
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
    us : dict : Toutes les user stories sous la forme [{id: 1, title: "En tant que dev..."}, ...]
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
                    Tu dois retourner en markdown les User Stories qui correspondent le plus à l'issue fournie.
                    Tu retourneras les User Stories sous la forme :

                    # UserStory lié <!-- ALREADY DONE -->
                    - #<id_user_story>
                    - #<id_user_story>
                    - #<id_user_story>

                    Même si cela semble étrange il faut trouver à minima une user story ou toute si c'est trop absurde, qui concernent l'issue, aprés s'il sagit de taches trés génarales, dont toute l'application a besoin, il faut toute les retourner.
                    """,
                },
                {
                    "role": "user",
                    "content": f"Issue Title: {issue_title}\nIssue Body: {issue_body}\nUser Stories: {us}",
                },
            ],
            model=model_name,
            temperature=1,
            max_tokens=4096,
            top_p=1,
        )
    except Exception as e:
        print(f"Erreur lors de la génération des User Stories via OpenAI : {str(e)}")
        return "Erreur lors de la requête OpenAI"

    return response.choices[0].message.content


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            "Usage: python3 define_us.py <openai_api_key> <issue_number> <issue_title> <issue_body> <user_stories>"
        )
        sys.exit(1)

    openai_api_key = sys.argv[1]
    issue_number = sys.argv[2]
    issue_title = sys.argv[3]
    issue_body = sys.argv[4]
    us = sys.argv[5]

    us = json.loads(us)

    result = define_us_of_an_issue(
        api_key=openai_api_key, us=us, issue_title=issue_title, issue_body=issue_body
    )

    print(result)
