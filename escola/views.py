import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404

from escola.models_horario import Horario, Turno, TurnoAula
from .decorators import *
from .forms import *
from .models import *

logger = logging.getLogger(__name__)


@is_user_escola
@login_required
def index(request):
    logger.info('views:index; user_id: %s', request.user.pk)
    context = {'request': request}
    if request.user.profile_escola.is_aluno:
        logger.info('views:index; user_id: %s é aluno.', request.user.pk)
        # HORARIO
        logger.warning("Lembre-se de retirar os horarios daqui e generalizar;")
        turma_pk = request.user.aluno.turma.pk
        logger.info('Preparando para tentar pegar horario...')
        try:
            horario = Horario.objects.get(turma__id=turma_pk)
            logger.info('O horario já existia, id=%s', horario.pk)
        except:
            logger.info("Criando horario novo...")
            horario = Horario(turma=request.user.aluno.turma)
            horario.save()
            logger.info('O novo horario possui id: %s', horario.pk)
        turnos = Turno.objects.all().order_by('cod')
        logger.info('Puxou %s turno(s) do banco de dados.', len(turnos))
        DIAS_DA_SEMANA = ['Domingo',
                          'Segunda-feira',
                          'Terça-feira',
                          'Quarta-feira',
                          'Quinta-feira',
                          'Sexta-feira',
                          'Sabado', ]
        DIAS_DA_SEMANA_N = range(1, 8)
        ta = {}
        logger.info('Preparando para entrar no loop de turnos...')
        for turno in turnos:
            logger.debug('Turno id:%s', turno.pk)
            for dia in DIAS_DA_SEMANA_N:
                a = TurnoAula.objects.filter(turno=turno, diaDaSemana=dia, horario=horario)
                if len(a) > 0:
                    if dia not in ta:
                        ta[dia] = dict()
                    ta[dia][turno.cod] = a[0]

        context.update({'turnos': turnos, 'DIAS_DA_SEMANA': DIAS_DA_SEMANA, 'DIAS_DA_SEMANA_N': DIAS_DA_SEMANA_N,
                        'ta': ta, 'turma_pk': turma_pk, 'range': range(1, 6)})
        # TAREFAS
        logger.warning("Lembre-se de retirar as tarefas daqui e generalizar;")
        tarefas = Tarefa.objects.filter(turma__pk=turma_pk, deadline__gte=datetime.date.today()).order_by('deadline')
        tarefas_c = []
        for tarefa in tarefas:
            tarefas_c.append((tarefa, tarefa.get_completacao(request.user.aluno)))
        context.update({'tarefas': tarefas_c, 'turma': get_object_or_404(Turma, pk=turma_pk)})

    logger.info('Antes de renderizar a view index, user: %s', request.user.pk)
    return render(request, 'escola/home.html', context=context)


@permission_required('escola.edit_aluno')
def edit_aluno():
    # TODO: Implement edit aluno
    raise NotImplementedError


@permission_required('escola.can_delete_aluno')
def delete_aluno(request, aluno_pk):
    aluno = get_object_or_404(Aluno, pk=aluno_pk)
    turma = aluno.turma
    aluno.delete()
    return HttpResponseRedirect(reverse('escola:list-alunos', args=[turma.pk]))


def sobre(request):
    return render(request, 'escola/sobre.html')


@is_user_escola
@login_required
def seguir_manager(request, pk):
    seguidor = SeguidorManager.objects.get(pk=pk)
    seguidor.adicionar_seguidor(request.user)
    return HttpResponseRedirect(request.GET.get('next', reverse('escola:index')))
