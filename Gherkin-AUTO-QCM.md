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
* Accès à la page de création de QCM
* Accès à la page de création de question
* Accès aux pages sans authentification

[Lien vers le fichier de test.](https://github.com/enzofrnt/AUTO-QCM/blob/QualDev-Teillol-Fournet/auto_qcm/features/control_access.feature)

### Problème rencontré

Lors des premier tests sur le tableau de bors étudiant, nous nous sommes rendu compte que entant qu'enseignant, nous avons accès à la page étudiant. Ce qui ne devrait pas être on a donc réalisé un fix pour que les enseignant ne puisse pas accéder à la page étudiant en ajoutant un décorateur `student_required` sur la vue concernée.

Aussi lors des test de connexion sur le tableau de bord admin, nous nous sommes rendu compte qu'un utilisateur non administrateur était refirigé vers la page de connexion. Ce qui ne devrait pas être le cas. Nous avons donc réalisé un fix pour que les utilisateur non administrateur ne puisse pas accéder à la page de connexion en ajoutant un décorateur `admin_required` sur la vue concernée. Afin que l'erreur 403 soit renvoyée et que l'utilisateur soit redirigé vers la page de connexion.

### Intéret des tests

Ces tests permettent de vérifier que l'application est correctement sécurisée et que les utilisateurs ont bien uniquement accès aux pages qui les concernent et non à celles des autres utilisateurs. On constate d'ailleurs que l'implémentation a mis en évidence des soucis de cohérence.

## User Story #6

En tant qu'utilisateur, Je veux pouvoir saisir des questions

### Scénarios implémentés et résultats

Utilisateur :
    prof - rôle enseignant
    Lois - rôle étudiant
    admin - role admin

* Essayer de créer un question

[Lien vers le fichier de test.](https://github.com/enzofrnt/AUTO-QCM/blob/QualDev-Teillol-Fournet-US6/auto_qcm/features/test-US6.feature) #TODO: FIX

### Problème rencontré

### Intéret des tests

## User Story #11

En tant qu'enseignant, je souhaite agréger automatiquement des questions pour générer des QCM de contrôle afin de faciliter l'évaluation des étudiants.

### Scénarios implémentés et résultats

Nous avons mis en œuvre les tests suivants pour les différents utilisateurs :

- prof (rôle enseignant)
- Lois (rôle étudiant)
- admin (rôle administrateur)

Les scénarios testés sont :

* Création de QCM
* Modification de QCM
* Suppression de QCM
* Consultation de QCM

Pour chaque scénario, nous vérifions :

1. Les droits d'accès appropriés (403 pour les étudiants)
2. La persistance des données
3. La cohérence des informations affichées
4. La gestion des plages horaires
5. L'association des questions

[Lien vers le fichier de test](https://github.com/enzofrnt/AUTO-QCM/blob/QualDev-Teillol-Fournet/auto_qcm/features/crud_qcm.feature)

### Problèmes rencontrés

Aucun sur ces tests.

### Intérêt des tests

Ces tests BDD sont particulièrement importants car ils permettent de :

1. Vérifier que seuls les enseignants et administrateurs peuvent créer/modifier/supprimer des QCM
2. S'assurer que les étudiants peuvent uniquement consulter les QCM
3. Garantir l'intégrité des données lors des opérations CRUD
4. Valider la gestion des plages horaires et l'association des questions
5. Maintenir une cohérence dans l'interface utilisateur

Les tests ont également mis en évidence l'importance d'une bonne gestion des droits d'accès et de la validation des données pour garantir la fiabilité du système d'évaluation.
Ces tests permet de vérifier que les enseignants peuvent créer des questions.

##  User Story #14

En tant qu'enseignant, Je veux pouvoir générer des questions

### Scénarios implémentés et résultats

Utilisateur :
    prof - rôle enseignant
    Lois - rôle étudiant
    admin - role admin

* Essayer de générer des questions

[Lien vers le fichier de test.](https://github.com/enzofrnt/AUTO-QCM/blob/QualDev-Teillol-Fournet-US6/auto_qcm/features/test-US12.feature) #TODO: FIX

### Problème rencontré

La fonction POST de Django ne suit pas le même comportement par défaut que la bibliothèque de requêtes de Python, nous avons donc dû demander explicitement un format multipart et lire le flux d'octets à la fonction avant qu'elle ne fonctionne.
La fonction POST de génération de questions n'a pas été configurée pour exiger une authentification, ce qui a été corrigé avec un `@teacher_required` supplémentaire

### Intéret des tests

Ces tests permet de vérifier que les enseignants et seule les enseignants peuvent générer des questions à partir d'un pdf.
