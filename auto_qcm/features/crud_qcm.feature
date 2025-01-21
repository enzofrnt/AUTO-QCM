Feature: Gestion des QCM
  En tant qu'enseignant
  Je veux créer, modifier, supprimer et consulter des QCM
  Afin de gérer les évaluations de mes étudiants

  Background:
    Given la base de données est remplie avec des données de test

  Scenario Outline: Création de QCM
    Given je suis connecté en tant que "<user>"
    When je crée un nouveau QCM
    Then je devrais voir "<resultat>"
    Given je me deconnecte

    Examples:
      | user     | resultat                      |
      | prof     | le formulaire de création de QCM |
      | Lois     | une erreur d'accès 403        |
      | admin    | le formulaire de création de QCM |

  Scenario Outline: Modification de QCM
    Given je suis connecté en tant que "<user>"
    And QCM créé
    When je modifie un QCM
    Then je devrais voir "<resultat>"
    Given je me deconnecte

    Examples:
      | user     | resultat                      |
      | prof     | le QCM est mis à jour        |
      | Lois     | une erreur d'accès 403       |
      | admin    | le QCM est mis à jour        |

  Scenario Outline: Suppression de QCM
    Given je suis connecté en tant que "<user>"
    And QCM créé
    When je supprime un QCM
    Then je devrais voir "<resultat>"
    Given je me deconnecte

    Examples:
      | user     | resultat                      |
      | prof     | le QCM est supprimé          |
      | Lois     | une erreur d'accès 403       |
      | admin    | le QCM est supprimé          |

  Scenario Outline: Consultation de QCM
    Given je suis connecté en tant que "<user>"
    And QCM créé
    When je consulte un QCM
    Then je devrais voir "<resultat>"
    Given je me deconnecte

    Examples:
      | user     | resultat                      |
      | prof     | le QCM est affiché           |
      | Lois     | le QCM est affiché           |
      | admin    | le QCM est affiché           |
