#  Developed by Vinicius José Fritzen
#  Last Modified 20/05/19 15:02.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import logging

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, DetailView

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
    pass

# Adicionar prova de area

# Editar Prova de Materia

# Editar Prova de Area

# Apagar Prova de Materia

# Apagar prova de area

# Detalhes de prova

# Adicionar conteudos a prova

# Datas Livres da turma
