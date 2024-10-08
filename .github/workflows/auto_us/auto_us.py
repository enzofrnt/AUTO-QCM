import os

import openai


def define_us_of_an_issue(token, us, issue):
    """
    L'objectif de cette fonciton est de choisir parmis les user story celle qui correspond le plus à l'issue.
    A la suite de ce traitement, on retourne en markdown les user story qui correspondent le plus à l'issue sous la forme :

    # UserStory lié
    - #<id_user_story>
    - #<id_user_story>
    - #<id_user_story>


    token : str : OpenAI token
    us : str : Tout les user story sous la forme {1: "En tant que devellopeur je vuex pouvoir me connecter à l'application", 2: "En tant que devellopeur je vuex pouvoir me connecter à l'application"}
    issue : str : L'issue sous la forme : "CRUD User : CRUD Trouver le moyen de créer un User par defaut en prod #123 Verification"
    """
    endpoint = "https://models.inference.ai.azure.com"
    model_name = "gpt-4o"

    client = openai.OpenAI(
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
                    Tu vas recevoir une liste de User Story, tu dois me retourner en markdown les User Story qui correspondent le plus à l'issue fournie.
                    Tu retourneras les User Story sous la forme :

                    # UserStory lié <!-- ALREADY DONE -->
                    - #<id_user_story>
                    - #<id_user_story>
                    - #<id_user_story>

                    Même si cela semble étrange il faut trouver à minima une user story ou toute si c'est trop absurde, qui concernent l'issue, aprés s'il sagit de taches trés génarales, dont toute l'application a besoin, il faut toute les retourner.
                    """,
                },
                {
                    "role": "user",
                    "content": f"Issue : {issue}\n User Story : {us}",
                },
            ],
            model=model_name,
            temperature=1,
            max_tokens=4096,
            top_p=1,
        )
    except Exception as e:
        print(f"Erreur lors de la génération des questions via OpenAI : {str(e)}")
        exit(1)

    response = response.choices[0].message.content

    print(response)
    return response


# Only for testing
# if __name__ == "__main__":
#     # En tant qu'enseignant je veux avoir accès à toutes les pages qui me sont destinées #63
#     # En tant qu'enseignant, je souhaite établir un lien efficace entre le système de QCM et Moodle/AMC pour automatiser l'intégration des QCM dans la plateforme d'apprentissage. #18
#     # En tant qu'enseignant, je veux pouvoir accéder à un espace de gestion des questions, où je peux modifier, supprimer ou ajouter des questions, pour assurer la qualité et la pertinence des QCM. #17
#     # En tant qu'enseignant, je veux consulter un tableau de bord des résultats des étudiants, avec des statistiques anonymisées ou personnalisées, un historique des résultats, pour mieux évaluer la compréhension des cours. #16
#     # En tant qu'étudiant, je veux pouvoir réaliser les QCM à tout moment pour réviser de manière flexible et autonome. #14
#     # En tant qu'enseignant, je souhaite pouvoir envoyer mes support de cours pour générer automatiquement (IA) des questions à partir de mes supports de cours (texte ou PDF) afin de diversifier et enrichir les QCM. #12
#     # En tant qu'enseignant, je souhaite agréger automatiquement des questions pour générer des QCM de contrôle afin de faciliter l'évaluation des étudiants. #11
#     # En tant qu'étudiant, je veux pouvoir accéder à un tableau de bord interactif me montrant mes progrès, avec un historique des notes, et mes résultats aux QCM pour suivre mon évolution tout au long du semestre. #7
#     # En tant qu'enseignant, je souhaite pouvoir saisir ou envoyer mes questions très simplement afin de créer des QCM de révision hebdomadaires. #6

#     us = {
#         65: "En tant qu'étudiant, je veux avoir accès à toutes les pages qui me sont destinées",
#         18: "En tant qu'enseignant, je souhaite établir un lien efficace entre le système de QCM et Moodle/AMC pour automatiser l'intégration des QCM dans la plateforme d'apprentissage.",
#         17: "En tant qu'enseignant, je veux pouvoir accéder à un espace de gestion des questions, où je peux modifier, supprimer ou ajouter des questions, pour assurer la qualité et la pertinence des QCM.",
#         16: "En tant qu'enseignant, je veux consulter un tableau de bord des résultats des étudiants, avec des statistiques anonymisées ou personnalisées, un historique des résultats, pour mieux évaluer la compréhension des cours.",
#         14: "En tant qu'étudiant, je veux pouvoir réaliser les QCM à tout moment pour réviser de manière flexible et autonome.",
#         12: "En tant qu'enseignant, je souhaite pouvoir envoyer mes support de cours pour générer automatiquement (IA) des questions à partir de mes supports de cours (texte ou PDF) afin de diversifier et enrichir les QCM.",
#         11: "En tant qu'enseignant, je souhaite agréger automatiquement des questions pour générer des QCM de contrôle afin de faciliter l'évaluation des étudiants.",
#         7: "En tant qu'étudiant, je veux pouvoir accéder à un tableau de bord interactif me montrant mes progrès, avec un historique des notes, et mes résultats aux QCM pour suivre mon évolution tout au long du semestre.",
#         6: "En tant qu'enseignant, je souhaite pouvoir saisir ou envoyer mes questions très simplement afin de créer des QCM de révision hebdomadaires.",
#     }
#     define_us_of_an_issue(
#         token=os.getenv("GITHUB_TOKEN"),
#         us=us,
#         issue="CRUD User : CRUD Trouver le moyen de créer un User par defaut en prod #123 Verification",
#     )
