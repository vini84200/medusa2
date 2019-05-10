Feature: Aviso de email
  Quando um usuario não possuir um email registrado

  @django_db
  Scenario: Usuario vê aviso
    Given a user is logged in
    And he doesn't have a email
    When he is in the homepage
    Then he sees a warning about his email
    And a link in the warning, to change his email

  @django_db
  Scenario: Usuario tem formulario
    Given a user is logged in
    When Enters the page 'escola:self-email-change'
    Then a form should load

  @django_db
  Scenario: Usuario preenche email
    Given a user is logged in
    And enters the page 'escola:email-change'
    When fill the field 'email' with 'teste@ok.com'
    And submit the form
    Then he is redirected to a page with confirmation message
