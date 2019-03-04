from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile_escola', on_delete=models.CASCADE)
    is_aluno = models.BooleanField('student status', default=False)
    is_professor = models.BooleanField('teacher status', default=False)

    def __str__(self):
        return f"Profile de {self.user.__str__()}"


class Turma(models.Model):
    numero = models.IntegerField()
    ano = models.IntegerField()

    class Meta:
        permissions = (('can_add_turma', "Pode criar turmas"),
                       ('can_edit_turma', "Pode editar turmas"),
                       ('can_delete_turma', "Pode deletar turmas"),
                       ('can_populate_turma', "Pode popular turmas"),)


class Professor(models.Model):
    user = models.OneToOneField(User, related_name='professor', on_delete=models.CASCADE)


class MateriaDaTurma(models.Model):
    nome = models.CharField(max_length=50)
    professor = models.ForeignKey(Professor, on_delete=models.DO_NOTHING)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)


class Aluno(models.Model):
    chamada = models.PositiveSmallIntegerField()
    nome = models.CharField(max_length=70)
    user = models.OneToOneField(User, related_name='aluno', on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.DO_NOTHING)
    is_lider = models.BooleanField(default=False)

class ProvaBase(models.Model):
    materia = models.ForeignKey(MateriaDaTurma, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)


class ProvaAplicada(models.Model):
    provaBase = models.ForeignKey(ProvaBase, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    nota = models.FloatField(null=True, blank=True)


class Horario(models.Model):
    turma = models.OneToOneField(Turma, related_name='horario', on_delete=models.CASCADE)


class Turno(models.Model):
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


class TurnoAula(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    DIAS_DA_SEMANA = (
        (1, 'sabado'),
        (2, 'segunda-feira'),
        (3, 'terca-feira'),
        (4, 'quarta-feira'),
        (5, 'quinta-feira'),
        (6, 'sexta-feira'),
        (7, 'sabado'),
    )
    diaDaSemana = models.PositiveSmallIntegerField(choices=DIAS_DA_SEMANA)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)


class Periodo(models.Model):
    turnoAula = models.ForeignKey(TurnoAula, on_delete=models.CASCADE)
    materia = models.ForeignKey(MateriaDaTurma, on_delete=models.CASCADE)
