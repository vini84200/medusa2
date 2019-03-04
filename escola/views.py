import datetime

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseForbidden
from django.template import loader
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.base_user import BaseUserManager
from .models import *
from .forms import *
from .decorators import *


#   HELPERS
def username_present(username):
    if User.objects.filter(username=username).exists():
        return True

    return False


#   VIEWS:


@login_required
@is_user_escola
def index(request):
    return render(request, 'escola/home.html', context={'request': request})


@permission_required('escola.can_add_turma')
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
            hor = Horario(turma = t)
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


@permission_required('escola.can_populate_turma')
def populate_turma(request, pk):
    return None


@permission_required('escola.can_add_cargo')
def add_cargo(request, pk_turma):
    if request.method == 'POST':

        # FORM TUTORIAL: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
        # Create a form instance and populate it with data from the request (binding):
        form = CargoForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            cargo = CargoTurma()
            cargo.nome = form.cleaned_data['nome']
            cargo.turma = get_object_or_404(Turma, pk=pk_turma)
            cargo.cod_especial = form.cleaned_data['cod_especial']
            cargo.ativo = form.cleaned_data['ativo']
            cargo.ocupante = form.cleaned_data['ocupante']
            cargo.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('escola:list-cargos', args=[pk_turma]))

        # If this is a GET (or any other method) create the default form.
    else:
        proposed_ativo = True
        proposed_cod_especial = 0
        form = CargoForm(initial={'ativo': proposed_ativo, 'cod_especial': proposed_cod_especial})

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
        form = CargoForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            cargo.nome = form.cleaned_data['nome']
            cargo.cod_especial = form.cleaned_data['cod_especial']
            cargo.ativo = form.cleaned_data['ativo']
            cargo.ocupante = form.cleaned_data['ocupante']
            cargo.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('escola:list-cargos', args=[cargo.turma]))

        # If this is a GET (or any other method) create the default form.
    else:
        form = CargoForm(initial={'nome': cargo.nome, 'turma': cargo.turma, 'ocupante': cargo.ocupante,
                                  'cod_especial': cargo.cod_especial, 'ativo': cargo.ativo})

    context = {
        'form': form,
    }

    return render(request, 'escola/cargos/formCargos.html', context)


@permission_required('escola.can_edit_cargo')
def delete_cargo(request, pk):
    a = get_object_or_404(CargoTurma, pk=pk)
    turmapk = a.turma.pk
    a.delete()
    return HttpResponseRedirect(reverse('escola:list-cargos', args=[turmapk]))


@permission_required('escola.can_add_cargo')
def add_aluno(request, pk_turma):
    if request.method == 'POST':

        # FORM TUTORIAL: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
        # Create a form instance and populate it with data from the request (binding):
        form = AlunoCreateForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            nome: str = form.cleaned_data['nome']
            username = form.cleaned_data['username']
            # Gera username a partir do Nome
            if not username:
                # Cria a base do username a partir do primeiro nome
                username = nome.split(' ')[0].lower() + "."
                # Adiciona as iniciais depois do ponto
                for n in nome.split(' '):
                    if n[0]:
                        username += n[0].lower()

                # Verifica se já foi usado, caso positivo, vai adicionando numeros até o certo
                a = 0
                usernameTeste = username
                while username_present(usernameTeste):
                    a = + 1
                    usernameTeste = username + a.__str__()
                username = usernameTeste

            senha = form.cleaned_data['senha']
            # Verifica se uma senha foi especificada.
            # Caso não, gera uma.
            if not senha:
                senha = BaseUserManager().make_random_password(length=8,
                                                               allowed_chars='abcdefghjkmnpqrstuvwxyz23456789')

            user = User.objects.create_user(username, password=senha)
            user.first_name = nome.split(" ")[0]
            user.last_name = nome.split(" ")[-1]
            user.save()
            profile = Profile(user=user, is_aluno=True, is_professor=False)
            profile.save()
            aluno = Aluno()
            aluno.chamada = form.cleaned_data['num_chamada']
            aluno.nome = nome
            aluno.user = user
            turma = get_object_or_404(Turma, numero=form.cleaned_data['turma'], ano=datetime.date.today().year)
            aluno.turma = turma
            aluno.save()
            # redirect to a new URL:
            if form.cleaned_data['senha']:
                return HttpResponseRedirect(reverse('list-alunos', args=[turma.pk]))
            else:
                return HttpResponse(f"OK! Usuario criado. Username:{username} e senha:{senha} <br/> "
                                    f"Quando logar, lebrar de alterar a senha.")

        # If this is a GET (or any other method) create the default form.
    else:
        proposed_turma = get_object_or_404(Turma, pk=pk_turma).numero
        form = AlunoCreateForm(initial={'turma': proposed_turma})

    context = {
        'form': form,
    }

    return render(request, 'escola/alunos/formAlunosCreate.html', context)


def list_alunos(request, turma_pk):
    turma = get_object_or_404(Turma, pk=turma_pk)
    alunos = Aluno.objects.filter(turma=turma)
    return render(request, 'escola/alunos/listAlunosPerTurma.html', context={'alunos': alunos, 'turma': turma})
