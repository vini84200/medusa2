import logging

from django.core.exceptions import PermissionDenied
from django.shortcuts import reverse
from django.views.generic import DetailView, FormView
from rolepermissions.checkers import has_permission

from escola.forms import AvisoTurmaForm, CreateAvisoMixedForm
from escola.models import AvisoGeral
from escola.user_check_mixin import (UserCheckHasPermission,
                                     UserCheckHasRolePermission)

logger = logging.getLogger(__name__)


class AvisoDetailView(DetailView):
    template_name = 'escola/aviso/aviso_detail.html'
    model = AvisoGeral
    context_object_name = 'aviso'


class AvisoTurmaCreateView(FormView):
    form_class = AvisoTurmaForm
    template_name = 'escola/base_form.html'

    def dispatch(self, request, *args, **kwargs):
        if not has_permission(request.user, 'send_aviso'):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('escola:index')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'owner': self.request.user
        })
        return kwargs


class AvisoMixedCreateView(UserCheckHasRolePermission, FormView):
    form_class = CreateAvisoMixedForm
    template_name = 'escola/base_form.html'
    user_check_permission = 'send_avisos'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'owner': self.request.user
        })
        return kwargs

    def get_success_url(self):
        return reverse('escola:index')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
