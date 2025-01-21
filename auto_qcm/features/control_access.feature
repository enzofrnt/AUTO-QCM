Feature: Contrôle d'accès aux pages
  En tant qu'utilisateur
  Je veux accéder uniquement aux pages auxquelles j'ai le droit
  Afin de respecter la sécurité de l'application

  Background:
    Given la base de données est remplie avec des données de test

  Scenario Outline: Accès au tableau de bord enseignant
    Given je suis connecté en tant que "<user>"
    When je visite la page "tableau de bord enseignant"
    Then je devrais voir "<resultat>"
    Given je me deconnecte

    Examples:
      | user     | resultat                           |
      | prof     | le tableau de bord enseignant      |
      | Lois     | une erreur d'accès 403             |
      | admin    | le tableau de bord enseignant      |

  Scenario Outline: Accès au tableau de bord étudiant
    Given je suis connecté en tant que "<user>"
    When je visite la page "tableau de bord étudiant"
    Then je devrais voir "<resultat>"
    Given je me deconnecte

    Examples:
      | user     | resultat                          |
      | prof     | une erreur d'accès 403            |
      | Lois     | le tableau de bord étudiant       |
      | admin    |  une erreur d'accès 403           |


  Scenario Outline: Accès au tableau de bord admin
    Given je suis connecté en tant que "<user>"
    When je visite la page "tableau de bord admin"
    Then je devrais voir "<resultat>"
    Given je me deconnecte

    Examples:
      | user     | resultat                          |
      | prof     | une erreur d'accès 403            |
      | Lois     | une erreur d'accès 403            |
      | admin    | le tableau de bord admin          |

  Scenario Outline: Accès au formulaire de création de QCM
    Given je suis connecté en tant que "<user>"
    When je visite la page "création de QCM"
    Then je devrais voir "<resultat>"
    Given je me deconnecte

    Examples:
      | user     | resultat                          |
      | prof     | le formulaire de création de QCM  |
      | Lois     | une erreur d'accès 403            |
      | admin    | le formulaire de création de QCM  |

  Scenario Outline: Accès au formulaire de création de question
    Given je suis connecté en tant que "<user>"
    When je visite la page "création de question"
    Then je devrais voir "<resultat>"
    Given je me deconnecte

    Examples:
      | user     | resultat                              |
      | prof     | le formulaire de création de question |
      | Lois     | une erreur d'accès 403                |
      | admin    | le formulaire de création de question |

  Scenario Outline: Accès aux pages sans authentification
    Given je ne suis pas connecté
    When je visite la page "<page>"
    Then je devrais être redirigé vers la page de connexion

    Examples:
      | page                          |
      | tableau de bord enseignant    |
      | tableau de bord étudiant      |
      | liste des questions           |
      | création de QCM               |
      | création de question          |
      | tableau de bord admin         |
