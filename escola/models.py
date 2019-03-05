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

    def __str__(self):
        return f"Turma {self.numero}"


class CargoTurma(models.Model):
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
                       ('can_designar_cargo', "Pode designar alguem para o cargo"),)

    def __str__(self):
        return f"Cargo {self.nome} da turma {self.turma.numero}"


class Professor(models.Model):
    user = models.OneToOneField(User, related_name='professor', on_delete=models.CASCADE)
    nome = models.CharField(max_length=70)

    def __str__(self):
        return self.nome


class MateriaDaTurma(models.Model):
    nome = models.CharField(max_length=50)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    abreviacao = models.CharField(max_length=5)

    def __str__(self):
        return self.nome


class Aluno(models.Model):
    chamada = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    nome = models.CharField(max_length=70)
    user = models.OneToOneField(User, related_name='aluno', on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class ProvaBase(models.Model):
    materia = models.ForeignKey(MateriaDaTurma, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)


class ProvaAplicada(models.Model):
    provaBase = models.ForeignKey(ProvaBase, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    nota = models.FloatField(null=True, blank=True)


class Horario(models.Model):
    turma = models.OneToOneField(Turma, related_name='horario', on_delete=models.CASCADE)

    def get_turno_aula_or_create(self, dia, turno_a):
        turno = TurnoAula.objects.filter(diaDaSemana=dia, turno=turno_a, turma=self.turma)
        if turno:
            return turno[0]
        else:
            turno = TurnoAula(turma = self.turma, horario = self, diaDaSemana=dia, turno= turno_a)
            turno.save()
            return turno

    def get_periodo_or_create(self, dia, turno:int, num):
        turno_aula = self.get_turno_aula_or_create(dia, Turno.get_turno_by_cod(turno))
        per = turno_aula.periodo_set.filter(num=num)
        if per:
            return per[0]
        else:
            per = Periodo(turnoAula=turno_aula, num=num)
            per.save()
            return per


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

    def __str__(self):
        return self.nome

    def get_turno_by_cod(cod):
        return Turno.objects.filter(cod = cod)[0]


class TurnoAula(models.Model):
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


class Periodo(models.Model):
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
