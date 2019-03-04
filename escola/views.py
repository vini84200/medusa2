import datetime

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseForbidden
from django.template import loader
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from .models import *
from .forms import *
from .decorators import *


@login_required
@is_user_escola
def index(request):
    return render(request, 'escola/home.html', context={'request': request})


@staff_member_required
def add_turma(request):
    if request.method == 'POST':

        #FORM TUTORIAL: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
        # Create a form instance and populate it with data from the request (binding):
        form = CriarTurmaForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            t = Turma()
            t.numero = form.cleaned_data['numero']
            t.ano = form.cleaned_data['ano']
            t.save()

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


def list_turmas(request):
    return None