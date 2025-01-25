Feature: Admin access to pages

Scenario: Admin accesses all pages intended for them
  Given I am a Admin
  When I log in as admin
  Then I should have access to admin urls:
    | /question/list/           |
    | /qcm/create/              |
    | /enseignant-dashboard/    |
    | /support-doc/             |
    | / |