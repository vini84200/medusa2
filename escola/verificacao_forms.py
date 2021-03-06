"""
Verificações dos Campos dos Forms.
"""
#  Developed by Vinicius José Fritzen
#  Last Modified 12/04/19 13:19.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import datetime
from typing import Callable, Any

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

import logging
from escola.utils import username_present
logger = logging.getLogger(__name__)


class Verificacao:
    """
    Objeto de verificação base, possui uma funçao que retorna True se o campo for valido e raise Validation error
    se não for
    """

    def verificar(self, date):
        """Verifica se os dados estão OK"""
        return date


class VerificarLambda(Verificacao):
    """Uma verificação que usa uma Lambda para verificar"""
    lamb: Callable[[Any], bool] = lambda date: True
    msg = "Esse campo não foi preenchido corretamente."

    def __init__(self, veri, msg="Esse campo não foi preenchido corretamente."):
        self.lamb = veri
        self.msg = _(msg)

    def verificar(self, data):
        """Verifica se a Lambda retorna True"""
        if self.lamb(data):
            return data
        else:
            raise ValidationError(self.msg)


class VerificarMinimo(VerificarLambda):
    """Verifica se o campo numerico for no minimo um certo valor"""
    valor_min = 0
    msg = "Por favor, digite um numero maior, ou igual a {}"

    def __init__(self, valor_min=0, msg="Por favor, digite um numero maior, ou igual a {}"):
        super().__init__(lambda data: data >= valor_min, msg.format(valor_min))


class VerificarMaximo(VerificarLambda):
    """Verifica se o campo numerico for no minimo um certo valor"""
    valor_max = 0
    msg = "Por favor, digite um numero menor, ou igual a {}"

    def __init__(self, valor_max=0, msg="Por favor, digite um numero maior que {}"):
        super().__init__(lambda data: data <= valor_max, msg.format(valor_max))


class VerificarPositivo(VerificarMinimo):
    """Verifica se o campo é um valor positivo, isto é maior ou igual a zero."""

    def __init__(self, msg="Por favor, digite um valor positivo"):
        super().__init__(0, msg)


class VerificarNomeUsuario(Verificacao):
    """ Faz uma verificação do nome de usuario"""
    blank = False
    msg_blank = _("O nome de usuario não pode estar em branco.")
    msg_ja_usado = _("Este nome de usuario já existe, use outro.")

    def __init__(self, blank=False,
                 msg_ja_usado="Este nome de usuario já existe, use outro.",
                 msg_blank="O nome de usuario não pode estar em branco."):
        self.blank = blank
        self.msg_blank = _(msg_blank)
        self.msg_ja_usado = _(msg_ja_usado)

    def verificar(self, data):
        """Verifica que o nome de usuario é valido."""
        if data == '':
            if self.blank:
                return data
            else:
                raise ValidationError(self.msg_blank)

        if username_present(data):
            raise ValidationError(self.msg_ja_usado)

        return data


class VerificarSenha(Verificacao):
    """ Faz uma verificação da senha, retorna date, ou cria um ValidationExeption"""
    blank = False
    msg_blank = _("A senha não pode estar em branco.")

    def __init__(self, blank=False,
                 msg_blank="A senha não pode estar em branco."):
        self.blank = blank
        self.msg_blank = _(msg_blank)

    def verificar(self, data):
        """Verifica se a senha é valida."""
        if data == '':
            if self.blank:
                return data
            else:
                raise ValidationError(self.msg_blank)
        # Segundo a documentação validate_password retorna None se as validações passarem;
        if validate_password(data) is None:
            return data
        logger.error("Por algum motivo o validate_password()[forms.py:AlunoCreateForm:clean_senha()] não retornou "
                       "None, nem deu Raise num ValidateError.")
        raise ValidationError(_('Algo de errado aconteceu, por favor tente novamente mais tarde.'))


class VerificarDataFutura(VerificarLambda):
    """Verifica se uma data é futura, retorna erro se não"""

    msg = "A data preenchida não esta no futuro"

    def __init__(self, msg=msg):
        super().__init__(lambda data: data >= timezone.now(), msg)


def verificar(date, verificacoes):
    """Verifica um campo quando recebe uma lista de verificacoes"""
    for veri in verificacoes:
        date = veri.verificar(date)
    return date
