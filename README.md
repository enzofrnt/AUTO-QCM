CE PROJET EST EN COURS DE DEVELOPPEMENT ET N'EST PAS ENCORE COMPLETEMENT FONCTIONNEL

# AUTO-QCM
Ce projet a pour objectif de répondre aux besoins de l’IUT de Blagnac en facilitant la création de QCM afin de simplifier le processus d’évaluation des étudiants.

## Installation

***Seul un serveru de dev est disponible pour le moment***

Rendez-vous dans le dossier `deploiement-dev` et lancez la commande `docker-compose up -d --build`.

Ensuite rendez vous dans un terminal dans le conteneur python dans le repertoire `/app` puis lancez les commandes suivantes :

```bash
python manage.py fill_fake_data
```
*Cette commande remplira la base de données avec des données fictives pour tester l'application.*

A partir de là, l'application sera accessible à l'adresse `http://localhost:8000` et permettra de tester les fonctionnalités de l'applications.
