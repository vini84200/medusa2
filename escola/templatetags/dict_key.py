from django.template.defaultfilters import register

from escola.models import Turno


@register.filter(name='dict_key')
def dict_key(d, k):
    '''Returns the given key from a dictionary.'''
    return d[k]


@register.filter(name='contain_key')
def contain_key(d, k):
    return k in d


@register.simple_tag
def get_p(turno, dia, p, ta):
    return ta[dia][turno.cod].periodo_set.filter(num=p)[0].materia


@register.simple_tag
def dia_teste(turno, dia, ta):
    return dia in ta and turno.cod in ta[dia]


@register.inclusion_tag('escola/horario/horario_include.html')
def mostra_horario_proprio(user):
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
               'user':user,
               'turma':aluno_turma}
    return context


@register.inclusion_tag('escola/horario/horario_include.html')
def mostra_horario(turma, user):
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
               'user':user,
               'turma':turma}
    return context
