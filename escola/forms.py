import logging
from typing import Any, Callable

from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from .models import *

logger = logging.getLogger(__name__)


def username_present(username):
    if User.objects.filter(username=username).exists():
        return True

    return False


class Verificacao:
    """Objeto de verificação base, possui uma funçao que retorna True se o campo for valido e raise Validation error
    se não for """

    def verificar(self, date):
        return date


class VerificarLambda(Verificacao):
    """Uma verificação que usa uma Lambda para verificar"""
    lamb: Callable[[Any], bool] = lambda date: True
    msg = "Esse campo não foi preenchido corretamente."

    def __init__(self, veri, msg="Esse campo não foi preenchido corretamente."):
        self.lamb = veri
        self.msg = msg

    def verificar(self, data):
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


def verificar(date, verificacoes):
    """Verifica um campo quando recebe uma lista de verificacoes"""
    for veri in verificacoes:
        date = veri.verificar(date)
    return date


class CriarTurmaForm(forms.Form):
    numero = forms.IntegerField(label="Numero da Turma:",
                                help_text="Coloque o numero da turma. Exs. 101, 303, 203, 204")
    ano = forms.IntegerField(label="Ano:", help_text="Ano de atividade dessa turma. Exs. 2018, 2019")

    def clean_numero(self):
        return verificar(self.cleaned_data['numero'], [
            VerificarPositivo()
        ])

    def clean_ano(self):
        return verificar(self.cleaned_data['ano'], [
            VerificarMinimo(1940, msg='Ano invalido, por favor informe um ano posterior a {}.')
        ])


class CargoForm(ModelForm):
    class Meta:
        model = CargoTurma
        fields = ['nome', 'ocupante', 'cod_especial', 'ativo', ]

    def __init__(self, turma, *args, **kwargs):
        super(CargoForm, self).__init__(*args, **kwargs)
        self.fields['ocupante'].queryset = User.objects.filter(aluno__turma=turma) | \
                                           User.objects.filter(profile_escola__is_professor=True)


class AlunoCreateForm(forms.Form):
    num_chamada = forms.IntegerField()
    nome = forms.CharField()
    username = forms.CharField(help_text="Deixe em branco para geração automatica.", required=False)
    senha = forms.CharField(help_text="Deixe em branco para aleatorio.", required=False)
    turma = forms.IntegerField()

    def clean_num_chamada(self):
        return verificar(self.cleaned_data['num_chamada'], [
            VerificarPositivo()
        ])

    def clean_senha(self):
        return verificar(self.cleaned_data['senha'],[
            VerificarSenha(blank=True)
        ])

    def clean_username(self):
        return verificar(self.cleaned_data['username'], [
            VerificarNomeUsuario(blank=True)
        ])


class AlunoCreateFormOutLabel(forms.Form):
    num_chamada = forms.IntegerField(label='')
    nome = forms.CharField(label='')
    username = forms.CharField(label='', required=False)
    senha = forms.CharField(label='', required=False)
    turma = forms.IntegerField(label='')

    def clean_num_chamada(self):
        return verificar(self.cleaned_data['num_chamada'], [
            VerificarPositivo()
        ])

    def clean_username(self):
        return verificar(self.cleaned_data['username'], [
            VerificarNomeUsuario(blank=True),
        ])

    def clean_senha(self):
        return verificar(self.cleaned_data['senha'], [
            VerificarSenha(blank=True)
        ])


class PeriodoForm(ModelForm):
    class Meta:
        model = Periodo
        fields = ['materia']


class ProfessorCreateForm(forms.Form):
    nome = forms.CharField()
    username = forms.CharField(help_text="Deixe em branco para geração automatica.", required=False)
    senha = forms.CharField(help_text="Deixe em branco para aleatorio.", required=False)

    def clean_senha(self):
        return verificar(self.cleaned_data['senha'], [
            VerificarSenha(blank=True)
        ])

    def clean_username(self):
        return verificar(self.cleaned_data['username'], [
            VerificarNomeUsuario(blank=True),
        ])


class MateriaForm(ModelForm):
    class Meta:
        model = MateriaDaTurma
        fields = ['nome', 'professor', 'abreviacao']


class TarefaForm(ModelForm):
    class Meta:
        model = Tarefa
        exclude = ('turma',)

    def __init__(self, turma, *args, **kwargs):
        super(TarefaForm, self).__init__(*args, **kwargs)
        self.fields['materia'].queryset = MateriaDaTurma.objects.filter(turma=turma)


class ComentarioTarefaForm(ModelForm):
    class Meta:
        model = TarefaComentario
        fields = ['texto', ]
