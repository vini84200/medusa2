#  Developed by Vinicius José Fritzen
#  Last Modified 20/04/19 09:00.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

import datetime
import logging

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import RequestContext
from django.views.generic import ListView, TemplateView

from escola.models import (Horario, Notificacao, Notificador, Turma, Turno,
                           TurnoAula)

from .decorators import *
from .forms import *
from .models import *

logger = logging.getLogger(__name__)


@is_user_escola
@login_required
def index(request):
    logger.info('views:index; user_id: %s', request.user.pk)
    context = {'request': request}

    logger.info('Antes de renderizar a view index, user: %s', request.user.pk)

    if request.user.profile_escola.is_aluno:
        logger.info('É um aluno renderizando tela do aluno')
        context.update({'turma': request.user.aluno.turma})
        return render(request, 'escola/home_aluno.html', context=context)

    if request.user.profile_escola.is_professor:
        logger.info('É um professor renderizando tela do professor')
        return render(request, 'escola/home_professor.html', context=context)
    logger.warning('O usuario não é nem professor nem aluno, renderizando a tela default')
    return render(request, 'escola/home_base.html', context=context)


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
    seguidor = Notificador.objects.get(pk=pk)
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


def handler404(request, exception, template_name="404.html"):
    response = render_to_response('404.html')
    response.status_code = 404
    return response


def handler500(request, template_name="500.html"):
    response = render_to_response('500.html', {'request': request})
    response.status_code = 500
    return response


def base_layout(request):
    template = 'escola/base.html'
    return render(request, template)


# class UserListView(ListView):
#     model = User
#     context_object_name = 'users'
#     template_name = 'listUser.html'


def atualisar_emails(request):
    Turma.atualizaProvas()
    Turma.atualizaTarefas()
    count = Notificacao.send_all_emails()
    return JsonResponse({'success': True, 'emails_sended': count})
