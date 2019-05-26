#  Developed by Vinicius José Fritzen
#  Last Modified 20/05/19 15:02.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import logging

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.functional import lazy
from django.views.generic import ListView, CreateView, DetailView
from rolepermissions.checkers import has_object_permission, has_role, has_permission

from escola.forms import MarcarProvaMateriaProfessorForm, MarcarProvaAreaProfessorForm
from escola.models import Turma, Professor

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
        if has_role(request.user, 'Professor') or has_role(request.user, 'Admin'):
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
        if has_role(request.user, 'Professor') or has_permission(request.user, 'add_prova_area_geral'):
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

# Editar Prova de Materia

# Editar Prova de Area

# Apagar Prova de Materia

# Apagar prova de area

# Detalhes de prova

# Adicionar conteudos a prova

# Datas Livres da turma
