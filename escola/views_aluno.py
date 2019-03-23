import datetime

from django.contrib.auth.base_user import BaseUserManager
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
from escola.utils import username_present


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
                            a += 1
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
                    usuarios.append((username, senha))
            response = render(request, 'escola/alunos/alunosList.html', context={'usuarios': usuarios})
            mail_managers("Lista de Senhas para uma nova popuação de usarios, imprima", response.content)
            return response

    context = {
        'formset': formset
    }
    return render(request, 'escola/alunos/formPopulateAlunos.html', context)


@permission_required_obj('escola.can_add_aluno', (Turma, 'pk', 'turma_pk'))
def add_aluno(request, turma_pk, qualquer=False):
    if request.method == 'POST':
        # FORM TUTORIAL: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
        # Create a form instance and populate it with data from the request (binding):
        form = AlunoCreateForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            turma = get_object_or_404(Turma, numero=form.cleaned_data['turma'], ano=datetime.date.today().year)
            if qualquer or turma.pk == turma_pk:
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
                        a += 1
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

                aluno.turma = turma
                aluno.save()
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