# Documentation des Tests BDD - AUTO-QCM

## Execution des tests

### Prérequis

Application exécutée en développement

```bash
cd deploiement-dev
docker compose up -d --build
```

## Execution des tests

```bash
docker compose exec -it auto_qcm_python python manage.py behave --noinput
```

## Execution des test et génération du rapport

```bash
docker compose exec -it auto_qcm_python python manage.py behave --noinput -f behave_html_formatter:HTMLFormatter -o rapport_tests.html
```

## CI

Une CI gihtub a été mise en oeuve pour lancer les tests à chaque push. Elle permet un suivis sur l'évolution de nos tets et donc la qualité du code et de notre application.

Le rapport générer par la CI est donc rendu disponible dans les artefacts de la CI sur github.

Exemple : [CI]() #TODO

## User Story #65 et #63

### #65

En tant qu'étudiant je veux avoir accès à toutes les pages qui me sont destinées
afin de pouvoir utiliser efficacement l'application.

### #63

En tant qu'enseignant je veux avoir accès à toutes les pages qui me sont destinée

---

Ces deux user stories sont regrouper dans le même scénario car il sagit de vérifier que des utilisateur spécifque on correctemnt accées à l'applications donc plus globalement de vérifier que les droit d'accès sont correctement implémenté.

#### Scénarios implémentés et résultats

Nous avons donc mis en oeuvre les test suivant sur les utilisater suivant:

Utilisateur :
    prof - rôle enseignant
    Lois - rôle étudiant
    admin - role admin


* Accès au tableau de bord enseignant
* Accès au tableau de bord étudiant

* Accès à la page de création de QCM #TODO
* Accès à la page de création de question #TODO

* Accès aux pages sans authentification

##### Problème rencontré

Lors des premier tests
