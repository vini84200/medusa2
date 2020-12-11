# Medusa2
Medusa 2

**PROJETO ABANDONADO**
Ele não terá novas atualizações

[![Build Status](https://travis-ci.org/vini84200/medusa2.svg?branch=a)](https://travis-ci.org/vini84200/medusa2) 
[![Maintainability](https://api.codeclimate.com/v1/badges/03975d644adf743e4cf5/maintainability)](https://codeclimate.com/github/vini84200/medusa2/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/03975d644adf743e4cf5/test_coverage)](https://codeclimate.com/github/vini84200/medusa2/test_coverage)
[![DOI](https://zenodo.org/badge/152637885.svg)](https://zenodo.org/badge/latestdoi/152637885)

Este projeto tem como função a ajuda de alunos, e professores em suas vidas escolares.
O projeto foi escrito em Python com o auxilio do framework Django. O servidor de nossa utilização roda em https://medusa2.herokuapp.com
Para a instalação desse projeto, é necessario que as seguintes ENV vars sejam definidas:
```
SECRET_KEY: Uma cadeia de aproximadamente 50 caracteres aleatoria, deve ser mantida em segredo de produção.
ENV: Um nome para o ambiente que esta sendo rodado.
DJANGO_SETTINGS_MODULE: Endereço do modulo de configurações do django(Ex: "MedusaII/settings.py")
ENVIRONMENT: Um nome para o ambiente que esta sendo rodado.
DEFAULT_VERSION: Versão default, caso ele não consiga encontrar a versão.
```
Configurações obrigatorias para email
```
EMAIL_HOST
EMAIL_PORT
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD

EMAIL_FEEDACK_FROM: De qual email os feedbacks será enviado

```
Variaveis opcionais:
```
DSN_SENTRY: Coletor de erros, coloque o codigo do Sentry(Pode ser obrigatorio, não foi testado sem)
GA_TRACKING_ID: Id para coletar dados com o Google Analytics
EMAIL_BACKEND: (AVANÇADO) Alterar o metodo que usado para enviar os emails, usando como padrão as backends do Django. (https://docs.djangoproject.com/en/2.2/topics/email/#email-backends)
ADMINS_JSON: Formato JSON, uma lista de admins, eles receberão emails de feedbacks, nesse formato:
```
``` json
'[["Nome", "Email@exemple.com"], ["Nome", "Email@exemple.com"]]'
```
````
MAINTENANCE_MODE: Se mudado para 'True' impedo todos os usarios que não são superusers, ou staff de acessar o site.
```
