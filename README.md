# AUTO-QCM
Ce projet a pour objectif de répondre aux besoins de l’IUT de Blagnac en facilitant la création de QCM afin de simplifier le processus d’évaluation des étudiants.

## Installation

rendez-vous dans le dossier `deploiement-dev` et exécutez la commande `docker-compose up -d --build` pour lancer l'application.
Vous pourrez alors utiliser l'api django en local sur le port `8000` et travailler dessus en allant dans le dossier `auto-qcm` qui contient Django.
Il y a donc deux conteneur qui s'exécutent en parallèle, un pour l'api et un pour la base de données celui de l'api contient déjà AMC qui y est installé.