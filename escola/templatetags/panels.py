#  Developed by Vinicius José Fritzen
#  Last Modified 20/05/19 15:16.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import datetime
import logging
import random
import re

from django.shortcuts import get_object_or_404
from django.template.defaultfilters import register
from django.utils.safestring import mark_safe

from escola.controller_provas_marcadas import (get_materias_professor_for_day,
                                               get_provas_professor_futuras,
                                               get_provas_turma_futuras)
from escola.models import (LinkConteudo, Professor, Tarefa, Turma, Turno,
                           TurnoAula)
from escola.quotes.quotes_conf import QUOTES

logger = logging.getLogger(__name__)


@register.inclusion_tag('escola/horario/horario_include.html')
def panel_mostra_horario_proprio(user):
    logger.debug('panel_mostra_horario_proprio():')
    aluno_turma = user.aluno.turma
    horario = aluno_turma.get_or_create_horario()
    ta = horario.get_horario()
    context = {'turnos': Turno.objects.all().order_by('cod'),
               'DIAS_DA_SEMANA': [nome for num, nome in TurnoAula.DIAS_DA_SEMANA],
               'DIAS_DA_SEMANA_N': range(1, 8),
               'ta': ta,
               'turma_pk': aluno_turma.pk,
               'range': range(1, 6),
               'user': user,
               'turma': aluno_turma}
    logger.debug(context['DIAS_DA_SEMANA'])
    return context


@register.inclusion_tag('escola/horario/horario_include.html')
def panel_mostra_horario(turma, user):
    logger.debug('panel_mostra_horario():')
    horario = turma.get_or_create_horario()
    ta = horario.get_horario()
    context = {'turnos': Turno.objects.all().order_by('cod'),
               'DIAS_DA_SEMANA': [nome for num, nome in TurnoAula.DIAS_DA_SEMANA],
               'DIAS_DA_SEMANA_N': range(1, 8),
               'ta': ta,
               'turma_pk': turma.pk,
               'range': range(1, 6),
               'user': user,
               'turma': turma}
    logger.debug(context['DIAS_DA_SEMANA'])
    return context


@register.inclusion_tag('escola/panels/listaTarefas.html')
def panel_tarefas_aluno(user, qnt=0):
    """Esse painel mostra as tarefas do usuario, se a qnt for 0, mostra todas"""
    turma_pk = user.aluno.turma.pk
    logger.info('views:index; user_id: %s é aluno.', user.pk)
    tarefas = Tarefa.objects.filter(turma__pk=turma_pk, deadline__gte=datetime.date.today()).order_by('deadline')
    tarefas_c = []
    for tarefa in tarefas:
        tarefas_c.append((tarefa, tarefa.get_completacao(user.aluno)))
    logger.debug(f'Encontrei {len(tarefas_c)} tarefas.')
    return {'tarefas': tarefas_c, 'turma': get_object_or_404(Turma, pk=turma_pk)}


@register.inclusion_tag('escola/panels/resumoHojeProfessor.html')
def panel_resumo_do_dia_prof(user):
    """O resumo diario para um professor"""
    professor = user.professor
    context = {}
    context.update({'turmashoje': get_materias_professor_for_day(professor, datetime.date.today())})
    return context


# Panel da lista de provas de uma turma
@register.inclusion_tag('escola/panels/listaProvasMarcadas.html')
def panel_lista_provas_marcadas_turma(turma: Turma, qnt=0):
    """Retorna uma lista de provas de uma turma em especifico"""
    context = {}
    provas = get_provas_turma_futuras(turma, qnt)
    context.update({'turma': turma, 'provas': provas})
    return context


# panel_lista_provas_marcadas_professor
@register.inclusion_tag('escola/panels/listaProvasMarcadas.html')
def panel_lista_provas_marcadas_professor(professor: Professor, qnt=0):
    """Retorna uma lista de provas de uma turma em especifico"""
    context = {}
    provas = get_provas_professor_futuras(professor, qnt)
    context.update({'professor': professor, 'provas': provas})
    return context

# Panel do resumo diario dos alunos

# Lista de provas do aluno
# PS: Usar a função anterior já existente

# Painel de uma citação
@register.inclusion_tag('escola/panels/panelQuote.html')
def panel_quote():
    """Mostra uma citação aleatoria selecionada do arquivo de citações."""
    context = {}
    citacao, autor = random.choice(QUOTES)
    context.update({'quote': mark_safe(citacao), 'autor': autor})
    return context


@register.inclusion_tag('escola/panels/panelQuote.html')
def panel_quote_esp(id: int):
    """Mostra uma citação aleatoria selecionada do arquivo de citações."""
    context = {}
    citacao, autor = QUOTES[id]
    context.update({'quote': mark_safe(citacao), 'autor': autor})
    return context


@register.inclusion_tag('escola/panels/panelQuotesList.html')
def panel_all_quotes():
    """Mostra uma citação aleatoria selecionada do arquivo de citações."""
    context = {}
    ids = []
    for quote in QUOTES:
        ids.append(QUOTES.index(quote))
    context.update({'quotes_ids': ids})
    return context


@register.inclusion_tag('escola/panels/link_conteudo.html')
def link_conteudo(conteudo_link: LinkConteudo):
    """Mostra um link com conteudo"""
    url = conteudo_link.link
    conteudo = {'link': conteudo_link}
    # Verificação YouTube
    regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')

    match = regex.match(url)

    if match:
        conteudo.update({'youtube': True,
                         'default': False,
                         'y_id': match.group('id')})
        return conteudo

    # Default
    conteudo.update({'youtube': False, 'default': True, })
    return conteudo
