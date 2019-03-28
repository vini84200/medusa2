import datetime

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.mail import mail_managers
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from guardian.decorators import permission_required as permission_required_obj

from escola.decorators import is_user_escola
from escola.forms import AlunoCreateFormOutLabel, AlunoCreateForm
from escola.models import Profile, Aluno, Turma
from escola.utils import genarate_password, generate_username


@permission_required('escola.can_populate_turma')
def populate_alunos(request):
    AlunosFormSet = formset_factory(AlunoCreateFormOutLabel, extra=35, max_num=40)
    formset = AlunosFormSet(data=request.POST or None)
    if request.method == "POST":
        usuarios = []
        if formset.is_valid():
            for form in formset:
                # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
                if 'nome' in form.cleaned_data:
                    senha, username = generate_aluno(form)
                    usuarios.append((username, senha))
            response = render(request, 'escola/alunos/alunosList.html', context={'usuarios': usuarios})
            mail_managers("Lista de Senhas para uma nova popuação de usarios, imprima", response.content)
            return response

    context = {
        'formset': formset
    }
    return render(request, 'escola/alunos/formPopulateAlunos.html', context)


def generate_aluno(form):
    nome: str = form.cleaned_data['nome']
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
    profile = Profile(user=user, is_aluno=True, is_professor=False)
    profile.save()
    aluno = Aluno()
    aluno.chamada = form.cleaned_data['num_chamada']
    aluno.nome = nome
    aluno.user = user
    turma = get_object_or_404(Turma, numero=form.cleaned_data['turma'], ano=datetime.date.today().year)
    aluno.turma = turma
    aluno.save()
    return senha, username


@permission_required_obj('escola.can_add_aluno', (Turma, 'pk', 'turma_pk'))
def add_aluno(request, turma_pk):
    if request.method == 'POST':
        # FORM TUTORIAL: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
        # Create a form instance and populate it with data from the request (binding):
        form = AlunoCreateForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            turma = get_object_or_404(Turma, numero=form.cleaned_data['turma'], ano=datetime.date.today().year)
            if request.user.has_perm('escola.can_add_aluno',turma):
                senha, username = generate_aluno(form)
                # redirect to a new URL:
                if form.cleaned_data['senha']:
                    return HttpResponseRedirect(reverse('escola:list-alunos', args=[turma.pk]))
                else:
                    return render(request, 'escola/alunos/alunosList.html',
                                  context={'usuarios': [(username, senha,), ]})
            else:
                raise PermissionDenied

        # If this is a GET (or any other method) create the default form.
    else:
        proposed_turma = get_object_or_404(Turma, pk=turma_pk).numero
        form = AlunoCreateForm(initial={'turma': proposed_turma})

    context = {
        'form': form,
    }

    return render(request, 'escola/alunos/formAlunosCreate.html', context)


@is_user_escola
def list_alunos(request, turma_pk):
    turma = get_object_or_404(Turma, pk=turma_pk)
    alunos = Aluno.objects.filter(turma=turma).order_by('chamada')
    return render(request, 'escola/alunos/listAlunosPerTurma.html', context={'alunos': alunos, 'turma': turma})