from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm
from django.forms import ModelForm
from django.utils.safestring import mark_safe

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

    def __init__(self, *args, **kwargs):
        super(AlunoCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Enviar'))


class AlunoCreateFormOutLabel(forms.Form):
    num_chamada = forms.IntegerField(label='', widget=forms.NumberInput(attrs={
        'placeholder': 'N. Chamada, ex.: 24'
    }))
    nome = forms.CharField(label='', widget=forms.TextInput(attrs={
        'placeholder': 'Nome Ex.: Oliver Wood'
    }))
    username = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Username( deixe em branco para geração automatica )'
    }))
    senha = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Senha'
    }))
    turma = forms.IntegerField(label='', widget=forms.NumberInput(attrs={
        'placeholder': 'Turma ex.: 204'
    }))

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

    def __init__(self, *args, **kwargs):
        super(AlunoCreateFormOutLabel, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_class = 'form-row'
        self.helper.form_method = 'post'
        # self.helper.template = 'bootstrap/table_inline_formset.html'
        # self.helper.formset_tag = False

        # self.helper.add_input(Submit('submit', 'Enviar'))


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
        exclude = ('turma', 'manager_seguidor')

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


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'oliver.ow'}),
                               label=mark_safe('Nome de Usuario'), label_suffix='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'ex.: *********'}),
                               label='Senha', label_suffix=''
                               )


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="", max_length=254, label_suffix='',
                             widget=forms.TextInput(
                                 attrs={
                                     'class': 'form-control',
                                     'placeholder': 'ex.: hermione@spew.org.uk'
                                 }))


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Senha atual",
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True, 'class': 'form-control', }),
    )
    new_password1 = forms.CharField(
        label="Nova senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control has-popover',
                                          'data-content': password_validation.password_validators_help_text_html(),
                                          'data-placement': 'right', 'data-container': 'body'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="Confirmação da nova senha",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
