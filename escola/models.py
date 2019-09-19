"""
Models gerais do aplicativo Escola.
"""
import datetime
#  Developed by Vinicius José Fritzen
#  Last Modified 28/04/19 09:52.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import logging
from smtplib import SMTPException
from typing import List

from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import get_template
from django.urls import reverse
from markdownx.models import MarkdownxField
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager

import escola
from escola.customFields import ColorField
from escola.misaka import to_space_safe_html
from users.models import Aluno, Professor

logger = logging.getLogger(__name__)


class Profile(models.Model):
    """Perfil basico, todos os usuarios do sistema tem um."""
    user = models.OneToOneField(
        User, related_name='profile_escola', on_delete=models.CASCADE)
    is_aluno = models.BooleanField('student status', default=False)
    is_professor = models.BooleanField('teacher status', default=False)
    bio = MarkdownxField(blank=True, null=True)
    cor = models.CharField(max_length=12, blank=True, null=True)

    receber_email_notificacao = models.BooleanField(default=True)

    @property
    def template_data(self):
        """ Retorna valores basicos requeridos pelo template, como notificações, etc... """
        context = {
            'notificacoes': self.get_unread_notifications(),
            'notificacao_count': len(self.get_unread_notifications()),
        }
        return context

    def get_unread_notifications(self):
        """Retorna lista de todas as notificações não lidas desse usuario."""
        return self.user.notificacao_set.filter(visualizado=False).order_by('-dataCriado')

    def read_all_notifications(self):
        """Marca como lida todas as notificações"""
        for n in self.get_unread_notifications():
            n.visualizado = True
            n.save()

    def __str__(self):
        return f"Profile de {self.user.__str__()}"


class Notificador(models.Model):
    """
    Mantem lista de usuarios que seguem alguma coisa, deve ser criado um 
    para cada materia.
    """
    seguidores = models.ManyToManyField(User)

    def is_seguidor(self, user):
        """
        Verifica se determinado ususario está na lista de seguidores
        desse conteudo.
        """
        return user in self.seguidores.all()

    def adicionar_seguidor(self, user):
        """Adiciona um usuario a lista de seguidores."""
        self.seguidores.add(user)
        self.save()

    def remover_seguidor(self, user):
        if self.is_seguidor(user):
            self.seguidores.remove(user)
            self.save()

    def set_seguidor_state(self, user, state):
        if not self.is_seguidor(user) == state:
            if state:
                self.adicionar_seguidor(user)
            else:
                self.remover_seguidor(user)

    def toggle_seguidor(self, user):
        self.set_seguidor_state(user, not self.is_seguidor(user))

    def comunicar_todos(self, title, msg, link=None):
        """Cria uma notificação para cada usuario."""
        for seguidor in self.seguidores.all():
            # noti = Notificacao(user=seguidor, title=title, msg=msg)
            # # TODO Adicionar uma função que trata a msg permitindo que
            # partes sejam adicionadas a msg como nome do
            # #  usuario.
            # if self.link:
            #     noti.link = self.link
            # noti.save()
            Notificacao().create(
                seguidor, title, msg,
                deve_enviar=seguidor.profile_escola.receber_email_notificacao,
                link=link)
            # FIXME: o Deve enviar deve seguir preferencia do usuario


class Notificacao(models.Model):
    """Notificação para os usuarios, campos obrigatorios: user, title, msg; Campos Livres: link"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visualizado = models.BooleanField(default=False)
    dataCriado = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=160)
    msg = MarkdownxField()
    link = models.URLField(blank=True, null=True)

    email_criado = models.BooleanField(default=False)
    deve_enviar = models.BooleanField(default=False)

    @staticmethod
    def create(user, title, msg, deve_enviar=False, link=None):
        noti = Notificacao(user=user, title=title, msg=msg)
        # TODO Adicionar uma função que trata a msg permitindo que partes sejam adicionadas a msg como nome do
        #  usuario.
        if link:
            noti.link = link
        noti.deve_enviar = deve_enviar
        noti.save()

    def get_email_message(self):
        logger.info(f"Preparando para enviar email de notificação {self.pk}")
        plaintext = get_template(
            'escola/email/notificacao/nova_notificacao.txt')
        htmly = get_template('escola/email/notificacao/nova_notificacao.html')

        c = {'user': self.user,
             'dataCriado': self.dataCriado,
             'title': self.title,
             'msg': self.msg,
             'link': self.link or None,
             }

        subject, from_email, to = f'Nova notificação do Medusa II - {self.title}', settings.NOTIFICACAO_EMAIL, [
            self.user.email, ]

        text_content = plaintext.render(c)
        html_content = htmly.render(c)

        logger.info("Ultimas preparações para enviar o email de notificação!")
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        return msg

    def send_email(self):
        if self.deve_enviar and not self.email_criado:
            if self.user.email is not None:
                msg = self.get_email_message()
                logger.info("Enviando o email de notificação...")
                try:
                    msg.send()  # TODO Enviar assicrono
                except SMTPException as e:
                    logger.error(
                        f"Um email não foi enviado por causa de um error. {e}")
                else:
                    logger.info("Enviado o email de notificação!!")
                    self.email_criado = True
                    self.save()
            else:
                logger.info(
                    f'O usuario {self.user} não possui email, e portanto não pode receber notificações.')

    @classmethod
    def send_all_emails(cls):
        logger = logging.getLogger(__name__ + "-SendEmails")
        logger.info("Iniciando a coleta de notificações para mandar emails.")
        notificacoes = cls.objects.filter(email_criado=False, deve_enviar=True)
        c = len(notificacoes)
        if c == 0:
            logger.info("Não há notificações")
            return 0
        logger.info(f"Coletado {c} notificacoes.")
        messages = []
        logger.info("Gerando messages")
        for n in notificacoes:
            messages.append(n.get_email_message())
        try:
            logger.info("Mandando mensagens...")
            connection = mail.get_connection()
            logger.info("Abrindo conexão...")
            connection.open()
            logger.info("Enviando...")
            connection.send_messages(messages)
        except SMTPException as e:
            logger.error(f"Erro inexperado: {e}")
            raise
        else:
            logger.info(f"{c} mensagens foram enviadas!")
            for n in notificacoes:
                n.email_criado = True
                n.save()
        finally:
            connection.close()
        return len(notificacoes)


class NotificacaoDoesNotExistError(Exception):
    pass


class NotificacaoCantHaveNoName(Exception):
    pass


class Turma(models.Model):
    """ Uma turma, conjunto de alunos, materias, tarefas, tambem possui um horario"""
    numero = models.IntegerField()
    ano = models.IntegerField()

    lider = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                              null=True, blank=True, related_name='turma_lider')
    vicelider = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True,
                                  related_name='turma_vicelider')
    regente = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='turma_regente')

    poss_noti = (
        ("nova_tarefa", "Há uma nova tarefa", True),
        ("nova_prova", "Há uma nova prova", True),
        ("prova_proxima", "Uma prova está próxima", True),
        ("tarefa_proxima", "Uma tarefa não completa está próxima", True),
        ("novo_conteudo", "Um professor postou um novo conteúdo", True),
        ("aviso_geral_turma", "Um professor postou um novo conteudo", True),
    )

    noti_nova_tarefa = models.OneToOneField(
        Notificador, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='+')
    noti_nova_prova = models.OneToOneField(
        Notificador, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='+')
    noti_prova_proxima = models.OneToOneField(
        Notificador, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='+')
    noti_tarefa_proxima = models.OneToOneField(
        Notificador, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='+')
    noti_novo_conteudo = models.OneToOneField(
        Notificador, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='+')
    noti_aviso_geral_turma = models.OneToOneField(
        Notificador, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='+')

    def get_poss_notis(self):
        """Retorna lista de possiveis notificadores"""
        return [a for a in self.poss_noti]

    @staticmethod
    def formatar_nome(name):
        """Formata o nome para o formato das variaveis"""
        if name == "":
            raise NotificacaoCantHaveNoName
        return f"noti_{name}"

    def has_noti(self, name):
        """Verifica se possui o notificador"""
        return name in [nome for nome, desc, default in self.get_poss_notis()]

    def has_def_noti(self, name):
        """Verifica se possui o notificador"""
        return hasattr(self, self.formatar_nome(name)) and getattr(self, self.formatar_nome(name)) is not None

    def get_noti_default(self, nome):
        return [default for name, desc, default in self.get_poss_notis() if name == nome][0]

    def create_notificador(self, name):
        notificador = Notificador()
        notificador.save()
        if self.get_noti_default(name):
            for user in self.get_list_alunos():
                notificador.seguidores.add(user)
        notificador.save()
        setattr(self, self.formatar_nome(name), notificador)
        self.save()

    def get_noti(self, name) -> Notificador:
        """Retorna o notificador que possui este nome"""
        if self.has_noti(name):
            if not self.has_def_noti(name):
                self.create_notificador(name)
            return getattr(self, self.formatar_nome(name))
        else:
            raise NotificacaoDoesNotExistError

    def get_noti_status(self, name, user):
        """Retorna o status de uma noti"""
        return self.get_noti(name).is_seguidor(user)

    def get_all_notis_and_status(self, user):
        """Retorna os notificadores e seus estados"""
        return [(nome, desc, self.get_noti_status(nome, user)) for nome, desc, default in self.get_poss_notis()]

    def comunicar_noti(self, nome_noti, titulo, msg, link=None):
        self.get_noti(nome_noti).comunicar_todos(titulo, msg, link)

    class Meta:
        """Meta das Models"""
        permissions = (('can_add_turma', "Pode criar turmas"),
                       ('can_edit_turma', "Pode editar turmas"),
                       ('can_delete_turma', "Pode deletar turmas"),
                       ('can_populate_turma', "Pode popular turmas"),
                       ('can_add_aluno', "Pode adicionar um aluno a turma."),
                       ('editar_horario', "Pode editar o horario."),
                       ('can_add_materia', 'Pode adicionar uma materia a turma.'),
                       ('can_add_tarefa', "Pode adicionar uma tarefa."))

    def get_or_create_horario(self):
        """Retorna ou cria e retorna o horario."""
        try:
            return self.horario
        except escola.models.Turma.horario.RelatedObjectDoesNotExist:
            h = Horario(turma=self)
            h.save()
            return h

    def get_list_alunos(self):
        """Retorna a lista de user da aluno"""
        return [a.user for a in self.aluno_set.all()]

    def __str__(self):
        return f"Turma {self.numero}"

    @staticmethod
    def atualizaProvas():
        startdate = datetime.date.today()
        enddate = startdate + datetime.timedelta(days=1, hours=6)
        provas_ma = ProvaMateriaMarcada.objects.filter(_prova__evento__evento__data__range=[
                                                       startdate, enddate], _prova__notificado=False)
        for prova in provas_ma:
            prova: ProvaMateriaMarcada
            prova.get_turma().comunicar_noti('prova_proxima', f'A prova {prova.get_nome()} está se aproximando',
                                             f'Ela ocorrerá dia {prova.get_data().strftime("%d/%m/%y")}, da materia {prova.get_apresentacao()}', prova.get_absolute_url())
            prova.set_notificado(True)
        provas_a = ProvaAreaMarcada.objects.filter(_prova__evento__evento__data__range=[
                                                   startdate, enddate], _prova__notificado=False)
        for prova in provas_a:
            prova: ProvaAreaMarcada
            prova.get_turma().comunicar_noti('prova_proxima', f'A prova de area {prova.get_nome()} está se aproximando',
                                             f'Ela ocorrerá dia {prova.get_data().strftime("%d/%m/%y")}, das materias {prova.get_apresentacao()}', prova.get_absolute_url())
            prova.set_notificado(True)

    @staticmethod
    def atualizaTarefas():
        startdate = datetime.date.today()
        enddate = startdate + datetime.timedelta(days=1, hours=6)
        tarefas = Tarefa.objects.filter(
            deadline__range=[startdate, enddate], notificado=False)
        for tarefa in tarefas:
            tarefa: Tarefa
            tarefa.turma.comunicar_noti('tarefa_proxima', "Uma tarefa está proxima de sua data de completação.",
                                        f"A tarefa {tarefa.titulo} está proxima de sua data final. Verifique se você já a completou. A data máxima é dia {tarefa.deadline.strftime('%d/%m/%Y')}")
            tarefa.notificado = True
            tarefa.save()


class CargoTurma(models.Model):
    """Um cargo dentro de uma turma como lider, regente e vice"""
    nome = models.CharField(max_length=50)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    ocupante = models.ForeignKey(User, on_delete=models.CASCADE)
    CODS_ESPECIAIS = (
        (0, 'Não especifico'),
        (1, 'Lider'),
        (2, 'Vice-lider'),
        (3, 'Suplente'),
        (4, 'Tesoureiro'),
        (5, 'Prof. Regente'),
    )
    cod_especial = models.PositiveSmallIntegerField(choices=CODS_ESPECIAIS)
    ativo = models.BooleanField(default=True)

    class Meta:
        """Meta, contem metas"""
        permissions = (('can_add_cargo', "Pode criar Cargo"),
                       ('can_edit_cargo', "Pode editar Cargo"),
                       ('can_delete_cargo', "Pode deletar Cargo"),
                       ('can_designar_cargo', "Pode designar alguem para o cargo"),)  # Não usado, depricated?

    def __str__(self):
        return f"Cargo {self.nome} da turma {self.turma.numero}"


class Professor(models.Model):
    """Um professor, não esecifico para uma turma."""
    user = models.OneToOneField(
        User, related_name='professor', on_delete=models.CASCADE)
    nome = models.CharField(max_length=70)

    def __str__(self):
        return self.nome

    class Meta:
        """Classe meta"""
        permissions = (('can_add_professor', 'Pode adicionar um novo Professor'),
                       ('can_edit_professor', 'Pode editar um professor'),
                       ('can_delete_professor', 'Pode deletar um professor'),)
        ordering = ['nome']


class Conteudo(MPTTModel):
    """Conteudo que pode ser o filho de outro."""
    nome = models.CharField(max_length=50)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    descricao = MarkdownxField()
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)

    def get_absolute_url(self):
        """Retorna Url do conteudo."""
        return reverse('escola:conteudo-detail', kwargs={'pk': self.pk})

    class Meta:
        """META"""
        verbose_name = "Conteudo"
        verbose_name_plural = "Conteudos"

        permissions = (
            ('can_add_in_materia', 'Pode adicionar esse conteudo à uma materia.'),)

    def __str__(self):
        return self.nome


class CategoriaConteudo(models.Model):
    """
    Uma cateogoria de um conteudo, inicialmente
    'Para se aprofundar',
    'Para revisar',
    'Para expandir seus horizontes'.
    """
    nome = models.CharField(max_length=50)
    cor = ColorField(default='#0e74ce')

    class Meta:
        """META"""
        verbose_name = "Categoria de Link de Conteudos"
        verbose_name_plural = "Categorias de Links de Conteudos"

    def __str__(self):
        return self.nome


class LinkConteudo(models.Model):
    """Um link em conteudo."""
    titulo = models.CharField(max_length=50)
    link = models.URLField()
    categoria = models.ForeignKey(CategoriaConteudo, on_delete=models.CASCADE)
    descricao = MarkdownxField(null=True, blank=True)
    conteudo = models.ForeignKey(Conteudo, on_delete=models.CASCADE)
    tags = TaggableManager()

    class Meta:
        """META"""
        verbose_name = "Link de Conteudo"
        verbose_name_plural = "Links de Conteudos"

    def __str__(self):
        return self.titulo


class AreaConhecimento(models.Model):
    """Area do conhecimento"""
    nome = models.CharField(max_length=40)
    turma = models.ForeignKey(Turma, models.CASCADE, 'Area')

    def __str__(self):
        return f"{self.nome.upper()}/{self.turma.numero}"

    def get_materias(self):
        """Retorna as materias desta area"""
        return self.materias.all()

    def get_materias_str(self):
        """
        Retorna a lista de materias no formato string.
        Ex.
            "Matematica"
            "Portugues, Ingles"
        """
        mats = self.get_materias()
        if len(mats) == 1:
            return f"{mats[0].nome}"
        str_nomes = ''
        for m in mats:
            if not str_nomes == "":
                str_nomes += ", "
            str_nomes += f"{m.nome}"
        return str_nomes


class MateriaManager(models.Manager):
    def filter_from_professor(self, professor):
        return super().filter(professor=professor).all()

    def filter_from_professor_for_day(self, professor, day):
        # return [a for a in self.filter_from_professor(professor).all() if a.has_aula_in_day(day)]
        return {p.materia for p in Periodo.objects.filter(turnoAula__diaDaSemana=day, materia__professor=professor)}


class MateriaDaTurma(models.Model):
    """Materia de uma turma, possui um professor e é dedicada a uma turma."""
    nome = models.CharField(max_length=50)
    professor = models.ForeignKey(
        Professor, on_delete=models.CASCADE, related_name='materias')
    turma = models.ForeignKey(
        Turma, on_delete=models.CASCADE, related_name='materias')
    abreviacao = models.CharField(max_length=5)
    conteudos = models.ManyToManyField(
        Conteudo, blank=True, related_name='materias')
    area = models.ForeignKey(AreaConhecimento, on_delete=models.CASCADE,
                             related_name='materias', null=True, blank=True)

    objects = models.Manager()
    helper = MateriaManager()

    def __str__(self):
        return f"{self.nome}/{self.turma.numero}"

    def get_professor(self):
        return self.professor

    class Meta:
        """Meta"""
        permissions = (('can_edit_materia', 'Pode editar uma materia'),
                       ('can_delete_materia', 'Pode deletar uma materia'),)
        ordering = ['nome', 'area', 'professor']


class Aluno(models.Model):
    """Aluno de uma turma."""
    chamada = models.PositiveSmallIntegerField(
        null=True, blank=True, default=0)
    nome = models.CharField(max_length=70)
    user = models.OneToOneField(
        User, related_name='aluno', on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    class Meta:
        """Meta"""
        permissions = (('edit_aluno', 'Pode editar um aluno.'),
                       ('can_delete_aluno', 'Pode deletar um aluno.'),)


class Tarefa(models.Model):
    """Tarefa para com prazo, como um tema, ou pesquisa"""
    titulo = models.CharField(max_length=60)
    turma: Turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    materia = models.ForeignKey(MateriaDaTurma, on_delete=models.CASCADE)
    TIPOS = (
        (1, 'Tema'),
        (2, 'Trabalho'),
        (3, 'Pesquisa'),
        (4, 'Redação'),
    )
    tipo = models.PositiveSmallIntegerField(
        choices=TIPOS, blank=True, null=True)
    descricao = MarkdownxField()
    deadline = models.DateField(verbose_name='Data limite')
    noti_comentario = models.OneToOneField(
        Notificador, on_delete=models.DO_NOTHING, null=True, blank=True)
    notificado = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('escola:detalhes-tarefa', args=(self.pk, ))

    def get_completacao(self, aluno):
        """Retorna se já foi completado."""
        completo = self.tarefacompletacao_set.filter(aluno=aluno)
        if len(completo) > 0:
            return completo[0]
        else:
            completo = TarefaCompletacao(tarefa=self, aluno=aluno)
            completo.save()
            return completo

    @classmethod
    def create(cls, titulo, turma: Turma, materia, tipo, descricao, deadline):
        tarefa = cls()
        tarefa.titulo = titulo
        tarefa.turma = turma
        tarefa.materia = materia
        tarefa.tipo = tipo
        tarefa.descricao = descricao
        tarefa.deadline = deadline
        tarefa.save()
        turma.comunicar_noti('nova_tarefa',
                             "Há uma nova tarefa em sua turma",
                             f"A Tarefa \"{titulo}\" foi criada com data final em {deadline}. Para ver mais detalhes siga o link.",
                             tarefa.get_absolute_url())
        return tarefa

    def get_seguidor_manager(self):
        """Retorna o SeguidorManager dessa tarefa."""
        if self.noti_comentario:
            return self.noti_comentario
        else:
            m = Notificador()
            m.save()
            self.noti_comentario = m
            self.save()
            return self.noti_comentario

    class Meta:
        """Meta"""
        permissions = (('can_edit_tarefa', 'Pode editar uma tarefa.'),
                       ('can_delete_tarefa', 'Pode deletar uma tarefa.'),)


class TarefaCompletacao(models.Model):
    """Completação de uma tarefa especifica por um aluno especifico."""
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    completo = models.BooleanField(default=False)


class TarefaComentario(models.Model):
    """Comentario em uma tarefa por um usuario."""
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    texto = MarkdownxField()
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)


class Horario(models.Model):
    """O horario de uma turma."""
    turma = models.OneToOneField(
        Turma, related_name='horario', on_delete=models.CASCADE)

    def get_turno_aula_or_create(self, dia, turno_a):
        """Retorna um turno ou o cria"""
        turno = TurnoAula.objects.filter(
            diaDaSemana=dia, turno=turno_a, turma=self.turma)
        if turno:
            return turno[0]
        else:
            turno = TurnoAula(turma=self.turma, horario=self,
                              diaDaSemana=dia, turno=turno_a)
            turno.save()
            return turno

    def get_periodo_or_create(self, dia, turno: int, num):
        """Retorna um periodo ou cria um novo"""
        turno_aula = self.get_turno_aula_or_create(
            dia, Turno.get_turno_by_cod(turno))
        per = turno_aula.periodo_set.filter(num=num)
        if per:
            return per[0]
        else:
            per = Periodo(turnoAula=turno_aula, num=num)
            per.save()
            return per

    def get_horario(self):
        """Retorna o horario, como lista de Turnos"""
        logger.debug('horario:get_horario()')
        turnos = Turno.objects.all().order_by('cod')
        logger.info('Puxou %s turno(s) do banco de dados.', len(turnos))
        DIAS_DA_SEMANA_N = range(1, 8)
        ta = {}
        logger.info('Preparando para entrar no loop de turnos...')
        for turno in turnos:
            logger.debug('Turno id:%s', turno.pk)
            # Passa todos os dias da semana
            for dia in DIAS_DA_SEMANA_N:
                # Pega Turnos de Aula em que o turno, dia e horario seja certo;
                a = TurnoAula.objects.filter(
                    turno=turno, diaDaSemana=dia, horario=self)
                # Se houver um turno
                if len(a) > 0:
                    # Se esse dia não estiver na lista de horario que sai adiciona
                    if dia not in ta:
                        ta[dia] = dict()
                    # Salva o turno aula na saida
                    ta[dia][turno.cod] = a[0]
        return ta


class Turno(models.Model):
    """Um turno como matututino ou vespertino"""
    # TODO: 12/05/2019 por wwwvi: Adicionar maneira de flexibilizar quantidade de periodos
    nome = models.CharField(max_length=30)
    cod = models.PositiveSmallIntegerField()
    horaInicio = models.TimeField(blank=True, null=True)
    # 1
    s1 = models.TimeField(blank=True, null=True)
    # 2
    s2 = models.TimeField(blank=True, null=True)
    # 3
    s3 = models.TimeField(blank=True, null=True)
    # intervalo
    s4 = models.TimeField(blank=True, null=True)
    # 4
    s5 = models.TimeField(blank=True, null=True)
    # 5
    horaFim = models.TimeField(blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.nome

    @staticmethod
    def get_turno_by_cod(cod):
        return Turno.objects.filter(cod=cod)[0]


class TurnoAula(models.Model):
    """Um turno de aula tem um dia da semana, turno e uma turma """
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    DIAS_DA_SEMANA = (   # Segundo a ISO
        (1, 'Segunda-feira'),
        (2, 'Terça-feira'),
        (3, 'Quarta-feira'),
        (4, 'Quinta-feira'),
        (5, 'Sexta-feira'),
        (6, 'Sábado'),
        (7, 'Domingo'),
    )
    diaDaSemana = models.PositiveSmallIntegerField(choices=DIAS_DA_SEMANA)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)


class Periodo(models.Model):
    """Um periodo de aula"""
    num = models.PositiveSmallIntegerField()
    turnoAula = models.ForeignKey(TurnoAula, on_delete=models.CASCADE)
    materia = models.ForeignKey(
        MateriaDaTurma, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def dia(self):
        return self.turnoAula.diaDaSemana

    @property
    def turma(self):
        return self.turnoAula.turma

    @property
    def turno_cod(self):
        return self.turnoAula.turno.cod


# class MetodoAvaliativo(Enum):
#     """Enumerado de metodos de registrar uma nota"""
#     CONCEITO = ('CONCEITO', NotaConceito)
#     PORCENTAGEM = ('PORCENTAGEM', NotaPercentual)
#
#     def __init__(self, name, klass):
#         self.nome = name
#         self.klass = klass
#
#     @property
#     def tupleChoice(self):
#         return self.name, self.name.title()


# class ItemAvaliativo(PolymorphicModel):
#     """Um item que será avaliado, com  nota"""
#     nome = models.CharField(max_length=90)
#     numero = models.IntegerField()
#     nota = JSONField(null=True, blank=True)
#     metodosAvaliativos = [m.tupleChoice for m in MetodoAvaliativo]
#     metodoNota = models.CharField(max_length=30, choices=metodosAvaliativos)
#
#     def get_materias(self) -> List[MateriaDaTurma]:
#         return []


# class ItemAvaliativoMateria(ItemAvaliativo):
#     materia = models.ForeignKey(MateriaDaTurma, models.CASCADE)
#
#     def get_materias(self):
#         return [self.materia, ]
#
#
# class ItemAvaliativoArea(ItemAvaliativo):
#     area = models.ForeignKey(AreaConhecimento, models.CASCADE)
#
#     def get_materias(self) -> List[MateriaDaTurma]:
#         """Retorna lista de materias dessa prova"""
#         return self.area.get_materias()


class Evento(models.Model):
    """Uma data especial que aparecerá em um calendario"""
    nome = models.CharField(max_length=70)
    data = models.DateTimeField()
    descricao = MarkdownxField()

    owner = models.ForeignKey(User, models.CASCADE, null=True, blank=True)

    def get_nome(self):
        return self.nome

    def __str__(self):
        return self.get_nome()

    def get_data(self) -> datetime:
        """Retorna data do evento"""
        return self.data

    def get_descricao(self):
        """Retorna a descrição do evento"""
        return self.descricao

    def get_owner(self):
        return self.owner

    def has_permition_edit(self, user: User) -> bool:
        """Retorna True se o usuario tem permissão para editar o evento"""
        if user == self.owner:
            return True
        return False

    @staticmethod
    def create(nome, data, descricao, owner):
        a = Evento()
        a.nome = nome
        a.data = data
        a.descricao = descricao
        a.owner = owner
        a.save()
        return a

    def update(self, *args, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])
        self.save()


class EventoTurma(models.Model):
    """Uma data especial de uma turma"""
    turma: Turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    evento: Evento = models.ForeignKey(Evento, on_delete=models.CASCADE)

    block_prova = models.BooleanField(default=True)

    def delete(self, using=None, keep_parents=False):
        self.evento.delete(using, keep_parents)
        super(EventoTurma, self).delete(using, keep_parents)

    def __str__(self):
        return self.get_nome()

    def get_participantes(self):
        """Retorna lista de participante, alunos da turma"""
        return self.turma.get_list_alunos()

    def get_nome(self):
        return self.evento.get_nome()

    def get_data(self) -> datetime:
        """Retorna data do evento"""
        return self.evento.get_data()

    def get_descricao(self):
        """Retorna a descrição do evento"""
        return self.evento.get_descricao()

    def get_owner(self):
        return self.evento.get_owner()

    def has_permition_edit(self, user: User) -> bool:
        """Retorna True se o usuario tem permissão para editar o evento"""
        if user == self.get_owner():
            return True
        return False

    def get_turma(self):
        return self.turma

    @staticmethod
    def create(turma, nome, data, descricao, owner, block_prova=True):
        a = EventoTurma()
        a.evento = Evento.create(nome, data, descricao, owner)
        a.turma = turma
        a.block_prova = block_prova
        a.save()
        return a

    def update(self, *args, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])
        self.save()


class EventoEscola(models.Model):
    """Uma data especial de uma turma"""
    evento: Evento = models.ForeignKey(Evento, on_delete=models.CASCADE)

    block_prova = models.BooleanField(default=True)

    def delete(self, using=None, keep_parents=False):
        self.evento.delete(using, keep_parents)
        super(EventoTurma, self).delete(using, keep_parents)

    def __str__(self):
        return self.get_nome()

    def get_participantes(self):
        """Retorna lista de participante, todos da Escola"""
        return User.objects.all()

    def get_nome(self):
        return self.evento.get_nome()

    def get_data(self) -> datetime:
        """Retorna data do evento"""
        return self.evento.get_data()

    def get_descricao(self):
        """Retorna a descrição do evento"""
        return self.evento.get_descricao()

    def get_owner(self):
        return self.evento.get_owner()

    def has_permition_edit(self, user: User) -> bool:
        """Retorna True se o usuario tem permissão para editar o evento"""
        if user == self.get_owner():
            return True
        return False

    def get_turma(self):
        return self.turma

    @staticmethod
    def create(nome, data, descricao, owner, block_prova=True):
        a = EventoEscola()
        a.evento = Evento.create(nome, data, descricao, owner)
        a.block_prova = block_prova
        a.save()
        return a

    def update(self, *args, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])
        self.save()


class ProvaMarcada(models.Model):
    """Uma prova"""
    conteudos = models.ManyToManyField(Conteudo, blank=True)
    evento: EventoTurma = models.ForeignKey(
        EventoTurma, on_delete=models.CASCADE, related_name='prova')
    notificado = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        self.evento.delete(using, keep_parents)
        super(ProvaMarcada, self).delete(using, keep_parents)

    def set_notificado(self, value: bool):
        self.notificado = value
        self.save()

    def get_notificado(self) -> bool:
        return self.notificado

    def get_uper(self):
        if hasattr(self, 'p_area'):
            return self.p_area
        elif hasattr(self, 'p_materia'):
            return self.p_materia

    def get_materias(self):
        """Retorna lista de materias da prova"""
        return self.get_uper().get_materias()

    def get_materias_text(self):
        return ', '.join(m.__str__() for m in self.get_materias())

    def __str__(self):
        return self.get_nome()

    def get_conteudos(self) -> List[MateriaDaTurma]:
        """Retorna lista de conteudos dessa prova"""
        s = self.conteudos
        g = []
        for item in s:
            g += [item, ]
        return g

    def add_conteudo(self, conteudo):
        if conteudo.parent:
            self.add_conteudo(conteudo.parent)
        if conteudo not in self.conteudos:
            self.conteudos.add(conteudo)

    def add_conteudos(self, conteudos):
        for c in conteudos:
            self.add_conteudo(c)

    def get_participantes(self):
        """Retorna lista de participante, alunos da turma"""
        return self.evento.get_participantes()

    def get_nome(self):
        return self.evento.get_nome()

    def get_data(self) -> datetime:
        """Retorna data do evento"""
        return self.evento.get_data()

    def get_descricao(self):
        """Retorna a descrição do evento"""
        return self.evento.get_descricao()

    def get_owner(self):
        return self.evento.get_owner()

    def get_turma(self):
        return self.evento.get_turma()

    def has_permition_edit(self, user: User) -> bool:
        """Retorna True se o usuario tem permissão para editar o evento"""
        if user == self.get_owner():
            return True
        return False

    @staticmethod
    def create(turma, nome, data, descricao, owner, conteudos=None):
        a = ProvaMarcada()
        a.evento = EventoTurma.create(
            turma, nome, data, descricao, owner, True)
        a.save()
        if conteudos:
            a.add_conteudos(conteudos)
        return a


class ProvaMateriaMarcada(models.Model):
    """Prova de uma materia"""
    materia: MateriaDaTurma = models.ForeignKey(
        MateriaDaTurma, on_delete=models.CASCADE, related_name='provas_materia')
    # item_avaliativo = models.ForeignKey(ItemAvaliativoMateria, on_delete=models.CASCADE)
    _prova: ProvaMarcada = models.OneToOneField(
        ProvaMarcada, on_delete=models.CASCADE, related_name='p_materia')

    def delete(self, using=None, keep_parents=False):
        self._prova.delete(using, keep_parents)
        super(ProvaMateriaMarcada, self).delete(using, keep_parents)

    def __str__(self):
        return self.get_nome()

    def set_notificado(self, value):
        self._prova.set_notificado(value)

    def get_notificado(self):
        return self._prova.get_notificado()

    def get_apresentacao(self):
        return f"{self.materia.nome}"

    def get_materias(self) -> List[MateriaDaTurma]:
        """Retorna lista de materias dessa prova"""
        return [self.materia, ]

    def get_conteudos(self):
        return self._prova.get_conteudos()

    def add_conteudo(self, c):
        return self._prova.add_conteudo(c)

    def add_conteudos(self, clist):
        return self._prova.add_conteudos(clist)

    def update(self, *args, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])
        self.save()

    def get_participantes(self):
        """Retorna lista de participante, alunos da turma"""
        return self._prova.get_participantes()

    def get_nome(self):
        return self._prova.get_nome()

    def get_data(self) -> datetime:
        """Retorna data do evento"""
        return self._prova.get_data()

    def get_descricao(self):
        """Retorna a descrição do evento"""
        return self._prova.get_descricao()

    def get_owner(self):
        return self._prova.get_owner()

    def has_permition_edit(self, user: User) -> bool:
        """Retorna True se o usuario tem permissão para editar o evento"""
        if user == self.get_owner():
            return True
        return False

    def get_turma(self):
        return self._prova.get_turma()

    def get_conteudo_materia(self, materia):
        pass

    def get_absolute_url(self):
        return reverse('escola:prova-detail', kwargs={'pk': self._prova.pk})

    @staticmethod
    def create(materia: MateriaDaTurma, nome, data, descricao, owner, conteudos=None):
        a = ProvaMateriaMarcada()
        turma: Turma = materia.turma
        a._prova = ProvaMarcada.create(
            turma, nome, data, descricao, owner, conteudos)
        a.materia = materia
        a.save()
        turma.comunicar_noti('nova_prova', f"Uma prova foi marcada para dia {data.strftime('%d/%m/%y')} ",
                             f"A prova {nome}, foi marcada para dia {data.strftime('%d/%m/%y')}, da materia {materia}. Estude até lá!", a.get_absolute_url())
        return a


class ProvaAreaMarcada(models.Model):
    """Prova de Area"""
    area: AreaConhecimento = models.ForeignKey(
        AreaConhecimento, on_delete=models.CASCADE, related_name='provas_area')
    # item_avaliativo = models.ForeignKey(ItemAvaliativoArea, on_delete=models.CASCADE)
    _prova: ProvaMarcada = models.OneToOneField(
        ProvaMarcada, on_delete=models.CASCADE, related_name='p_area')

    def delete(self, using=None, keep_parents=False):
        self._prova.delete(using, keep_parents)
        super(ProvaAreaMarcada, self).delete(using, keep_parents)

    def get_materias(self) -> List[MateriaDaTurma]:
        """Retorna lista de materias dessa prova"""
        return self.area.get_materias()

    def set_notificado(self, value):
        self._prova.set_notificado(value)

    def get_notificado(self):
        return self._prova.get_notificado()

    def __str__(self):
        return self.get_nome()

    def get_conteudos(self):
        return self._prova.get_conteudos()

    def add_conteudo(self, c):
        return self._prova.add_conteudo(c)

    def add_conteudos(self, clist):
        return self._prova.add_conteudos(clist)

    def update(self, *args, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])
        self.save()

    def get_participantes(self):
        """Retorna lista de participante, alunos da turma"""
        return self._prova.get_participantes()

    def get_nome(self):
        return self._prova.get_nome()

    def get_data(self) -> datetime:
        """Retorna data do evento"""
        return self._prova.get_data()

    def get_descricao(self):
        """Retorna a descrição do evento"""
        return self._prova.get_descricao()

    def get_owner(self):
        return self._prova.get_owner()

    def has_permition_edit(self, user: User) -> bool:
        """Retorna True se o usuario tem permissão para editar o evento"""
        if user == self.get_owner():
            return True
        return False

    def get_turma(self):
        return self._prova.get_turma()

    def get_apresentacao(self):
        return f"Area: {self.area}({self.area.get_materias_str()})"

    @staticmethod
    def create(area: AreaConhecimento, nome, data, descricao, owner, conteudos=None):
        a = ProvaAreaMarcada()
        turma = area.turma
        a._prova = ProvaMarcada.create(
            turma, nome, data, descricao, owner, conteudos)
        a.area = area
        a.save()
        turma.comunicar_noti('nova_prova', f"Uma prova de área foi marcada para dia {data.strftime('%d/%m/%y')}",
                             f"A prova {nome}, foi marcada para dia {data.strftime('%d/%m/%y')}, da área {area}. Estude até lá!", a.get_absolute_url())
        return a

    def get_absolute_url(self):
        return reverse('escola:prova-detail', kwargs={'pk': self._prova.pk})


class AvisoGeral(models.Model):
    titulo = models.CharField(max_length=170)
    msg = MarkdownxField()
    owner = models.ForeignKey(User, models.DO_NOTHING,
                              related_name="avisos_publicados", null=True,
                              blank=True)
    destinatarios = models.ManyToManyField(User,
                                           related_name="avisos_recebidos")

    def gerar_notis(self):
        for destino in self.destinatarios.all():
            Notificacao().create(
                destino,
                f"AVISO:{self.titulo}",
                f"Você recebeu um novo aviso, criado por {self.owner}, por"
                f" favor, leia-o.",
                deve_enviar=destino.profile_escola.receber_email_notificacao,
                link=self.get_absolute_url())

    def get_absolute_url(self):
        # return reverse
        return reverse('escola:aviso-detail', args=(self.pk, ))

    @staticmethod
    def create(titulo, msg, owner, destinatarios, gerar_notis=True):
        aviso = AvisoGeral()
        aviso.titulo = titulo
        aviso.msg = msg
        aviso.owner = owner
        aviso.save()
        aviso.destinatarios.add(*destinatarios)
        aviso.save()

        if gerar_notis:
            aviso.gerar_notis()

        return aviso

    @staticmethod
    def create_for_turma(titulo, msg, owner, turma: Turma):
        a = AvisoGeral.create(titulo, msg, owner, turma.get_list_alunos(),
                              gerar_notis=False)
        turma.comunicar_noti('aviso_geral_turma', f"AVISO DA TURMA: {titulo}",
                             f"Aviso enviado por {owner}.",
                             a.get_absolute_url())
