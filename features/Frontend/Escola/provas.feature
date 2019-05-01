Feature: Provas

  @live_server_no_flush
  Scenario: Aluno wants to see his Provas
    Given a Aluno is logged in
    And a Professor created a Prova
    When he is in the homepage
    Then the Aluno should see the Prova in the list

  @live_server_no_flush
  Scenario: When Professor wants to create a Prova show Form
    Given a Professor is logged in
    And he is in the homepage
    And he has a Materia for him
    And he clicks the Area do Professor dropdown
    And then clicks in the Minhas Materias option in the dropdown
    And he clicks on the materia of the list
    And he clicks the link 'Adicionar Prova'
    Then the form of Adicionar Prova shows
