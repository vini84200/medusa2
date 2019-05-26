import datetime

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from escola.verificacao_forms import Verificacao, VerificarLambda, VerificarMinimo, VerificarMaximo, VerificarPositivo, \
    verificar, VerificarDataFutura


def test_verificacao_lambda_raise():
    veri = VerificarLambda(lambda date: date == "Okay")
    with pytest.raises(ValidationError):
        veri.verificar("NO")


def test_validation_lambda_true():
    veri = VerificarLambda(lambda date: date == "Okay")
    assert veri.verificar("Okay") == "Okay"


def test_validation_base_return_true():
    assert Verificacao().verificar('asaf') == 'asaf'


def test_verificar_minimo_valor_menor_raise():
    with pytest.raises(ValidationError):
        VerificarMinimo(4).verificar(2)


def test_verificar_minimo_valor_igual_okay():
    assert VerificarMinimo(5).verificar(5) == 5


def test_verificar_minimo_valor_acima_okay():
    assert VerificarMinimo(7).verificar(23) == 23


def test_verificar_minimo_nao_numero_raise():
    with pytest.raises(TypeError):
        VerificarMinimo(1).verificar("Não Numero")


def test_verificar_maximo_valor_menor_okay():
    assert VerificarMaximo(4).verificar(2) == 2


def test_verificar_maximo_valor_igual_okay():
    assert VerificarMaximo(5).verificar(5) == 5


def test_verificar_maximo_valor_acima_raise():
    with pytest.raises(ValidationError):
        VerificarMaximo(7).verificar(23)


def test_verificar_maximo_nao_numero_raise():
    with pytest.raises(TypeError):
        VerificarMaximo(1).verificar("Não Numero")


def test_verificar_raise():
    with pytest.raises(ValidationError):
        verificar(12, [VerificarMaximo(10)])

    with pytest.raises(ValidationError):
        verificar(5, [VerificarMaximo(10), VerificarMinimo(8)])


def test_verificar_okay():
    assert verificar(6, [VerificarMinimo(4), VerificarMaximo(14)]) == 6
    assert verificar(7, [VerificarMaximo(7)]) == 7


def test_verificar_positivo_raise():
    with pytest.raises(ValidationError):
        VerificarPositivo().verificar(-23)

def test_verificar_positivo_okay():
    assert VerificarPositivo().verificar(34) == 34

# Verificar data futura

def test_verificar_data_passada():
    future = timezone.now() + datetime.timedelta(minutes=10)
    past = timezone.now() - datetime.timedelta(minutes=10)
    assert VerificarDataFutura().verificar(future) == future
    with pytest.raises(ValidationError):
        VerificarDataFutura().verificar(past)
