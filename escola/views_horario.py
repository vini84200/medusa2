#  Developed by Vinicius José Fritzen
#  Last Modified 12/04/19 13:19.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from guardian.decorators import permission_required as permission_required_obj

from escola.decorators import is_user_escola
from escola.forms import PeriodoForm
from escola.models import Turma, MateriaDaTurma, Horario, Turno, TurnoAula


@is_user_escola
def ver_horario(request, turma_pk):
    context = {'turma': get_object_or_404(Turma, pk=turma_pk), }
    return render(request, 'escola/horario/mostraHorario.html', context=context)


class PeriodoFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PeriodoFormSetHelper, self).__init__(*args, **kwargs)
        self.add_input(Submit("submit", "Adicionar"))
        self.form_show_labels = False


@is_user_escola
@permission_required_obj('escola.editar_horario', (Turma, 'pk', 'turma_pk'))
def alterar_horario(request, turno_cod, dia_cod, turma_pk):

    horario: Horario = get_object_or_404(Horario, turma_id=turma_pk)

    PeriodoFormSet = formset_factory(PeriodoForm, extra=5, max_num=5)

    data = request.POST or None

    formset = PeriodoFormSet(data=data)
    helper = PeriodoFormSetHelper()
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
    DIAS_DA_SEMANA = ['Domingo',
                          'Segunda-feira',
                          'Terça-feira',
                          'Quarta-feira',
                          'Quinta-feira',
                          'Sexta-feira',
                          'Sabado', ]
    turnos = Turno.objects.all().order_by('cod')

    formset, ta = genarate_initial_form(PeriodoFormSet, dia_cod, formset, horario, turno_cod)

    return render(request, 'escola/horario/editarHorario.html',
                  context={'turnos': turnos, 'DIAS_DA_SEMANA': DIAS_DA_SEMANA, 'DIAS_DA_SEMANA_N': range(1,8),
                           'ta': ta, 'edit_turno': turno_cod, 'edit_dia': dia_cod, 'formset': formset,
                           'range': range(1, 6), 'turma_pk': turma_pk, 'turma': get_object_or_404(Turma, pk=turma_pk),
                           'helper': helper})


def genarate_initial_form(PeriodoFormSet, dia_cod, formset, horario, turno_cod):
    ta = horario.get_horario()
    if turno_cod in ta and dia_cod in ta[turno_cod]:
        ini = []
        for periodo in ta[turno_cod][dia_cod].periodo_set.all():
            ini.append({'materia': periodo.materia})
        formset = PeriodoFormSet(initial=ini)
        for form in formset:
            form.fields['materia'].queryset = MateriaDaTurma.objects.filter(turma=horario.turma)
    return formset, ta