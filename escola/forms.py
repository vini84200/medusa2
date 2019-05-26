#  Developed by Vinicius José Fritzen
#  Last Modified 12/04/19 13:19.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from mptt.forms import TreeNodeChoiceField, TreeNodeMultipleChoiceField
from rolepermissions.checkers import has_role, has_permission

from escola.verificacao_forms import VerificarMinimo, VerificarPositivo, VerificarNomeUsuario, VerificarSenha, \
    verificar, VerificarDataFutura
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

    def __init__(self, *args, **kwargs):
        super(CriarTurmaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', "Criar"))


class CargoForm(ModelForm):
    class Meta:
        model = CargoTurma
        fields = ['nome', 'ocupante', 'cod_especial', 'ativo', ]

    def __init__(self, turma, *args, **kwargs):
        super(CargoForm, self).__init__(*args, **kwargs)
        self.fields['ocupante'].queryset = User.objects.filter(aluno__turma=turma) | \
                                           User.objects.filter(profile_escola__is_professor=True)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', "Adicionar"))


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

    def __init__(self, *args, **kwargs):
        super(PeriodoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


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

    def __init__(self, *args, **kwargs):
        super(ProfessorCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', "Adicionar"))


class MateriaForm(ModelForm):
    class Meta:
        model = MateriaDaTurma
        fields = ['nome', 'professor', 'abreviacao']

    def __init__(self, *args, **kwargs):
        super(MateriaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', "Adicionar"))


class TarefaForm(ModelForm):
    class Meta:
        model = Tarefa
        exclude = ('turma', 'manager_seguidor')

    def __init__(self, turma, *args, **kwargs):
        super(TarefaForm, self).__init__(*args, **kwargs)
        self.fields['materia'].queryset = MateriaDaTurma.objects.filter(turma=turma)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', "Adicionar"))



class ComentarioTarefaForm(ModelForm):
    class Meta:
        model = TarefaComentario
        fields = ['texto', ]
        widgets = {'texto': forms.Textarea(attrs={'placeholder': 'Escreva aqui um comentario...',
                                                  'rows': 3})}

    def __init__(self, *args, **kwargs):
        super(ComentarioTarefaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', "Comentar"))
        self.helper.form_show_labels = False
        self.helper.html5_required =True


class ConteudoForm(ModelForm):
    """Formulario para criação e atualização de Conteudos."""

    class Meta:
        model = Conteudo
        fields = ['nome', 'descricao', 'parent', ]
        widgets = {'parent': forms.HiddenInput(),
                   }

    def __init__(self, *args, **kwargs):
        super(ConteudoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', "Adicionar"))


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


class SelectConteudosForm(forms.Form):
    conteudos = TreeNodeMultipleChoiceField(queryset=Conteudo.objects.all())

    def __init__(self, professor, materia, *args, **kwargs):
        super(SelectConteudosForm, self).__init__(*args, **kwargs)
        self.fields['conteudos'].queryset = Conteudo.objects.filter(professor=professor)
        self.materia = materia
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', "Adicionar"))

    def add_materia(self):
        conteudos = self.cleaned_data['conteudos']
        for conteudo in conteudos:
            # TODO: 06/04/2019 por wwwvi: Adicionar forma de retirar conteudos
            self.add_conteudo_na_materia(conteudo)

    def add_conteudo_na_materia(self, conteudo):

        if conteudo not in self.materia.conteudos.all():
            if conteudo.parent:
                if conteudo.parent not in self.materia.conteudos.all():
                    self.add_conteudo_na_materia(conteudo.parent)
            self.materia.conteudos.add(conteudo)

class EmailChangeForm(forms.Form):
    """
    A form that lets a user change set their email while checking for a change in the
    e-mail.
    """
    error_messages = {
        'email_mismatch': "Os dois emails não são iguais",
        'not_changed': "O email continua o mesmo",
    }

    new_email1 = forms.EmailField(
        label="Novo email",
        widget=forms.EmailInput,
    )

    new_email2 = forms.EmailField(
        label="Confirmar novo email",
        widget=forms.EmailInput,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EmailChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Alterar'))

    def clean_new_email1(self):
        old_email = self.user.email
        new_email1 = self.cleaned_data.get('new_email1')
        if new_email1 and old_email:
            if new_email1 == old_email:
                raise forms.ValidationError(
                    self.error_messages['not_changed'],
                    code='not_changed',
                )
        return new_email1

    def clean_new_email2(self):
        new_email1 = self.cleaned_data.get('new_email1')
        new_email2 = self.cleaned_data.get('new_email2')
        if new_email1 and new_email2:
            if new_email1 != new_email2:
                raise forms.ValidationError(
                    self.error_messages['email_mismatch'],
                    code='email_mismatch',
                )
        return new_email2

    def save(self, commit=True):
        email = self.cleaned_data["new_email1"]
        self.user.email = email
        if commit:
            self.user.save()
        return self.user


class MarcarProvaMateriaProfessorForm(forms.Form):
    """
        Formumulario para marcar uma prova de materia.
    """
    error_messages = {

    }
    
    titulo = forms.CharField(max_length=70)
    data = forms.DateTimeField(widget=AdminDateWidget)
    descricao = forms.CharField(widget=forms.Textarea())
    materia = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, instance, professor, **kwargs):
        super().__init__(*args, **kwargs)
        # professor = kwargs.get('professor')
        self.fields['materia'].queryset = professor.professor.materias
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', "Adicionar"))
        self.user = professor

    def clean_data(self):
        return verificar(self.cleaned_data['data'],
                         [VerificarDataFutura('A data da prova deve estar no futuro.')])

    def save(self):
        ProvaMateriaMarcada.create(self.cleaned_data['materia'],
                                   self.cleaned_data['titulo'],
                                   self.cleaned_data['data'],
                                   self.cleaned_data['descricao'],
                                   self.user)


class MarcarProvaAreaProfessorForm(forms.Form):
    """
        Formumulario para marcar uma prova de materia.
    """
    error_messages = {

    }

    titulo = forms.CharField(max_length=70)
    data = forms.DateTimeField()
    descricao = forms.CharField(widget=forms.Textarea())
    area = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, instance, professor, **kwargs):
        super().__init__(*args, **kwargs)
        # professor = kwargs.get('professor')
        # Define as opções que aparecem na lista
        if has_permission(professor, 'add_prova_area_geral'):
            self.fields['area'].queryset = AreaConhecimento.objects.all()
        else:
            self.fields['area'].queryset = Turma.objects.filter(regente=professor).area.all()

        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', "Adicionar"))
        self.user = professor

    def clean_data(self):
        return verificar(self.cleaned_data['data'],
                         [VerificarDataFutura('A data da prova deve estar no futuro.')])

    def save(self):
        ProvaAreaMarcada.create(self.cleaned_data['area'],
                                   self.cleaned_data['titulo'],
                                   self.cleaned_data['data'],
                                   self.cleaned_data['descricao'],
                                   self.user)
