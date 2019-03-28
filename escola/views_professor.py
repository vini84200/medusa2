from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from escola.decorators import is_user_escola
from escola.forms import ProfessorCreateForm
from escola.models import Profile, Professor
from escola.utils import username_present, generate_username, genarate_password


@permission_required('escola.can_add_professor')
def add_professor(request):
    if request.method == 'POST':

        # FORM TUTORIAL: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
        # Create a form instance and populate it with data from the request (binding):
        form = ProfessorCreateForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            senha, username = create_professor(form)
            # redirect to a new URL:
            if form.cleaned_data['senha']:
                return HttpResponseRedirect(reverse('list-professores'))
            else:
                return render(request, 'escola/alunos/alunosList.html', context={'usuarios': [(username, senha,), ]})

        # If this is a GET (or any other method) create the default form.
    else:
        form = ProfessorCreateForm()

    context = {
        'form': form,
    }

    return render(request, 'escola/professor/formProfessorCreate.html', context)


def create_professor(form):
    # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
    nome = form.cleaned_data['nome']
    username = form.cleaned_data['username']
    # Gera username a partir do Nome
    if not username:
        username = generate_username(nome)
    senha = form.cleaned_data['senha']
    if not senha:
        senha = genarate_password()
    user = User.objects.create_user(username, password=senha)
    user.first_name = nome.split(" ")[0]
    user.last_name = nome.split(" ")[-1]
    user.save()
    profile = Profile(user=user, is_aluno=False, is_professor=True)
    profile.save()
    professor = Professor()
    professor.user = user
    professor.nome = nome
    professor.save()
    return senha, username


@is_user_escola
def list_professores(request):
    professores = Professor.objects.all()
    return render(request, 'escola/professor/listProfessores.html', context={'professores': professores})


@permission_required("escola.can_edit_professor")
def edit_professor():
    # TODO Implement edit professor
    raise NotImplementedError


@permission_required('escola.can_delete_professor')
def delete_professor(request, pk):
    prof = get_object_or_404(Professor, pk=pk)
    prof.delete()
    return HttpResponseRedirect(reverse('escola:list-professores'))