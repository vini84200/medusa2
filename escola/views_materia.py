#  Developed by Vinicius José Fritzen
#  Last Modified 25/04/19 13:41.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import DetailView

from escola.decorators import is_user_escola
from escola.forms import MateriaForm
from escola.models import Turma, MateriaDaTurma


# FIXME: 25/04/2019 por wwwvi: Adicionar permissões
def add_materia(request, turma_pk):
    # FIXME Adicionar permissões, a lista de permissões do grupo LIDER, VICELIDER e REGENTE da turma;
    if request.method == 'POST':
        form = MateriaForm(request.POST)
        if form.is_valid():
            materia = MateriaDaTurma()
            materia.nome = form.cleaned_data['nome']
            materia.turma = get_object_or_404(Turma, pk=turma_pk)
            materia.professor = form.cleaned_data['professor']
            materia.abreviacao = form.cleaned_data['abreviacao']
            materia.save()
            # TODO: 25/04/2019 por wwwvi: Dar permissão ao criador ou algo parecido.
            return HttpResponseRedirect(reverse('escola:list-materias', args=[turma_pk]))
    else:
        form = MateriaForm()

    context = {
        'form': form,
    }
    return render(request, 'escola/materia/formMateria.html', context=context)


@is_user_escola
def list_materias(request, turma_pk):
    turma = get_object_or_404(Turma, pk=turma_pk)
    materias = MateriaDaTurma.objects.filter(turma=turma)
    return render(request, 'escola/materia/listMaterias.html', context={'materias': materias, 'turma': turma})


# FIXME: 25/04/2019 por wwwvi: Adicionar requerimento de permissão
def edit_materia(request, materia_pk):
    materia = get_object_or_404(MateriaDaTurma, pk=materia_pk)
    turma = materia.turma
    if request.method == 'POST':
        form = MateriaForm(request.POST)
        if form.is_valid():
            materia.nome = form.cleaned_data['nome']
            materia.turma = turma
            materia.professor = form.cleaned_data['professor']
            materia.abreviacao = form.cleaned_data['abreviacao']
            materia.save()
    else:

        form = MateriaForm(instance=materia)

    context = {
        'form': form,
    }
    return render(request, 'escola/materia/formMateria.html', context=context)


# FIXME: 25/04/2019 por wwwvi: Adicionar Permissão
def delete_materia(request, materia_pk):
    materia = get_object_or_404(MateriaDaTurma, pk=materia_pk)
    turma = materia.turma
    materia.delete()
    return HttpResponseRedirect(reverse('escola:list-materias', args=[turma.pk]))


# FIXME: 25/04/2019 por wwwvi: Adicionar Permissão
class MateriaDaTurmaDetailView(LoginRequiredMixin, DetailView):
    """View de detalhes sobre a materia"""
    model = MateriaDaTurma
    context_object_name = 'materia'
