#  Developed by Vinicius José Fritzen
#  Last Modified 25/04/19 17:02.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

import datetime

from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from rolepermissions.decorators import has_permission_decorator

from escola.decorators import is_user_escola
from escola.forms import CriarTurmaForm
from escola.models import Turma, Horario


@has_permission_decorator('add_turma', redirect_to_login=True)
def add_turma(request):
    if request.method == 'POST':

        # FORM TUTORIAL: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
        # Create a form instance and populate it with data from the request (binding):
        form = CriarTurmaForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            t = Turma()
            t.numero = form.cleaned_data['numero']
            t.ano = form.cleaned_data['ano']
            t.save()
            hor = Horario(turma=t)
            hor.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('escola:list-turmas'))

        # If this is a GET (or any other method) create the default form.
    else:
        proposed_ano = datetime.date.today().year
        form = CriarTurmaForm(initial={'ano': proposed_ano})

    context = {
        'form': form,
    }

    return render(request, 'escola/turma/criarForm.html', context)


@is_user_escola
def list_turmas(request):
    turmas = Turma.objects.all()
    return render(request, 'escola/turma/listaTurmas.html', context={'turmas': turmas})


@permission_required('escola.can_edit_turma')
def edit_turma(request, pk):
    turma: Turma = get_object_or_404(Turma, pk=pk)

    if request.method == 'POST':

        # FORM TUTORIAL: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
        # Create a form instance and populate it with data from the request (binding):
        form = CriarTurmaForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            turma.numero = form.cleaned_data['numero']
            turma.ano = form.cleaned_data['ano']
            turma.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('escola:list-turmas'))

        # If this is a GET (or any other method) create the default form.
    else:
        form = CriarTurmaForm(initial={'numero': turma.numero, 'ano': turma.ano})
    context = {
        'form': form,
    }

    return render(request, 'escola/turma/criarForm.html', context)


@permission_required('escola.can_delete_turma')
def delete_turma(request, pk):
    # TODO: Add confirmation message.
    turma_instace: Turma = get_object_or_404(Turma, pk=pk)
    turma_instace.delete()
    return HttpResponseRedirect(reverse('escola:list-turmas'))