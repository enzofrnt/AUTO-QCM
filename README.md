⚠️ CE PROJET EST EN COURS DE DEVELOPPEMENT ET N'EST PAS ENCORE COMPLETEMENT FONCTIONNEL
# Auto-QCM

<img width="100" alt="image" src="https://github.com/user-attachments/assets/436af0a7-9046-41da-a632-bf32059e6af6">
<img height="100" alt="image" src="https://github.com/user-attachments/assets/71909bfd-2626-46bd-9789-cfe974416b62">


## Contexte

À l'IUT de Blagnac, les enseignants avaient mis en place un système de QCM hebdomadaires via un outil dédié pour aider les étudiants à réviser leurs cours et suivre leur progression. Ces QCM constituaient un outil précieux pour les enseignants comme pour les élèves, permettant d'assurer un apprentissage continu. Toutefois, à la rentrée 2024, ce dispositif a été abandonné en raison du temps considérable qu'il nécessitait et du manque de ressources pour le maintenir en place.

## Objectifs du projet

Face à cette situation, un nouveau projet a vu le jour au sein du département informatique de l'IUT de Blagnac. Ce projet ambitieux vise à relancer les QCM hebdomadaires, mais cette fois en automatisant le processus grâce entre autres à l'intelligence artificielle. L'objectif est de simplifier la gestion des QCM tout en offrant une expérience plus enrichissante pour les enseignants et les étudiants.

### Fonctionnalités principales

Les principales fonctionnalités de ce projet incluent :

- La création d'un outil permettant aux enseignants de soumettre des questions facilement,
- Le regroupement des questions de la semaine,
- La génération automatique d'un fichier PDF pour les contrôles,
- La conservation des questions dans une base de données pour une réutilisation ultérieure.

De plus, le projet prévoit l'intégration de modèles de langage (LLM), tels que GPT ou Claude, pour permettre aux enseignants de générer des questions à partir de textes ou de documents PDF.

### Tableaux de bord et suivi

Un autre volet du projet est la mise en place de tableaux de bord :

- Un tableau pour les enseignants, afin de suivre la progression des étudiants,
- Un tableau pour les étudiants, où ils pourront consulter leurs réponses.

À terme, il est envisagé d'intégrer ce système de QCM avec Moodle, offrant ainsi une solution complète et pratique pour l'IUT.

## Perspectives d'avenir

Si ce projet s'avère fructueux, il pourrait bien être adopté par d'autres établissements au-delà de l'IUT de Blagnac. Ce projet marque un tournant dans la manière dont les évaluations peuvent être gérées, allégeant la charge de travail des enseignants tout en maintenant un suivi pédagogique de qualité pour les étudiants.

## Notre équipe

- [Nathan Pagnucco](https://github.com/November304)
- [loispacqueteau](https://github.com/loispacqueteau)
- [Enzo Fournet](https://github.com/enzofrnt)
- [Anthony DECLIPPEL](https://github.com/KeynoIX)
- [Alexi Fontanilles](https://github.com/AlexiFon)
- [Kilian Boivert](https://github.com/Kilianspore)

## Technologies utilisées

---

- **Django**

<a href="https://www.djangoproject.com/">
  <img src="https://skillicons.dev/icons?i=django" alt="Logo Django" width="100" height="100">
</a>

Django est un framework Python idéal pour la construction d'APIs, grâce à sa capacité à accélérer le développement tout en assurant une haute qualité et une sécurité robuste. Son architecture « batteries incluses » propose une multitude d'outils intégrés et privilégie une approche DRY (Don't Repeat Yourself) pour minimiser le code répétitif. De plus, Django facilite les interactions avec la base de données grâce à son ORM (Object-Relational Mapping), rendant les tâches complexes plus gérables et plus efficaces. En outre, Django est hautement personnalisable et extensible, ce qui le rend approprié pour des projets de toute envergure. Enfin, le fait qu'Enzo utilise déjà beaucoup ce framework durant son alternance cela représente un avantage significatif pour notre efficacité.

---

- **PostgreSQL**

<a href="https://www.postgresql.org/">
  <img width="100" alt="postgresql" src="https://github.com/user-attachments/assets/055be4c3-9a05-409d-a379-c58ba41592b2">
</a>


PostgreSQL est un système de gestion de bases de données relationnelles reconnu pour sa robustesse et sa conformité stricte aux standards SQL. Il offre des fonctionnalités avancées comme les transactions ACID, la gestion des versions de ligne, et la réplication, ce qui le rend particulièrement adapté pour des applications nécessitant une haute disponibilité et une intégrité des données. L'un des avantages majeurs de PostgreSQL réside dans son extensibilité, permettant d'ajouter des fonctions personnalisées ou des types de données complexes.

De plus, PostgreSQL se distingue par sa compatibilité avec divers langages de programmation, facilitant l'intégration avec des frameworks comme Django grâce à son support natif. Enzo a déjà une solide expérience dans la gestion de bases de données, et la familiarité avec PostgreSQL assure une mise en œuvre efficace et rapide dans notre projet, garantissant ainsi une manipulation sécurisée et optimisée des données.

---

- **Docker**

<a href="https://www.docker.com/">
  <img src="https://skillicons.dev/icons?i=docker" alt="Logo Docker" width="100" height="100">
</a>

Docker, utilisé conjointement avec Dockerfile et Docker Compose, est un outil essentiel pour le déploiement de conteneurs. Il facilite le déploiement d'applications dans des conteneurs, qui sont des environnements isolés et indépendants. Cette méthode permet de déployer des applications de manière simple, rapide et efficace, tout en assurant leur accessibilité. L'un des principaux atouts de Docker est sa capacité à déployer des applications sur divers systèmes d'exploitation, incluant Windows, Linux et MacOS. Cette polyvalence est particulièrement bénéfique pour notre projet, qui nécessite une compatibilité multiplateforme. De plus, Docker assure un déploiement sécurisé des applications, un aspect crucial pour la fiabilité de notre projet.
L'expérience préalable d'Enzo avec Docker représente un avantage notable, augmentant ainsi notre efficacité dans l'utilisation de cet outil. En somme, Docker apparaît comme une solution idéale pour répondre aux besoins spécifiques de notre projet.
En outre, l'avantage supplémentaire réside dans le fait qu'Emilien a déjà une certaine expérience avec Vue.js, ce qui facilite grandement l'intégration et le développement rapide de notre projet. Sa familiarité préalable avec le framework assure une courbe d'apprentissage plus douce pour l'équipe et contribue à une mise en œuvre plus efficace de l'application.

## Architecture du projet

<img width="400" alt="image" src="https://github.com/user-attachments/assets/34c9b13c-2840-4377-9a82-e7db23a97aa0">

L’architecture que nous avons conçue est un modèle de déploiement moderne qui exploite la puissance et la flexibilité des conteneurs Docker, en utilisant un Dockerfile et Docker Compose pour orchestrer notre application Django et sa base de données PostgreSQL. Cette approche nous permet de gérer efficacement l’intégration entre ces deux services essentiels. Les variables d’environnement sont centralisées via un fichier .env afin de garantir une configuration uniforme et synchronisée.

L’application repose sur deux conteneurs principaux : le premier est dédié à PostgreSQL, qui sert de base de données relationnelle fiable et performante pour gérer toutes les données de l’application. Le second est le conteneur Django, qui constitue le back-end de l’application web. Ce conteneur est construit à l’aide d’un Dockerfile personnalisé, qui prépare l’environnement nécessaire pour exécuter notre application.

La persistance des données est assurée par des volumes Docker, ce qui permet de garantir la sauvegarde et la réutilisation des données, même en cas de redémarrage des conteneurs. Cela facilite également le développement local, car les fichiers de l’application peuvent être synchronisés entre l’hôte et le conteneur, offrant un flux de travail fluide pour les développeurs.

Le fichier docker-compose.yml joue un rôle central dans cette architecture, en définissant les services (Django et PostgreSQL), en orchestrant la construction des images Docker et en gérant le démarrage des conteneurs. Il garantit également une communication transparente entre le back-end Django et la base de données PostgreSQL, assurant ainsi le bon fonctionnement de l’application.

Cette architecture offre une simplicité de déploiement, une évolutivité et une séparation claire des responsabilités entre les composants, rendant le système facile à maintenir et à faire évoluer. En utilisant cette infrastructure, nous assurons une expérience de développement moderne et flexible tout en offrant une application performante et fiable pour les utilisateurs finaux.

## Gestion de projet

### Backlog Produit

https://github.com/enzofrnt/AUTO-QCM/labels/user%20story
- [Backlog Produit](https://github.com/enzofrnt/AUTO-QCM/labels/user%20story)

### Retours d’expérience de sprints

- [Sprint 1](https://github.com/enzofrnt/AUTO-QCM/wiki/Gestion-de-Projet#retour-dexp%C3%A9rience-du-sprint-1)
- [Sprint 2](https://github.com/enzofrnt/AUTO-QCM/wiki/Gestion-de-Projet#retour-dexp%C3%A9rience-du-sprint-2)

 [Retour fin de projet](https://github.com/enzofrnt/AUTO-QCM/wiki/Gestion-de-Projet#retour-dexp%C3%A9rience-du-projet)

### Backlogs de sprint

- [Sprint 1](https://github.com/users/enzofrnt/projects/4)
- [Sprint 2](https://github.com/users/enzofrnt/projects/6)
- [Sprint 3](https://github.com/users/enzofrnt/projects/7)

## Documentation

La documentation du projet se trouve dans l’onglet [Wiki](https://github.com/enzofrnt/AUTO-QCM/wiki) de GitHub !

- [Documentation Technique](https://github.com/enzofrnt/AUTO-QCM/wiki/Documentation-technique)
- [Documentation Utilisateur](https://github.com/enzofrnt/AUTO-QCM/wiki/Documentation-utilisateur)
- [Cahier de Test](https://github.com/enzofrnt/AUTO-QCM/wiki/Cahier-de-Test)
- [Gestion de Projet](https://github.com/enzofrnt/AUTO-QCM/wiki/Gestion-de-Projet)
- [Remerciement](https://github.com/enzofrnt/AUTO-QCM/wiki/Remerciement)
