"""Exibe conteudos de uma materia."""
#  Developed by Vinicius José Fritzen
#  Last Modified 12/04/19 22:06.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

import logging

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView, DeleteView, DetailView, FormView, ListView, UpdateView)
from rolepermissions.checkers import has_object_permission

from escola.decorators import is_professor, is_user_escola
from escola.forms import (AdicionarMateriaConteudoForm, ConteudoForm,
                          SelectConteudosForm)
from escola.models import (CategoriaConteudo, Conteudo, LinkConteudo,
                           MateriaDaTurma)
from escola.user_check_mixin import (UserCheckHasObjectPermission,
                                     UserCheckHasObjectPermissionFromPk,
                                     UserCheckHasObjectPermissionGet,
                                     UserCheckReturnForbbiden)

logger = logging.getLogger(__name__)


class ConteudoCreate(CreateView):
    """
    View para criar um Conteudo.

    Dispatch Args:

    pk_parent : int - opicional
    """
    model = Conteudo
    form_class = ConteudoForm
    template_name = 'escola/conteudo/create_conteudo.html'

    def dispatch(self, request, *args, **kwargs):
        """Pega valores dos args"""
        if 'pk_parent' in kwargs.keys():
            self.parent = kwargs['pk_parent']
        return super(ConteudoCreate, self).dispatch(request, *args, **kwargs)

    def get_initial(self, *args, **kwargs):
        """Altera o valor inicial dos campos"""
        initial = super(ConteudoCreate, self).get_initial()
        print(kwargs)
        if hasattr(self, 'parent'):
            initial['parent'] = self.parent
        return initial

    def form_valid(self, form):
        """Altera o comportamento de validação do Form."""
        self.object = form.save(commit=False)
        self.object.professor = self.request.user.professor
        logger.debug(form.cleaned_data)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ConteudoUpdateView(UpdateView):
    """View para criar um Conteudo."""
    model = Conteudo
    form_class = ConteudoForm
    context_object_name = 'conteudo'
    template_name = 'escola/conteudo/create_conteudo.html'


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
                               'links': LinkConteudo.objects.filter(
                                   conteudo=context['object'], categoria=cat)
                               })
        context['categorias'] = categorias
        if (hasattr(self.request.user, 'professor') and
                self.request.user.professor == self.object.professor):
            materias = self.object.materias.all()
            context.update({
                'is_owner': True,
                'materias': materias,
                'materias__len': len(materias),
                })
        else:
            context.update({'is_owner': False})
        return context


class LinkConteudoCreateView(CreateView):
    """
    View para professores adicionarem links em um conteudo.

    Dispatch args;
    pk : int - obrigatorio - PK do conteudo em que dee ser criado
    cat : int - opicional - PK da categoria inicial. Se nao passado,
    o campo é iniciado em branco;
    """
    model = LinkConteudo
    fields = ['titulo', 'link', 'categoria', 'descricao', 'tags']

    # TODO: 06/04/2019 por wwwvi: Test

    def get_success_url(self):
        return reverse('escola:conteudo-detail', args=(self.kwargs['pk'], ))

    @method_decorator(is_professor)
    def dispatch(self, request, *args, **kwargs):
        self.conteudo = Conteudo.objects.get(pk=kwargs.get('pk'))
        self.categoria = kwargs.get('cat')
        if not has_object_permission('can_edit_conteudo', request.user,
                                     self.conteudo):
                                    # request.user ==
                                    #  self.conteudo.professor.user:
            logger.info(request.user)
            logger.info(self.conteudo)
            raise PermissionDenied("Você não tem permissão para adicionar "
                                   "um link aqui.")
        return super(LinkConteudoCreateView, self).dispatch(request, *args,
                                                            **kwargs)

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
    # FIXME: Lembre-se de adicionar permissões mais exatas do que apenas
    # conferir se é um professor, usar can_add_conteudo_to_materia.

    @method_decorator(is_professor)
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        self.materia = MateriaDaTurma.objects.get(pk=kwargs.get('materia'))
        return super(addConteudosAMateria, self).dispatch(request, *args,
                                                          **kwargs)

    def form_valid(self, form):
        form.add_materia()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super(addConteudosAMateria, self).get_form_kwargs()
        kwargs.update({'professor': self.user.professor,
                       'materia': self.materia})
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
        return super(MeusConteudosListView, self).dispatch(request, *args,
                                                           **kwargs)

    def get_queryset(self):
        return Conteudo.objects.filter(professor=self.user.professor).all()

# TODO: 06/04/2019 por wwwvi: Test


class RemoveLinkFromConteudoView(UserCheckHasObjectPermissionGet,
                                 UserCheckReturnForbbiden, DeleteView):
    """Remove o link de algum conteudo"""
    model = LinkConteudo
    user_check_obj_permission = 'can_remove_link_conteudo'
    template_name = 'escola/base_delete.html'

    def get_success_url(self):
        return reverse('escola:delete-link-conteudo', self.obj_conteuto_pk)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        self.obj_conteuto_pk = obj.conteudo.pk
        return obj


class RemoveConteudoFromMateriaView(DeleteView):
    """Remove o conteudo de uma materia"""
    pass  # TODO: 10/04/2019 por wwwvi: Terminar
    # SOBRESCREVER CODIGO QUE REALIZA EXCLUSÂO PARA RETIRAR DA LISTA.


class AdicionarAVariasMateriasView(UserCheckHasObjectPermissionFromPk, FormView):
    """
    Adicionar um conteudo a diversas materias com apenas um form.
    Deve receber um pk de um conteudo, com o nome de pk.
    """
    form_class = AdicionarMateriaConteudoForm
    template_name = "escola/base_form.html"
    user_check_object_name = 'object'
    user_check_obj_permission = 'can_add_conteudo_to_materias'
    checker_model = Conteudo

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_materias(self):
        if not hasattr(self, 'materias'):
            self.materias = MateriaDaTurma.objects.filter(
                professor=self.request.user.professor)
        return self.materias

    def get_form_kwargs(self):
        kwargs = super(AdicionarAVariasMateriasView, self).get_form_kwargs()
        kwargs.update({'materias': self.get_materias(),
                       'conteudo': self.object})
        return kwargs
