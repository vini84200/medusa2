from django import forms
from django.forms import ModelForm

from escola.verificacao_forms import VerificarMinimo, VerificarPositivo, VerificarNomeUsuario, VerificarSenha, verificar
from .models import *

logger = logging.getLogger(__name__)


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
        return verificar(self.cleaned_data['senha'], [
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


class ConteudoForm(ModelForm):
    """Formulario para criação e atualização de Conteudos."""

    class Meta:
        model = Conteudo
        fields = ['nome', 'descricao', 'parent', ]
        widgets = {'parent': forms.HiddenInput(),
                   }
