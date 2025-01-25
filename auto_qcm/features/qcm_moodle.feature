Feature: QCM and Moodle/AMC integration

  Rule: QCM exports must support multiple formats
    Scenario Outline: Teacher exports QCM in different formats
      Given I am logged in as a teacher
      And I have created a QCM with ID "<qcm_id>"
      When I request to export the QCM in <format> format
      Then I should receive a file named "qcm_<qcm_id>.<extension>"
      And the file should have the correct content type "<content_type>"

      Examples:
        | qcm_id | format | extension | content_type        |
        | 123    | XML    | xml      | application/xml     |
        | 123    | LaTeX  | tex      | application/x-latex |
        | 123    | AMC    | txt      | application/x-amc   |
