#  Developed by Vinicius José Fritzen
#  Last Modified 25/04/19 23:11.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from rolepermissions.checkers import has_object_permission

from escola.forms import TarefaForm, ComentarioTarefaForm
from escola.models import Turma, Tarefa, TarefaComentario


def add_tarefa(request, turma_pk):
    turma = get_object_or_404(Turma, pk=turma_pk)
    if not has_object_permission('add_tarefa', request.user, turma):
        return redirect_to_login(request.get_full_path())
    if request.method == 'POST':
        form = TarefaForm(turma, request.POST)
        if form.is_valid():
            t = Tarefa.create(
                form.cleaned_data['titulo'],
                turma,
                form.cleaned_data['materia'],
                form.cleaned_data['tipo'],
                form.cleaned_data['descricao'],
                form.cleaned_data['deadline']
            )
            seg = t.get_seguidor_manager()
            seg.adicionar_seguidor(request.user)
            seg.adicionar_seguidor(t.materia.professor.user)
            return HttpResponseRedirect(reverse('escola:list-materias', args=[turma_pk]))
    else:
        form = TarefaForm(turma=turma)

    context = {
        'form': form,
    }
    return render(request, 'escola/tarefas/formTarefa.html', context=context)


@login_required
def list_tarefa(request, turma_pk):
    tarefas = Tarefa.objects.filter(turma__pk=turma_pk)
    if request.user.is_authenticated and request.user.profile_escola.is_aluno:
        tarefas_c = []
        for tarefa in tarefas:
            tarefas_c.append((tarefa, tarefa.get_completacao(request.user.aluno)))
        return render(request, 'escola/tarefas/listTarefasParaAluno.html',
                      context={'tarefas': tarefas_c, 'turma': get_object_or_404(Turma, pk=turma_pk)})
    else:
        return render(request, 'escola/tarefas/listTarefas.html', context={'tarefas': tarefas, 'turma': get_object_or_404(Turma, pk=turma_pk)})


def edit_tarefa(request, tarefa_pk):
    tarefa = get_object_or_404(Tarefa, pk=tarefa_pk)
    turma = tarefa.turma
    if not has_object_permission('edit_tarefa', request.user, tarefa):
        return redirect_to_login(request.get_full_path())
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


def delete_tarefa(request, tarefa_pk):
    tarefa = get_object_or_404(Tarefa, pk=tarefa_pk)
    if not has_object_permission('delete_tarefa', request.user, tarefa):
        return redirect_to_login(request.get_full_path())
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