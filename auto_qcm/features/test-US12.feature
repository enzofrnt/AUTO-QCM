Feature: Generer les QCMs
  En tant qu'enseignant
  Je veux pouvoir générer des QCMs automatiquement

  Background:
    Given la base de données est remplie avec des données de test

  Scenario Outline: génération des QCMs
    Given je suis connecté en tant que "<user>"
    When J'envoie un pdf
    Then Les questions "<existe>"
    Given je me deconnecte

    Examples:
      | user  | existe         |
      | prof  | existent       |
      | Lois  | n'existent pas |
      | admin | existent       |