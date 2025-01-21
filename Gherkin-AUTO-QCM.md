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

* **#65**

En tant qu'étudiant je veux avoir accès à toutes les pages qui me sont destinées
afin de pouvoir utiliser efficacement l'application.

* **#63**

En tant qu'enseignant je veux avoir accès à toutes les pages qui me sont destinée

---

Ces deux user stories sont regrouper dans le même scénario car il sagit de vérifier que des utilisateur spécifque on correctemnt accées à l'applications donc plus globalement de vérifier que les droit d'accès sont correctement implémenté.

### Scénarios implémentés et résultats

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

### Problème rencontré

Lors des premier tests sur le tableau de bors étudiant, nous nous sommes rendu compte que entant qu'enseignant, nous avons accès à la page étudiant. Ce qui ne devrait pas être on a donc réalisé un fix pour que les enseignant ne puisse pas accéder à la page étudiant en ajoutant un décorateur `student_required` sur la vue concernée.

Aussi lors des test de connexion sur le tableau de bord admin, nous nous sommes rendu compte qu'un utilisateur non administrateur était refirigé vers la page de connexion. Ce qui ne devrait pas être le cas. Nous avons donc réalisé un fix pour que les utilisateur non administrateur ne puisse pas accéder à la page de connexion en ajoutant un décorateur `admin_required` sur la vue concernée. Afin que l'erreur 403 soit renvoyée et que l'utilisateur soit redirigé vers la page de connexion.

### Intéret des tests

Ces tests permettent de vérifier que l’application est correctement sécurisée et que les utilisateurs ont bien uniquement accès aux pages qui les concernent et non à celles des autres utilisateurs. On constate d’ailleurs que l’implémentation a mis en évidence des soucis de cohérence.

## User story #6

### Scénarios implémentés et résultats

### Problème rencontré

### Intéret des tests
