#  Developed by Vinicius José Fritzen
#  Last Modified 12/04/19 13:19.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import logging
import re

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       PasswordResetForm)
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.forms import ModelForm
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from markdownx.fields import MarkdownxFormField
from mptt.forms import TreeNodeMultipleChoiceField
from rolepermissions.checkers import has_permission
from django_select2.forms import Select2MultipleWidget

from escola.models import (AreaConhecimento, AvisoGeral, CargoTurma, Conteudo,
                           MateriaDaTurma, Periodo, ProvaAreaMarcada,
                           ProvaMateriaMarcada, Tarefa, TarefaComentario,
                           Turma, Aluno)
from escola.verificacao_forms import (VerificarDataFutura, VerificarMinimo,
                                      VerificarNomeUsuario, VerificarPositivo,
                                      VerificarSenha, verificar)

logger = logging.getLogger(__name__)


class CriarTurmaForm(forms.Form):
    numero = forms.IntegerField(label="Numero da Turma:",
                                help_text="Coloque o numero da turma."
                                          "Exs. 101, 303, 203, 204")
    ano = forms.IntegerField(label="Ano:", help_text="Ano de atividade dessa"
                                                     " turma. Exs. 2018, 2019")

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
        exclude = ('turma', 'noti_comentario', 'notificado')

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
        self.helper.html5_required = True


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

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', "Logar"))


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
        self.fields['conteudos'].queryset = Conteudo.objects.filter(
            professor=professor)
        self.materia = materia
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', "Adicionar"))

    def add_materia(self):
        conteudos = self.cleaned_data['conteudos']
        for conteudo in conteudos:
            # TODO: 06/04/2019 por wwwvi: Adicionar forma de retirar conteudos
            self.add_conteudo_na_materia(conteudo)

    def add_conteudo_na_materia(self, conteudo: Conteudo):

        if conteudo not in self.materia.conteudos.all():
            if conteudo.parent:
                if conteudo.parent not in self.materia.conteudos.all():
                    self.add_conteudo_na_materia(conteudo.parent)
            self.materia.conteudos.add(conteudo)
            self.materia.turma.comunicar_noti('novo_conteudo', f"Um novo conteudo foi postado na materia {self.materia}", f"A materia {self.materia} recebeu um novo conteudo, "
                                                               f"ele se chama {conteudo.nome}, para ver mais detalhes acesse o conteudo.", conteudo.get_absolute_url())


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
    descricao = MarkdownxFormField(widget=forms.Textarea())
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
    descricao = MarkdownxFormField(widget=forms.Textarea())
    area = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, instance, professor, **kwargs):
        super().__init__(*args, **kwargs)
        # professor = kwargs.get('professor')
        # Define as opções que aparecem na lista
        if has_permission(professor, 'add_prova_area_geral'):
            self.fields['area'].queryset = AreaConhecimento.objects.all()
        else:
            # self.fields['area'].queryset = Turma.objects.filter(regente=professor).area.all()
            self.fields['area'].queryset = AreaConhecimento.objects.filter(turma__regente=professor)

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


# Feedback
class FeedbackForm(forms.Form):
    """Formulario que permite que um usuario envie seu feedback, deve enviar email."""

    error_messages = {

    }

    nome = forms.CharField(max_length=100, required=False, label="Nome(Opicional)")
    email = forms.EmailField(required=False, label="Email(Opicional)")
    assunto = forms.CharField(required=False, label="Assunto(Opcional)")
    mensagem = forms.CharField(max_length=3000, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "send-feedback-form"
        self.helper.form_action = ""

    def save(self):
        logger.info("Preparando para enviar email de feedback")
        nome = self.cleaned_data['nome'] or "[ANONIMO]"
        email = self.cleaned_data['email'] or "[ANONIMO]"
        assunto = self.cleaned_data['assunto'] or "[SEM ASSUNTO]"
        mensagem = self.cleaned_data['mensagem']

        plaintext = get_template('escola/feedback/email_feedback.txt')
        htmly = get_template('escola/feedback/email_feedback.html')

        c = {'nome': nome, 'email': email, 'assunto': assunto, 'mensagem': mensagem}

        subject, from_email, to = f'Novo feedback: {assunto}', settings.FEEDBACK_FROM_EMAIL, [b for a, b in settings.ADMINS]

        text_content = plaintext.render(c)
        html_content = htmly.render(c)

        logger.info("Ultimas preparações para enviar o email de feedback!")
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        logger.info("Enviando o email de feedback...")
        msg.send()
        logger.info("Enviado o email de feedback!!")


class AvisoTurmaForm(forms.Form):
    titulo = forms.CharField(max_length=170)
    msg = MarkdownxFormField(max_length=5000)
    turma = forms.ModelChoiceField(queryset=None)

    def __init__(self, owner, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['turma'].queryset = Turma.objects.all()
        self.owner = owner
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', "Adicionar"))

    def save(self):
        AvisoGeral.create(
            self.cleaned_data['titulo'],
            self.cleaned_data['msg'],
            self.owner,
            self.cleaned_data['turma'])


class AvisoMixedGeneratorBase:
    """Gerador base usado nos Avisos Mixed, tem como objetivo gerar opções"""
    def generate_list(self, gen_code):
        """
        Gera opções, todos suas opções devem estar identificadas com o
        gen_code
        """
        pass

    def get_own(self, gen_code, selected):
        """Verifica quais itens são proprios deste"""
        r = re.compile(r'{0}_\w+'.format(gen_code))
        return [x for x in selected if r.match(x)]

    def parse_item(self, item):
        raise NotImplementedError("Usando a classe basica, por favor "
                                  "implemente uma versão do parse_item.")

    def add_gen_code(self, gen_code, key, value):
        return ('{0}_{1}'.format(gen_code, key), value)

    def parse_list(self, gen_code, selected):
        """
        Usa o gen_code para separar as opções selecionadas desse gerador.
        Usa as seleções para retornar uma lista de usuarios que devem receber
        o aviso.
        """
        users = []
        for a in self.get_own(gen_code, selected):
            formated = a[a.find('_')+1:]  # Seleciona nomes após a underline
            users.extend(self.parse_item(formated))
        return users


class TodosAvisoMixedGenerator(AvisoMixedGeneratorBase):
    NOME_SECAO = "Todos"

    NOME_OPCAO_TODOS = 'Todos'
    CODIGO_OPCAO_TODOS = 'all'

    NOME_OPCAO_TODOS_ALUNOS = 'Todos os Alunos'
    CODIGO_OPCAO_TODOS_ALUNOS = 'all_alunos'

    NOME_OPCAO_TODOS_PROFESSORES = 'Todos os Professores'
    CODIGO_OPCAO_TODOS_PROFESSORES = 'all_professores'

    def generate_list(self, gen_code):
        choices = (self.NOME_SECAO, [
            # Todos
            ('{0}_{1}'.format(gen_code, self.CODIGO_OPCAO_TODOS),
             self.NOME_OPCAO_TODOS),
            # Todos Alunos
            ('{0}_{1}'.format(gen_code, self.CODIGO_OPCAO_TODOS_ALUNOS),
             self.NOME_OPCAO_TODOS_ALUNOS),
            # Todos Professores
            ('{0}_{1}'.format(gen_code, self.CODIGO_OPCAO_TODOS_PROFESSORES),
             self.NOME_OPCAO_TODOS_PROFESSORES),
            ])
        return choices

    def parse_item(self, item):
        if item == self.CODIGO_OPCAO_TODOS:
            return list(User.objects.all())
        elif item == self.CODIGO_OPCAO_TODOS_ALUNOS:
            return list(User.objects.filter(aluno__isnull=False))
        elif item == self.CODIGO_OPCAO_TODOS_PROFESSORES:
            return list(User.objects.filter(professor__isnull=False))
        else:
            logger.warning(
                f"Não há tratamento para a opção {item}, mas ela"
                f"foi gerada mesmo assim. EM TodosAvisoMixedGenerator")


class TurmaAvisoMixedGenerator(AvisoMixedGeneratorBase):
    NOME_SESSAO = "Turmas"

    def generate_list(self, gen_code):
        turmas = Turma.objects.all()
        turmas_choice = [self.add_gen_code(gen_code, x.pk, str(x)) for x in turmas]
        choices = (self.NOME_SESSAO, turmas_choice)
        return choices

    def parse_item(self, item):
        pk = int(item)
        turma = Turma.objects.get(pk=pk)
        users = turma.get_list_alunos
        return users


class AlunoAvisoMixedGenerator(AvisoMixedGeneratorBase):
    NOME_SESSAO = "Alunos"

    def generate_list(self, gen_code):
        alunos = Aluno.objects.all()
        alunos_choice = [self.add_gen_code(gen_code, x.pk, str(x)) for x in alunos]
        choices = (self.NOME_SESSAO, alunos_choice)
        return choices

    def parse_item(self, item):
        pk = int(item)
        aluno = Aluno.objects.get(pk=pk)
        users = [aluno.user]
        logger.debug(users)
        return users


class CreateAvisoMixedForm(forms.Form):
    destinatarios = forms.MultipleChoiceField(choices=(),
                                              widget=Select2MultipleWidget)
    titulo = forms.CharField(max_length=170)
    msg = MarkdownxFormField(max_length=5000, label='Mensagem')

    def __init__(self, owner, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.destinatariosGenerators = [
            TodosAvisoMixedGenerator,
            TurmaAvisoMixedGenerator,
            AlunoAvisoMixedGenerator
        ]
        self.fields['destinatarios'].choices = self.get_options()
        self.owner = owner
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', "Enviar Aviso"))

    def get_options(self):
        choices = []
        # Adiciona a opção de todos
        # Usando classes e uma list para gerar todas as opções
        # Cada classe recebe um numero para identificar suas opções,
        # e depois usa uma função para fazer o parse de todas suas
        # opções usando o numero
        for index, generator in enumerate(self.destinatariosGenerators):
            choices.append(generator().generate_list(index))
        return choices

    def get_user_list(self):
        """Retorna a lista de todos os usuarios selecionados"""
        users = []
        selected = self.cleaned_data['destinatarios']
        for index, generator in enumerate(self.destinatariosGenerators):
            logger.info(f"Generator n{index}")
            users.extend(generator().parse_list(index, selected=selected))
        logger.debug(f"{users} no get_user_list")
        return users

    def save(self):
        AvisoGeral.create(
            self.cleaned_data['titulo'],
            self.cleaned_data['msg'],
            self.owner,
            self.get_user_list())


class AdicionarMateriaConteudoForm(forms.Form):
    materias = forms.ModelMultipleChoiceField(
        queryset=MateriaDaTurma.objects.none())

    def __init__(self, materias, conteudo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['materias'].queryset = materias  # Define o campo com
        #                                              materias já definidas
        self.conteudo = conteudo  # Obtem o conteudo a ser lidado
        # Helper
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', "Adicionar"))

    def save(self):
        self.add_materia()

    def add_materia(self):
        materias = self.cleaned_data['materias']
        for materia in materias:
            # TODO: 06/04/2019 por wwwvi: Adicionar forma de retirar conteudos
            self.add_conteudo_na_materia(self.conteudo, materia)

    def add_conteudo_na_materia(self, conteudo: Conteudo, materia: MateriaDaTurma):

        if conteudo not in materia.conteudos.all():
            if conteudo.parent:
                if conteudo.parent not in materia.conteudos.all():
                    self.add_conteudo_na_materia(conteudo.parent)
            materia.conteudos.add(conteudo)
            materia.turma.comunicar_noti(
                'novo_conteudo',
                f"Um novo conteudo foi postado na materia {materia}",
                f"A materia {materia} recebeu um novo conteudo, "
                f"ele se chama {conteudo.nome}, para ver mais detalhes acesse o "
                f"conteudo.", conteudo.get_absolute_url())
