Feature: Saisir ou envoyer mes questions
  En tant qu'utilisateur
  Je veux pouvoir saisir des questions

  Background:
    Given la base de données est remplie avec des données de test

  Scenario Outline: création des questions
    Given je suis connecté en tant que "<user>"
    When je crée un nouveau question
    Then le question "<existe>"
    Given je me deconnecte

    Examples:
      | user  | existe       |
      | prof  | existe       |
      | Lois  | n'existe pas |
      | admin | existe       |