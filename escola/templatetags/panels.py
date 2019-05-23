#  Developed by Vinicius José Fritzen
#  Last Modified 20/05/19 15:16.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import datetime

from django.template.defaultfilters import register

from escola.controller_provas_marcadas import get_materias_professor_for_day, get_provas_turma
from escola.models import Turno, Turma


@register.inclusion_tag('escola/horario/horario_include.html')
def panel_mostra_horario_proprio(user):
    aluno_turma = user.aluno.turma
    horario = aluno_turma.get_or_create_horario()
    ta = horario.get_horario()
    context = {'turnos': Turno.objects.all().order_by('cod'),
               'DIAS_DA_SEMANA': ['Domingo',
                                  'Segunda-feira',
                                  'Terça-feira',
                                  'Quarta-feira',
                                  'Quinta-feira',
                                  'Sexta-feira',
                                  'Sabado', ],
               'DIAS_DA_SEMANA_N': range(1, 8),
               'ta': ta,
               'turma_pk': aluno_turma.pk,
               'range': range(1, 6),
               'user': user,
               'turma': aluno_turma}
    return context


@register.inclusion_tag('escola/horario/horario_include.html')
def panel_mostra_horario(turma, user):
    horario = turma.get_or_create_horario()
    ta = horario.get_horario()
    context = {'turnos': Turno.objects.all().order_by('cod'),
               'DIAS_DA_SEMANA': ['Domingo',
                                  'Segunda-feira',
                                  'Terça-feira',
                                  'Quarta-feira',
                                  'Quinta-feira',
                                  'Sexta-feira',
                                  'Sabado', ],
               'DIAS_DA_SEMANA_N': range(1, 8),
               'ta': ta,
               'turma_pk': turma.pk,
               'range': range(1, 6),
               'user': user,
               'turma': turma}
    return context


@register.inclusion_tag('escola/panels/resumoHojeProfessor.html')
def panel_resumo_do_dia_prof(user):
    """O resumo diario para um professor"""
    professor = user.professor
    context = {}
    context.update({'turmashoje': get_materias_professor_for_day(professor, datetime.date.today())})
    return context


# Panel da lista de provas de uma turma
@register.inclusion_tag('escola/panels/listaProvasMarcadas.html')
def panel_lista_provas_marcadas_turma(turma: Turma):
    """Retorna uma lista de provas de uma turma em especifico"""
    context = {}
    provas = get_provas_turma(turma)
    context.update({'turma': turma})


# Panel do resumo diario dos alunos

# Lista de provas do aluno
# PS: Usar a função anterior já existente
