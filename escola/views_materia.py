from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from guardian.decorators import permission_required as permission_required_obj

from escola.decorators import is_user_escola
from escola.forms import MateriaForm
from escola.models import Turma, MateriaDaTurma
from escola.utils import dar_permissao_perm_a_user_of_level


@permission_required_obj('escola.can_add_materia', (Turma, 'pk', 'turma_pk'))
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
            dar_permissao_perm_a_user_of_level('can_edit_materia', 1, get_object_or_404(Turma, pk=turma_pk), materia)
            dar_permissao_perm_a_user_of_level('can_delete_materia', 2, get_object_or_404(Turma, pk=turma_pk), materia)
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


@permission_required_obj('escola.can_edit_materia', (MateriaDaTurma, 'pk', 'materia_pk'))
def edit_materia(request, turma_pk, materia_pk):
    materia = get_object_or_404(MateriaDaTurma, pk=materia_pk)
    if request.method == 'POST':
        form = MateriaForm(request.POST)
        if form.is_valid():
            materia.nome = form.cleaned_data['nome']
            materia.turma = get_object_or_404(Turma, pk=turma_pk)
            materia.professor = form.cleaned_data['professor']
            materia.abreviacao = form.cleaned_data['abreviacao']
            materia.save()
    else:

        form = MateriaForm(materia)

    context = {
        'form': form,
    }
    return render(request, 'escola/materia/formMateria.html', context=context)


@permission_required_obj('escola.can_delete_materia', (MateriaDaTurma, 'pk', 'materia_pk'))
def delete_materia(request, turma_pk, materia_pk):
    materia = get_object_or_404(MateriaDaTurma, pk=materia_pk)
    materia.delete()
    return HttpResponseRedirect(reverse('escola:list-materias', args=[turma_pk]))