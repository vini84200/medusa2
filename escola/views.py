import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, TemplateView

from escola.models import Horario, Turno, TurnoAula
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
        turma_pk = request.user.aluno.turma.pk
        logger.info('views:index; user_id: %s é aluno.', request.user.pk)
        # TAREFAS
        logger.info("Lembre-se de retirar as tarefas daqui e generalizar;")
        tarefas = Tarefa.objects.filter(turma__pk=turma_pk, deadline__gte=datetime.date.today()).order_by('deadline')
        tarefas_c = []
        for tarefa in tarefas:
            tarefas_c.append((tarefa, tarefa.get_completacao(request.user.aluno)))
        logger.debug(f'Encontrei {len(tarefas_c)} tarefas.')
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


class SobreView(TemplateView):
    template_name = "escola/sobre.html"




@is_user_escola
@login_required
def seguir_manager(request, pk):
    seguidor = SeguidorManager.objects.get(pk=pk)
    seguidor.adicionar_seguidor(request.user)
    return HttpResponseRedirect(request.GET.get('next', reverse('escola:index')))


class NotificacaoListView(LoginRequiredMixin, ListView):
    model = Notificacao
    template_name = "escola/notificacoes_list.html"
    context_object_name = 'notificacoes'

    def get_queryset(self):
        query = Notificacao.objects.filter(user=self.request.user).order_by('-dataCriado')
        self.request.user.profile_escola.read_all_notifications()
        return query



