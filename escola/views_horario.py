from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from guardian.decorators import permission_required as permission_required_obj

from escola.decorators import is_user_escola
from escola.forms import PeriodoForm
from escola.models import Turma, MateriaDaTurma
from escola.models_horario import Horario, Turno, TurnoAula


@is_user_escola
def ver_horario(request, turma_pk):
    horario = Horario.objects.get(turma__id=turma_pk)
    if not horario:
        horario = Horario(turma=Turma.objects.get(pk=turma_pk))
        horario.save()
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
#@user_has_perm_or_turma_cargo('escola.editar_horario')
@permission_required_obj('escola.edit_horario', (Turma, 'pk', 'turma_pk'))
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