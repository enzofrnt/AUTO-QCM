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

## User Story #65

**En tant qu'**étudiant
**Je veux** avoir accès à toutes les pages qui me sont destinées
**Afin de** pouvoir utiliser efficacement l'application

### Critères d'acceptation

- Interface claire
- Accès restreint en fonction du rôle
- Données précises en temps réel

## Tests BDD Implémentés

#### Scénarios implémentés et résultats
