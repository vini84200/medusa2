from django.contrib.auth.models import User, Group
from django.db import models
from django_prometheus.models import ExportModelOperationsMixin
from django.urls import reverse
from guardian.shortcuts import assign_perm
from model_utils.managers import InheritanceManager


# Create your models here.


class Profile(models.Model, ExportModelOperationsMixin('Profiles')):
    user = models.OneToOneField(User, related_name='profile_escola', on_delete=models.CASCADE)
    is_aluno = models.BooleanField('student status', default=False)
    is_professor = models.BooleanField('teacher status', default=False)
    bio = models.TextField(blank=True, null=True)
    cor = models.CharField(max_length=12, blank=True, null=True)

    @property
    def template_data(self):
        context = {
            'notificacoes': self.get_unread_notifications(),
            'notificacao_count': len(self.get_unread_notifications()),
        }
        return context

    def get_unread_notifications(self):
        return self.user.notificacao_set.filter(visualizado=False).order_by('dataCriado')

    def read_all_notifications(self):
        for n in self.get_unread_notifications():
            n.visualizado = True
            n.save()

    def __str__(self):
        return f"Profile de {self.user.__str__()}"


class Turma(models.Model, ExportModelOperationsMixin('Turma')):
    numero = models.IntegerField()
    ano = models.IntegerField()
    lider = models.ForeignKey(Group, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='turma_lider')
    vicelider = models.ForeignKey(Group, on_delete=models.DO_NOTHING, null=True, blank=True,
                                  related_name='turma_vicelider')
    regente = models.ForeignKey(Group, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='turma_regente')

    class Meta:
        permissions = (('can_add_turma', "Pode criar turmas"),
                       ('can_edit_turma', "Pode editar turmas"),
                       ('can_delete_turma', "Pode deletar turmas"),
                       ('can_populate_turma', "Pode popular turmas"),
                       ('can_add_aluno', "Pode adicionar um aluno a turma."))

    def get_or_create_lider_group(self):
        if self.lider:
            return self.lider
        else:
            if Group.objects.filter(name=f'lider_turma_{self.pk}').exists:
                self.lider = Group.objects.get(name=f'lider_turma_{self.pk}')
            else:
                self.lider = Group.objects.create(name=f'lider_turma_{self.pk}')
            assign_perm('escola.editar_horario', self.lider, self.horario)
            assign_perm('escola.can_add_materia', self.lider, self)
            assign_perm('escola.can_edit_materia', self.lider, self)
            assign_perm('escola.can_delete_materia', self.lider, self)
            assign_perm('escola.can_add_tarefa', self.lider, self)
            assign_perm('escola.can_edit_tarefa', self.lider, self)
            assign_perm('escola.can_delete_tarefa', self.lider, self)
            return self.lider

    def get_or_create_vicelider_group(self):
        if self.vicelider:
            return self.vicelider
        else:
            if Group.objects.filter(name=f'vicelider_turma_{self.pk}').exists:
                self.vicelider = Group.objects.get(name=f'vicelider_turma_{self.pk}')
            else:
                self.vicelider = Group.objects.create(name=f'vicelider_turma_{self.pk}')
            assign_perm('escola.editar_horario', self.vicelider, self)
            assign_perm('escola.can_add_materia', self.vicelider, self)
            assign_perm('escola.can_edit_materia', self.vicelider, self)
            assign_perm('escola.can_add_tarefa', self.vicelider, self)
            assign_perm('escola.can_edit_tarefa', self.vicelider, self)
            return self.vicelider

    def get_or_create_regente_group(self):
        if self.regente:
            return self.regente
        else:
            if Group.objects.filter(name=f'regente_turma_{self.pk}').exists:
                self.regente = Group.objects.get(name=f'regente_turma_{self.pk}')
            else:
                self.regente = Group.objects.create(name=f'regente_turma_{self.pk}')
            assign_perm('escola.can_add_aluno', self.regente, self)
            assign_perm('escola.editar_horario', self.regente, self)
            assign_perm('escola.can_add_materia', self.regente, self)
            assign_perm('escola.can_edit_materia', self.regente, self)
            assign_perm('escola.can_delete_materia', self.regente, self)
            assign_perm('escola.can_add_tarefa', self.regente, self)
            assign_perm('escola.can_edit_tarefa', self.regente, self)
            assign_perm('escola.can_delete_tarefa', self.regente, self)
            return self.regente
    def __str__(self):
        return f"Turma {self.numero}"

    def is_lider(self, user: User):
        lider = self.get_lider()
        if lider is None:
            return False
        elif lider == user:
            return True
        else:
            return False

    def is_regente(self, user: User):
        regente = self.get_regente()
        if regente is None:
            return False
        elif regente == user:
            return True
        else:
            return False

    def is_user_especial(self, user: User):
        cargos = self.get_cargo_especial_list()
        if len(cargos) == 0:
            return False
        else:
            i = 0
            while i < len(cargos) and not cargos[i].ocupante == user:
                i = i + 1
            if i < len(cargos):
                return False
            else:
                return True

    def get_lider_list(self):
        return self.cargoturma_set.filter(cod_especial=1)

    def get_lider(self):
        if self.get_lider_list().exists():
            return self.get_lider_list()[0].ocupante
        else:
            return None

    def get_regente_list(self):
        return self.cargoturma_set.filter(cod_especial=5)

    def get_regente(self):
        if self.get_regente_list().exists():
            return self.get_regente_list()[0].ocupante
        else:
            return None

    def get_cargo_especial_list(self):
        return self.cargoturma_set.all()


class SeguidorManager(models.Model, ExportModelOperationsMixin('SeguidorManager')):
    link = models.URLField(null=True, blank=True)
    seguidores = models.ManyToManyField(User)

    def is_seguidor(self, user):
        return user in self.seguidores.all()

    def adicionar_seguidor(self, user):
        self.seguidores.add(user)
        self.save()

    def comunicar_todos(self, title, msg):
        for seguidor in self.seguidores:
            noti = Notificacao(seguidor, title, msg)
            if self.link:
                noti.link = self.link
            noti.save()


class CargoTurma(models.Model, ExportModelOperationsMixin('Cargos')):
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
        permissions = (('can_add_cargo', "Pode criar Cargo"),
                       ('can_edit_cargo', "Pode editar Cargo"),
                       ('can_delete_cargo', "Pode deletar Cargo"),
                       ('can_designar_cargo', "Pode designar alguem para o cargo"),)  # Não usado, depricated?

    def __str__(self):
        return f"Cargo {self.nome} da turma {self.turma.numero}"


class Professor(models.Model, ExportModelOperationsMixin('Professor')):
    user = models.OneToOneField(User, related_name='professor', on_delete=models.CASCADE)
    nome = models.CharField(max_length=70)

    def __str__(self):
        return self.nome

    class Meta:
        permissions = (('can_add_professor', 'Pode adicionar um novo Professor'),
                       ('can_edit_professor', 'Pode editar um professor'),
                       ('can_delete_professor', 'Pode deletar um professor'),)


class MateriaDaTurma(models.Model, ExportModelOperationsMixin('Materias')):
    nome = models.CharField(max_length=50)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    abreviacao = models.CharField(max_length=5)

    def __str__(self):
        return self.nome

    class Meta:
        permissions = (('can_add_materia', 'Pode adicionar uma novo Materia'),
                       ('can_edit_materia', 'Pode editar uma materia'),
                       ('can_delete_materia', 'Pode deletar uma materia'),)


class Aluno(models.Model, ExportModelOperationsMixin('Aluno')):
    chamada = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    nome = models.CharField(max_length=70)
    user = models.OneToOneField(User, related_name='aluno', on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    class Meta:
        permissions = (('edit_aluno', 'Pode editar um aluno.'),
                       ('can_delete_aluno', 'Pode deletar um aluno.'),)


class ProvaBase(models.Model):
    materia = models.ForeignKey(MateriaDaTurma, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)


class ProvaAplicada(models.Model):
    provaBase = models.ForeignKey(ProvaBase, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    nota = models.FloatField(null=True, blank=True)


class Horario(models.Model, ExportModelOperationsMixin('Horario')):
    turma = models.OneToOneField(Turma, related_name='horario', on_delete=models.CASCADE)

    def get_turno_aula_or_create(self, dia, turno_a):
        turno = TurnoAula.objects.filter(diaDaSemana=dia, turno=turno_a, turma=self.turma)
        if turno:
            return turno[0]
        else:
            turno = TurnoAula(turma=self.turma, horario=self, diaDaSemana=dia, turno=turno_a)
            turno.save()
            return turno

    def get_periodo_or_create(self, dia, turno: int, num):
        turno_aula = self.get_turno_ausla_or_create(dia, Turno.get_turno_by_cod(turno))
        per = turno_aula.periodo_set.filter(num=num)
        if per:
            return per[0]
        else:
            per = Periodo(turnoAula=turno_aula, num=num)
            per.save()
            return per

    permissions = (('editar_horario', 'Pode Editar o horario de qualquer turma.'),)


class Turno(models.Model, ExportModelOperationsMixin('Turno')):
    nome = models.CharField(max_length=30)
    cod = models.PositiveSmallIntegerField()
    horaInicio = models.TimeField()
    # 1
    s1 = models.TimeField()
    # 2
    s2 = models.TimeField()
    # 3
    s3 = models.TimeField()
    # intervalo
    s4 = models.TimeField()
    # 4
    s5 = models.TimeField()
    # 5
    horaFim = models.TimeField()

    def __str__(self):
        return self.nome

    def get_turno_by_cod(cod):
        return Turno.objects.filter(cod=cod)[0]


class TurnoAula(models.Model, ExportModelOperationsMixin('TurnoAula')):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    DIAS_DA_SEMANA = (
        (1, 'domingo'),
        (2, 'segunda-feira'),
        (3, 'terca-feira'),
        (4, 'quarta-feira'),
        (5, 'quinta-feira'),
        (6, 'sexta-feira'),
        (7, 'sabado'),
    )
    diaDaSemana = models.PositiveSmallIntegerField(choices=DIAS_DA_SEMANA)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)


class Periodo(models.Model, ExportModelOperationsMixin('Periodo')):
    num = models.PositiveSmallIntegerField()
    turnoAula = models.ForeignKey(TurnoAula, on_delete=models.CASCADE)
    materia = models.ForeignKey(MateriaDaTurma, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def dia(self):
        return self.turnoAula.diaDaSemana

    @property
    def turma(self):
        return self.turnoAula.turno.turma

    @property
    def turno_cod(self):
        return self.turnoAula.turno.cod


class Tarefa(models.Model, ExportModelOperationsMixin('Tarefa')):
    titulo = models.CharField(max_length=60)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    materia = models.ForeignKey(MateriaDaTurma, on_delete=models.CASCADE, null=True, blank=True)
    TIPOS = (
        (1, 'Tema'),
        (2, 'Trabalho'),
        (3, 'Pesquisa'),
        (4, 'Redação'),
    )
    tipo = models.PositiveSmallIntegerField(choices=TIPOS, blank=True, null=True)
    descricao = models.TextField()
    deadline = models.DateField(verbose_name='Data limite')
    manager_seguidor = models.OneToOneField(SeguidorManager, on_delete=models.DO_NOTHING, null=True, blank=True)

    def get_completacao(self, aluno: Aluno):
        completo = self.tarefacompletacao_set.filter(aluno=aluno)
        if len(completo) > 0:
            return completo[0]
        else:
            completo = TarefaCompletacao(tarefa=self, aluno=aluno)
            completo.save()
            return completo

    def get_seguidor_manager(self):
        if self.manager_seguidor:
            return self.manager_seguidor
        else:
            m = SeguidorManager(link=reverse('detalhes-tarefa', args=[self.pk, ]))
            m.save()
            self.manager_seguidor = m
            self.save()
            return self.manager_seguidor

    class Meta:
        permissions = (('can_add_tarefa', 'Pode adicionar uma nova tarefa.'),
                       ('can_edit_tarefa', 'Pode editar uma tarefa.'),
                       ('can_delete_tarefa', 'Pode deletar uma tarefa.'),)


class TarefaCompletacao(models.Model, ExportModelOperationsMixin('TarefaCompletação')):
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    completo = models.BooleanField(default=False)


class TarefaComentario(models.Model, ExportModelOperationsMixin('TarefaComentario')):
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    texto = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)


class Notificacao(models.Model, ExportModelOperationsMixin('Alerta')):
    """Notificação para os usuarios, campos obrigatorios: user, title, msg; Campos Livres: link"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visualizado = models.BooleanField(default=False)
    dataCriado = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=20)
    msg = models.TextField()
    link = models.URLField(blank=True, null=True)

# class Conteudo(models.Model):
#     materias = models.ManyToManyField(MateriaDaTurma)
#     nome = models.CharField(max_length=50)
#     serie = models.IntegerField() # 1 => 1 fundamente, 10=> 1º Medio, 20, 30
#     parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
#
# class CaixaBase(models.Model, ExportModelOperationsMixin('CaixaBase')):
#     objects = InheritanceManager()
#     nome = 'Classe Base'
#     pode_usar = False
#     min_w = 0
#     min_h = 0
#     max_h = 4
#     max_w = 3
#
#     config_url = ''
#
#     pos_x = models.IntegerField()
#     pos_y = models.IntegerField()
#
#     def return_html(self):
#         return 'Não implementado - Usando metodo da CaixaBase'
#
#
# # class ConteudosCaixa(CaixaBase):
# #     min_h = 2
# #     min_w = 1
# #     max_w = 2
# #     pode_usar = True
# #     nome = 'Box de Conteudos'
# #
# #     conteudos = models.ManyToManyField(Conteudo)
# #
# #     def return_html(self):
# #         return 'Ainda não implementado - Listará Conteudos'
#
# class TestCaixa(CaixaBase):
#     min_h = 2
#     min_w = 1
#     max_w = 2
#     pode_usar = True
#     nome = 'Box de Teste - Se você encontrar está entre em contato'
#
#     text = models.TextField()
#
#     def return_html(self):
#         return 'Box de Teste - Se você encontrar está entre em contato </br>' \
#                ''
