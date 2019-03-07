import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.decorators import login_required, permission_required
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .decorators import *
from .forms import *


#   HELPERS
def username_present(username):
    if User.objects.filter(username=username).exists():
        return True

    return False


def fun_perm_or_group(perm: str, group):
    return lambda u: u.has_perm(perm) or u in group


#   VIEWS:


@login_required
@is_user_escola
def index(request):
    context = {'request': request}
    if request.user.profile_escola.is_aluno:
        # HORARIO
        turma_pk = request.user.aluno.turma.pk
        horario = get_object_or_404(Horario, turma_id=turma_pk)
        turnos = Turno.objects.all().order_by('cod')
        DIAS_DA_SEMANA = ['Domingo',
                          'Segunda-feira',
                          'Terça-feira',
                          'Quarta-feira',
                          'Quinta-feira',
                          'Sexta-feira',
                          'Sabado', ]
        DIAS_DA_SEMANA_N = range(1, 8)
        ta = {}
        for turno in turnos:
            for dia in DIAS_DA_SEMANA_N:
                a = TurnoAula.objects.filter(turno=turno, diaDaSemana=dia, horario=horario)
                if len(a) > 0:
                    if dia not in ta:
                        ta[dia] = dict()
                    ta[dia][turno.cod] = a[0]

        context.update({'turnos': turnos, 'DIAS_DA_SEMANA': DIAS_DA_SEMANA, 'DIAS_DA_SEMANA_N': DIAS_DA_SEMANA_N,
                        'ta': ta, 'turma_pk': turma_pk, 'range': range(1, 6)})
        # TAREFAS
        tarefas = Tarefa.objects.filter(turma__pk=turma_pk, deadline__gte=datetime.date.today()).order_by('deadline')
        tarefas_c = []
        for tarefa in tarefas:
            tarefas_c.append((tarefa, tarefa.get_completacao(request.user.aluno)))
        context.update({'tarefas': tarefas_c, 'turma': get_object_or_404(Turma, pk=turma_pk)})

    return render(request, 'escola/home.html', context=context)


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

            return render(request, 'escola/alunos/alunosList.html', context={'usuarios': usuarios})

    context = {
        'formset': formset
    }
    return render(request, 'escola/alunos/formPopulateAlunos.html', context)


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
        form = CargoForm(request.POST, turma=cargo.turma)

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


@user_has_perm_or_turma_cargo('escola.can_add_aluno', lider=False, alter_qualquer=True)
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
                    return HttpResponseRedirect(reverse('list-alunos', args=[turma.pk]))
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


@is_user_escola
def ver_horario(request, turma_pk):
    horario = get_object_or_404(Horario, turma_id=turma_pk)
    turnos = Turno.objects.all().order_by('cod')
    DIAS_DA_SEMANA = ['Domingo',
                      'Segunda-feira',
                      'Terça-feira',
                      'Quarta-feira',
                      'Quinta-feira',
                      'Sexta-feira',
                      'Sabado', ]
    DIAS_DA_SEMANA_N = range(1, 8)
    ta = {}
    for turno in turnos:
        for dia in DIAS_DA_SEMANA_N:
            a = TurnoAula.objects.filter(turno=turno, diaDaSemana=dia, horario=horario)
            if len(a) > 0:
                if not dia in ta:
                    ta[dia] = dict()
                ta[dia][turno.cod] = a[0]

    context = {'turnos': turnos, 'DIAS_DA_SEMANA': DIAS_DA_SEMANA, 'DIAS_DA_SEMANA_N': DIAS_DA_SEMANA_N,
               'ta': ta, 'turma_pk': turma_pk, 'range': range(1, 6)}

    return render(request, 'escola/horario/mostraHorario.html', context=context)


@is_user_escola
@user_has_perm_or_turma_cargo('escola.editar_horario')
def alterar_horario(request, turno_cod, dia_cod, turma_pk):
    horario: Horario = get_object_or_404(Horario, turma_id=turma_pk)
    PeriodoFormSet = formset_factory(PeriodoForm, extra=5, max_num=5)
    data = request.POST or None
    formset = PeriodoFormSet(data=data)
    for form in formset:
        form.fields['materia'].queryset = MateriaDaTurma.objects.filter(turma=horario.turma)
    if request.method == 'POST':
        if formset.is_valid():
            n = 1
            for form in formset:
                per = horario.get_periodo_or_create(dia_cod, turno_cod, n)
                per.materia = form.cleaned_data['materia']
                per.save()
                n += 1
            return HttpResponseRedirect(reverse('escola:show-horario', args=[turma_pk]))
    else:
        # Visual

        turnos = Turno.objects.all().order_by('cod')
        DIAS_DA_SEMANA = ['Domingo',
                          'Segunda-feira',
                          'Terça-feira',
                          'Quarta-feira',
                          'Quinta-feira',
                          'Sexta-feira',
                          'Sabado', ]
        DIAS_DA_SEMANA_N = range(1, 8)
        ta = {}
        for turno in turnos:
            for dia in DIAS_DA_SEMANA_N:
                a = TurnoAula.objects.filter(turno=turno, diaDaSemana=dia, horario=horario)
                if len(a) > 0:
                    if not dia in ta:
                        ta[dia] = dict()
                    ta[dia][turno.cod] = a[0]
        if (turno_cod in ta and dia_cod in ta[turno_cod]):
            ini = []
            for periodo in ta[turno_cod][dia_cod].periodo_set.all():
                ini.append({'materia': periodo.materia})
            formset = PeriodoFormSet(initial=ini)
            for form in formset:
                form.fields['materia'].queryset = MateriaDaTurma.objects.filter(turma=horario.turma)

    return render(request, 'escola/horario/editarHorario.html',
                  context={'turnos': turnos, 'DIAS_DA_SEMANA': DIAS_DA_SEMANA, 'DIAS_DA_SEMANA_N': DIAS_DA_SEMANA_N,
                           'ta': ta, 'edit_turno': turno_cod, 'edit_dia': dia_cod, 'formset': formset,
                           'range': range(1, 6), 'turma_pk': turma_pk})


@permission_required('escola.edit_aluno')
def edit_aluno():
    # TODO: Implement edit aluno
    raise NotImplementedError


@permission_required('escola.can_delete_aluno')
def delete_aluno(request, aluno_pk):
    aluno = get_object_or_404(Aluno, pk=aluno_pk)
    turma = aluno.turma
    aluno.delete()
    return HttpResponseRedirect(reverse('escola:list-alunos', args=[turma.pk]))


@permission_required('escola.can_add_professor')
def add_professor(request):
    if request.method == 'POST':

        # FORM TUTORIAL: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
        # Create a form instance and populate it with data from the request (binding):
        form = ProfessorCreateForm(request.POST)

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
            profile = Profile(user=user, is_aluno=False, is_professor=True)
            profile.save()
            professor = Professor()
            professor.user = user
            professor.nome = nome
            professor.save()
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


# @permission_required('escola.can_add_materia')
@user_has_perm_or_turma_cargo('escola.can_add_materia')
def add_materia(request, turma_pk):
    if request.method == 'POST':
        form = MateriaForm(request.POST)
        if form.is_valid():
            materia = MateriaDaTurma()
            materia.nome = form.cleaned_data['nome']
            materia.turma = get_object_or_404(Turma, pk=turma_pk)
            materia.professor = form.cleaned_data['professor']
            materia.abreviacao = form.cleaned_data['abreviacao']
            materia.save()
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


# @permission_required('escola.can_edit_materia')
@user_has_perm_or_turma_cargo('escola.can_edit_materia')
def edit_materia(request, turma_pk, materia_pk):
    if request.method == 'POST':
        form = MateriaForm(request.POST)
        if form.is_valid():
            materia = MateriaDaTurma()
            materia.nome = form.cleaned_data['nome']
            materia.turma = get_object_or_404(Turma, pk=turma_pk)
            materia.professor = form.cleaned_data['professor']
            materia.abreviacao = form.cleaned_data['abreviacao']
            materia.save()
    else:

        form = MateriaForm(get_object_or_404(MateriaDaTurma, pk=materia_pk))

    context = {
        'form': form,
    }
    return render(request, 'escola/materia/formMateria.html', context=context)


@user_has_perm_or_turma_cargo('escola.can_delete_materia')
def delete_materia(request, turma_pk, materia_pk):
    materia = get_object_or_404(MateriaDaTurma, pk=materia_pk)
    materia.delete()
    return HttpResponseRedirect(reverse('escola:list-materias', args=[turma_pk]))


@user_has_perm_or_turma_cargo('escola.can_add_tarefa')
def add_tarefa(request, turma_pk):
    turma = get_object_or_404(Turma, pk=turma_pk)
    if request.method == 'POST':
        form = TarefaForm(turma, request.POST)
        if form.is_valid():
            tarefa = Tarefa()
            tarefa.titulo = form.cleaned_data['titulo']
            tarefa.turma = turma
            tarefa.materia = form.cleaned_data['materia']
            tarefa.tipo = form.cleaned_data['tipo']
            tarefa.descricao = form.cleaned_data['descricao']
            tarefa.deadline = form.cleaned_data['deadline']
            tarefa.save()
            return HttpResponseRedirect(reverse('escola:list-materias', args=[turma_pk]))
    else:
        form = TarefaForm(turma=turma)

    context = {
        'form': form,
    }
    return render(request, 'escola/tarefas/formTarefa.html', context=context)


def list_tarefa(request, turma_pk):
    tarefas = Tarefa.objects.filter(turma__pk=turma_pk)
    if request.user.profile_escola.is_aluno:
        tarefas_c = []
        for tarefa in tarefas:
            tarefas_c.append((tarefa, tarefa.get_completacao(request.user.aluno)))
        return render(request, 'escola/tarefas/listTarefasParaAluno.html',
                      context={'tarefas': tarefas_c, 'turma': get_object_or_404(Turma, pk=turma_pk)})
    else:
        return render(request, 'escola/tarefas/listTarefas.html', context={'tarefas': tarefas})


@user_has_perm_or_turma_cargo('escola.can_edit_tarefa')
def edit_tarefa(request, tarefa_pk):
    tarefa = get_object_or_404(Tarefa, pk=tarefa_pk)
    turma = tarefa.turma
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
            return HttpResponseRedirect(reverse('escola:list-tarefas', args=[turma.pk]))
    else:
        form = TarefaForm(turma=turma, initial={'titulo': tarefa.titulo, 'materia': tarefa.materia, 'tipo': tarefa.tipo,
                                                'descricao': tarefa.descricao, 'deadline': tarefa.deadline})

    context = {
        'form': form,
    }
    return render(request, 'escola/tarefas/formTarefa.html', context=context)


@user_has_perm_or_turma_cargo('escola.can_delete_tarefa')
def delete_tarefa(request, tarefa_pk):
    tarefa = get_object_or_404(Tarefa, pk=tarefa_pk)
    tarefa.delete()
    return HttpResponseRedirect(reverse('escola:index'))


def concluir_tarefa(request, tarefa_pk):
    tarefa: Tarefa = get_object_or_404(Tarefa, pk=tarefa_pk)
    conclusao = tarefa.get_completacao(request.user.aluno)
    conclusao.completo = not conclusao.completo
    conclusao.save()
    return HttpResponseRedirect(reverse('escola:index'))


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
            # TODO: enviar msg para o professor, {e outros?}
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
