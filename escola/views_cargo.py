from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from escola.forms import CargoForm
from escola.models import Turma, CargoTurma
from escola.utils import dar_permissao_user


@permission_required('escola.can_add_cargo')
def add_cargo(request, turma_pk):
    if request.method == 'POST':

        # FORM TUTORIAL: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
        # Create a form instance and populate it with data from the request (binding):
        form = CargoForm(get_object_or_404(Turma, pk=turma_pk), request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            cargo = CargoTurma()
            cargo.nome = form.cleaned_data['nome']
            cargo.turma = get_object_or_404(Turma, pk=turma_pk)
            cargo.cod_especial = form.cleaned_data['cod_especial']
            cargo.ativo = form.cleaned_data['ativo']
            cargo.ocupante = form.cleaned_data['ocupante']
            cargo.save()

            dar_permissao_user(cargo.ocupante, cargo)

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('escola:list-cargos', args=[turma_pk]))

        # If this is a GET (or any other method) create the default form.
    else:
        proposed_ativo = True
        proposed_cod_especial = 0
        form = CargoForm(initial={'ativo': proposed_ativo, 'cod_especial': proposed_cod_especial},
                         turma=get_object_or_404(Turma, pk=turma_pk))

    context = {
        'form': form,
    }

    return render(request, 'escola/cargos/formCargos.html', context)


def list_cargos(request, pk_turma):
    turma = get_object_or_404(Turma, pk=pk_turma)
    cargos = CargoTurma.objects.filter(turma=turma)
    return render(request, 'escola/cargos/listCargos.html', context={'cargos': cargos, 'turma': turma})


@permission_required('escola.can_edit_cargo')
def edit_cargo(request, pk):
    cargo = get_object_or_404(CargoTurma, pk=pk)

    if request.method == 'POST':
        # FORM TUTORIAL: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
        # Create a form instance and populate it with data from the request (binding):
        form = CargoForm(cargo.turma, request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            cargo.nome = form.cleaned_data['nome']
            cargo.cod_especial = form.cleaned_data['cod_especial']
            cargo.ativo = form.cleaned_data['ativo']
            cargo.ocupante = form.cleaned_data['ocupante']
            cargo.save()

            dar_permissao_user(cargo.ocupante, cargo)

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('escola:list-cargos', args=[cargo.turma.pk]))

        # If this is a GET (or any other method) create the default form.
    else:
        form = CargoForm(initial={'nome': cargo.nome, 'turma': cargo.turma, 'ocupante': cargo.ocupante,
                                  'cod_especial': cargo.cod_especial, 'ativo': cargo.ativo}, turma=cargo.turma)

    context = {
        'form': form,
    }

    return render(request, 'escola/cargos/formCargos.html', context)


@permission_required('escola.can_delete_cargo')
def delete_cargo(request, pk):
    a = get_object_or_404(CargoTurma, pk=pk)
    turmapk = a.turma.pk
    a.delete()
    return HttpResponseRedirect(reverse('escola:list-cargos', args=[turmapk]))