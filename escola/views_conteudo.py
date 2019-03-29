"""Exibe conteudos de uma materia."""
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView

from .forms import *
from .models import *

class ConteudoCreate(CreateView):
    """View para criar um Conteudo."""
    model = Conteudo
    form_class = ConteudoForm

    def get_initial(self, *args, **kwargs):
        """Altera o valor inicial dos campos"""
        initial = super(ConteudoCreate, self).get_initial(**kwargs)
        if 'pk_parent' in kwargs.keys():
            initial['parent'] = kwargs['pk_parent']
        return initial

    def form_valid(self, form):
        """Altera o comportamento de validação do Form."""
        self.object = form.save(commit=False)
        self.object.professor = self.request.user.professor
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ConteudoUpdate(UpdateView):
    """View para criar um Conteudo."""
    model = Conteudo
    form_class = ConteudoForm
    context_object_name = 'conteudo'


class ConteudoDetail(DetailView):
    """ Detalhes do Conteudo"""
    model = Conteudo

    def get_context_data(self, **kwargs):
        """ Adiciona itens ao Context """
        context = super(ConteudoDetail, self).get_context_data(**kwargs)
        categorias = []
        for cat in CategoriaConteudo.objects.all():
            categorias.append({'obj': cat,
                               'links': LinkConteudo.objects.filter(conteudo=context['object'])
                               })
        context['categorias'] = categorias
        return context
