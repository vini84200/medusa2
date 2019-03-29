from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from guardian.decorators import permission_required as permission_required_obj

from escola.forms import TarefaForm, ComentarioTarefaForm
from escola.models import Turma, Tarefa, TarefaComentario
from escola.utils import dar_permissao_perm_a_user_of_level


@permission_required_obj('escola.can_add_tarefa', (Turma, 'pk', 'turma_pk'))
def add_tarefa(request, turma_pk):
    # FIXME Adicionar permissões, a lista de permissões do grupo LIDER, VICELIDER e REGENTE da turma;
    turma = get_object_or_404(Turma, pk=turma_pk)
    if request.method == 'POST':
        form = TarefaForm(turma, request.POST)
        if form.is_valid():
            tarefa = Tarefa()
            tarefa.titulo = form.cleaned_data['titulo']
            tarefa.turma = turma
            tarefa.materia = form.cleaned_data['materia']
            tarefa.tipo = form.cleaned_data['tipo']
            tarefa.descricao = form.cleaned_data['descricao']
            tarefa.deadline = form.cleaned_data['deadline']
            tarefa.save()
            seg = tarefa.get_seguidor_manager()
            seg.adicionar_seguidor(request.user)
            seg.adicionar_seguidor(tarefa.materia.professor.user)

            dar_permissao_perm_a_user_of_level('can_edit_tarefa', 1, turma, tarefa)
            dar_permissao_perm_a_user_of_level('can_delete_tarefa', 2, turma, tarefa)

            return HttpResponseRedirect(reverse('escola:list-materias', args=[turma_pk]))
    else:
        form = TarefaForm(turma=turma)

    context = {
        'form': form,
    }
    return render(request, 'escola/tarefas/formTarefa.html', context=context)


def list_tarefa(request, turma_pk):
    tarefas = Tarefa.objects.filter(turma__pk=turma_pk)
    if request.user.profile_escola.is_aluno:
        tarefas_c = []
        for tarefa in tarefas:
            tarefas_c.append((tarefa, tarefa.get_completacao(request.user.aluno)))
        return render(request, 'escola/tarefas/listTarefasParaAluno.html',
                      context={'tarefas': tarefas_c, 'turma': get_object_or_404(Turma, pk=turma_pk)})
    else:
        return render(request, 'escola/tarefas/listTarefas.html', context={'tarefas': tarefas})


@permission_required_obj('escola.can_edit_tarefa', (Tarefa, 'pk', 'tarefa_pk'))
def edit_tarefa(request, tarefa_pk):
    tarefa = get_object_or_404(Tarefa, pk=tarefa_pk)
    turma = tarefa.turma
    if request.method == 'POST':
        form = TarefaForm(turma, request.POST)
        if form.is_valid():
            tarefa.titulo = form.cleaned_data['titulo']
            tarefa.turma = turma
            tarefa.materia = form.cleaned_data['materia']
            tarefa.tipo = form.cleaned_data['tipo']
            tarefa.descricao = form.cleaned_data['descricao']
            tarefa.deadline = form.cleaned_data['deadline']
            tarefa.save()
            return HttpResponseRedirect(reverse('escola:list-tarefa', args=[turma.pk]))
    else:
        form = TarefaForm(turma=turma, initial={'titulo': tarefa.titulo, 'materia': tarefa.materia, 'tipo': tarefa.tipo,
                                                'descricao': tarefa.descricao, 'deadline': tarefa.deadline})

    context = {
        'form': form,
    }
    return render(request, 'escola/tarefas/formTarefa.html', context=context)


@permission_required_obj('escola.can_delete_tarefa', (Tarefa, 'pk', 'tarefa_pk'))
def delete_tarefa(request, tarefa_pk):
    tarefa = get_object_or_404(Tarefa, pk=tarefa_pk)
    tarefa.delete()
    return HttpResponseRedirect(reverse('escola:index'))


@login_required
def concluir_tarefa(request, tarefa_pk):
    tarefa: Tarefa = get_object_or_404(Tarefa, pk=tarefa_pk)
    conclusao = tarefa.get_completacao(request.user.aluno)
    conclusao.completo = not conclusao.completo
    conclusao.save()
    return HttpResponseRedirect(reverse('escola:index'))


@login_required
def detalhes_tarefa(request, tarefa_pk):
    tarefa = get_object_or_404(Tarefa, pk=tarefa_pk)
    turma = tarefa.turma
    comentarios = TarefaComentario.objects.filter(tarefa=tarefa).order_by('-created_on')
    completacao = None
    if request.user.profile_escola.is_aluno:
        completacao = tarefa.get_completacao(request.user.aluno)
    if request.method == 'POST':
        form = ComentarioTarefaForm(request.POST)
        if form.is_valid():
            comentario = TarefaComentario()
            comentario.tarefa = tarefa
            comentario.user = request.user
            comentario.texto = form.cleaned_data['texto']
            comentario.save()
            # Cria notificação para o professor
            # TODO: Criar botão de seguir, e adicionar as notificações aqui
            # notificacao_professor = Notificacao(user=tarefa.materia.professor.user,
            #                                     title=f"Novo Comentario na tarefa {tarefa.titulo}, "
            #                                     f"{turma}", msg=f"{comentario.user.username.title()} comentou na "
            #     f"tarefa {tarefa.titulo}: \n"
            #     f"  {comentario.texto}",
            #                                     link=reverse('escola:detalhes-tarefa', args=[tarefa_pk]))
            # notificacao_professor.save()
            tarefa.get_seguidor_manager().comunicar_todos(title=f"Novo Comentario na tarefa {tarefa.titulo}, "
            f"{turma}", msg=f"{comentario.user.username.title()} comentou na "
            f"tarefa {tarefa.titulo}: \n"
            f"  {comentario.texto}")
            return HttpResponseRedirect(reverse('escola:detalhes-tarefa', args=[tarefa_pk]))
    else:
        form = ComentarioTarefaForm()

    context = {
        'form': form,
        'tarefa': tarefa,
        'comentarios': comentarios,
        'completacao': completacao,
    }
    return render(request, 'escola/tarefas/detalhesTarefa.html', context=context)