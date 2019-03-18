from django import forms
from django.contrib.auth.password_validation import validate_password

from .models import *
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def username_present(username):
    if User.objects.filter(username=username).exists():
        return True

    return False

class CriarTurmaForm(forms.Form):
    numero = forms.IntegerField(label="Numero da Turma:",
                                help_text="Coloque o numero da turma. Exs. 101, 303, 203, 204")
    ano = forms.IntegerField(label="Ano:", help_text="Ano de atividade dessa turma. Exs. 2018, 2019")

    def clean_numero(self):
        data = self.cleaned_data['numero']
        # Checks if it is zero or negative.
        if data <= 0:
            raise ValidationError(_('Número invalido, por favor informe um número positivo.'))

        return data

    def clean_ano(self):
        data = self.cleaned_data['ano']
        # Checks if it is zero or negative.
        if data <= 1940:
            raise ValidationError(_('Ano invalido, por favor informe um ano posterior a 1940.'))

        return data


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
        data = self.cleaned_data['num_chamada']
        if data <= 0:
            raise ValidationError(_("Por favor, salve a chamada com um numero positivo."))

        return data

    def clean_senha(self):
        data = self.cleaned_data['senha']
        if data == '':
            return data
        # Segundo a documentação validate_password retorna None se passar;
        if validate_password(data) is None:
            return data
        print("Por algum motivo o validate_password()[forms.py:AlunoCreateForm:clean_senha()] não retornou None, "
              "nem deu Raise num ValidateError.")
        raise ValidationError(_('Por algum motivo o validate_password()[forms.py:AlunoCreateForm:clean_senha()] não '
                                'retornou None, nem deu Raise num ValidateError, entre em contato porfavor.'))

    def clean_username(self):
        data = self.cleaned_data['username']
        if data == '':
            return data

        if username_present(data):
            raise ValidationError(_('Nome de usuario já tomado, por favor escolha outro.'))

        return data


class AlunoCreateFormOutLabel(forms.Form):
    num_chamada = forms.IntegerField(label='')
    nome = forms.CharField(label='')
    username = forms.CharField(label='', required=False)
    senha = forms.CharField(label='', required=False)
    turma = forms.IntegerField(label='')

    def clean_num_chamada(self):
        data = self.cleaned_data['num_chamada']
        if data <= 0:
            raise ValidationError(_("Por favor, salve a chamada com um numero positivo."))

        return data


class PeriodoForm(ModelForm):
    class Meta:
        model = Periodo
        fields = ['materia']


class ProfessorCreateForm(forms.Form):
    nome = forms.CharField()
    username = forms.CharField(help_text="Deixe em branco para geração automatica.", required=False)
    senha = forms.CharField(help_text="Deixe em branco para aleatorio.", required=False)


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
