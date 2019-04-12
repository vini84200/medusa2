"""Exibe conteudos de uma materia."""
#  Developed by Vinicius José Fritzen
#  Last Modified 12/04/19 13:19.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, FormView, ListView, DeleteView
from mptt.forms import MoveNodeForm

from .forms import *
from .models import *
from .decorators import *


class ConteudoCreate(CreateView):
    """View para criar um Conteudo."""
    model = Conteudo
    form_class = ConteudoForm

    def dispatch(self, request, *args, **kwargs):
        """Pega valores dos args"""
        if 'pk_parent' in kwargs.keys():
            self.parent = kwargs['pk_parent']
        return super(ConteudoCreate, self).dispatch(request, *args, **kwargs)

    def get_initial(self, *args, **kwargs):
        """Altera o valor inicial dos campos"""
        initial = super(ConteudoCreate, self).get_initial()
        print(kwargs)
        if self.parent:
            logger.debug('ConteudoCreate:get_initial():in if loop.')
            initial['parent'] = self.parent
            # TODO: 10/04/2019 por wwwvi: Adicionar Teste;
        return initial

    def form_valid(self, form):
        """Altera o comportamento de validação do Form."""
        self.object = form.save(commit=False)
        self.object.professor = self.request.user.professor
        logger.debug(form.cleaned_data)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ConteudoUpdate(UpdateView):
    """View para criar um Conteudo."""
    model = Conteudo
    form_class = ConteudoForm
    context_object_name = 'conteudo'
    # TODO: 10/04/2019 por wwwvi: Testar


class ConteudoDetail(DetailView):
    """ Detalhes do Conteudo"""
    model = Conteudo

    @method_decorator(is_user_escola)
    def dispatch(self, request, *args, **kwargs):
        return super(ConteudoDetail, self).dispatch(request, *args, **kwargs)

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


class LinkConteudoCreateView(CreateView):
    """View para professores adicionarem links em um conteudo."""
    model = LinkConteudo
    fields = ['titulo', 'link', 'categoria', 'descricao', 'tags']
    success_url = reverse_lazy('escola:conteudos-professor')

    # TODO: 06/04/2019 por wwwvi: Test

    @method_decorator(is_professor)
    def dispatch(self, request, *args, **kwargs):
        self.conteudo = Conteudo.objects.get(pk=kwargs.get('pk'))
        self.categoria = kwargs.get('cat')
        if not request.user == self.conteudo.professor.user:
            logger.debug(request.user)
            logger.debug(self.conteudo)
            raise PermissionDenied("Você não tem permissão para adicionar um link aqui.")
        return super(LinkConteudoCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_class(self):
        form_class = super(LinkConteudoCreateView, self).get_form_class()
        form_class.helper = FormHelper()
        form_class.helper.add_input(Submit('submit', 'Salvar'))
        return form_class

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.conteudo = self.conteudo
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self):
        kwargs = super(LinkConteudoCreateView, self).get_initial()
        if self.categoria:
            kwargs.update({'categoria': self.categoria})
        return kwargs


class addConteudosAMateria(FormView):
    form_class = SelectConteudosForm
    template_name = 'escola/conteudo/addConteudoToMateria.html'
    success_url = reverse_lazy('escola:materias_professor')

    # TODO: 06/04/2019 por wwwvi: Test

    @method_decorator(is_professor)
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        self.materia = MateriaDaTurma.objects.get(pk=kwargs.get('materia'))
        return super(addConteudosAMateria, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.add_materia()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super(addConteudosAMateria, self).get_form_kwargs()
        kwargs.update({'professor': self.user.professor, 'materia': self.materia})
        return kwargs


class moveConteudoTree(FormView):
    pass  # form_class = MoveNodeForm
    # TODO: 06/04/2019 por wwwvi: Acabar formulario de mudar de lugar
    # TODO: 06/04/2019 por wwwvi: Test


class MeusConteudosListView(ListView):
    model = Conteudo
    context_object_name = 'conteudos'
    template_name = 'escola/professor/listConteudos.html'

    # TODO: 06/04/2019 por wwwvi: Terminar

    def dispatch(self, request, *args, **kwargs):
        """Regista o usuario."""
        self.user = request.user
        return super(MeusConteudosListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Conteudo.objects.filter(professor=self.user.professor).all()

# TODO: 06/04/2019 por wwwvi: Test


class RemoveLinkFromConteudoView(DeleteView):
    """Remove o link de algum conteudo"""
    pass  # TODO: 10/04/2019 por wwwvi: Terminar
    # SOBRESCREVER CODIGO QUE REALIZA EXCLUSÂO PARA RETIRAR DA LISTA.


class RemoveConteudoFromMateriaView(DeleteView):
    """Remove o conteudo de uma materia"""
    pass  # TODO: 10/04/2019 por wwwvi: Terminar
    # SOBRESCREVER CODIGO QUE REALIZA EXCLUSÂO PARA RETIRAR DA LISTA.
