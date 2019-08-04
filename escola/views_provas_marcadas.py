#  Developed by Vinicius José Fritzen
#  Last Modified 20/05/19 15:02.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import logging
from datetime import datetime, timedelta
from dateutil import relativedelta

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.datetime_safe import date
from django.utils.safestring import mark_safe
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from rolepermissions.checkers import has_object_permission, has_role, has_permission

from escola import models
from escola.controller_provas_marcadas import CalendarioDatasLivresTurma
from escola.forms import MarcarProvaMateriaProfessorForm, MarcarProvaAreaProfessorForm
from escola.models import Turma

logger = logging.getLogger(__name__)


# Lista de Provas da Turma
class ListaProvasTurmaView(DetailView):
    """Retorna uma turma, e deixa o template exibir suas provas"""
    template_name = 'escola/provas_marcadas/provas_turma.html'
    context_object_name = 'turma'

    def get_object(self, queryset=None):
        self.turma = get_object_or_404(Turma,
                                       pk=self.kwargs.get('turma_pk'))
        return self.turma


# Adicionar prova de materia
class CreateProvaMateriaView(CreateView):
    form_class = MarcarProvaMateriaProfessorForm
    template_name = 'escola/provas_marcadas/marcar_prova_professor.html'

    def dispatch(self, request, *args, **kwargs):
        if has_role(request.user, 'professor') or has_role(request.user, 'Admin'):
            return super(CreateProvaMateriaView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'professor': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('escola:index')


# Adicionar prova de area
class CreateProvaAreaView(CreateView):
    form_class = MarcarProvaAreaProfessorForm
    template_name = 'escola/provas_marcadas/marcar_prova_professor.html'

    def dispatch(self, request, *args, **kwargs):
        if has_role(request.user, 'professor') or has_permission(request.user, 'add_prova_area_geral'):
            return super(CreateProvaAreaView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'professor': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('escola:index')


# Lista de provas do professor
class ListaProvasProfessorView(DetailView):
    template_name = "escola/provas_marcadas/listProvasProfessor.html"
    context_object_name = 'professor'

    def get_object(self, queryset=None):
        self.professor = self.request.user.professor
        return self.professor


# Apagar Prova de Materia
class ProvaMateriaDeleteView(DeleteView):
    model = models.ProvaMateriaMarcada
    template_name = "escola/base_delete.html"

    def get_object(self, queryset=None):
        """ Garante que o usuario possui permsissão"""
        obj = super(ProvaMateriaDeleteView, self).get_object(queryset)
        if not has_object_permission('can_edit_prova_materia', self.request.user, obj):
            raise PermissionDenied()
        return obj

    def get_success_url(self):
        return reverse('escola:index')


# Apagar prova de area
class ProvaAreaDeleteView(DeleteView):
    model = models.ProvaAreaMarcada
    template_name = "escola/base_delete.html"

    def get_object(self, queryset=None):
        """ Garante que o usuario possui permsissão"""
        obj = super(ProvaAreaDeleteView, self).get_object(queryset)
        if not has_object_permission('can_edit_prova_area', self.request.user, obj):
            raise PermissionDenied()
        return obj

    def get_success_url(self):
        return reverse('escola:index')


# Detalhes de prova
class ProvaDetailView(DetailView):
    template_name = 'escola/provas_marcadas/detail_prova.html'
    model = models.ProvaMarcada
    context_object_name = 'prova'


# Adicionar conteudos a prova

# Datas Livres da turma
class CalendarioTurmaDatasLivresView(ListView):
    model = models.EventoTurma
    template_name = 'escola/provas_marcadas/calendarioDatasLivres.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        date = get_date(self.request.GET.get('date', None))

        # Instantiate our calendar class with today's year and date
        cal = CalendarioDatasLivresTurma(date.year, date.month)
        context['year'] = date.year
        context['month'] = date.month
        next_month = date+relativedelta.relativedelta(months=1)
        prev_month = date-relativedelta.relativedelta(months=1)
        context['next'] = "{0}-{1}".format(next_month.year, next_month.month)
        context['prev'] = "{0}-{1}".format(prev_month.year, prev_month.month)
        context['turma__pk'] = self.kwargs.get('pk')

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(get_object_or_404(Turma, pk=self.kwargs.get('pk')), withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()
