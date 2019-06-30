#  Developed by Vinicius José Fritzen
#  Last Modified 04/05/19 15:55.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import RequestContext
from django.views.generic import ListView, TemplateView

from escola.models import Horario, Turno, TurnoAula

logger = logging.getLogger(__name__)


@login_required()
def email_change(request):
    form = EmailChangeForm(request.user)
    if request.method=='POST':
        form = EmailChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('escola:index'))

    return render(request, "escola/email_change.html", {'form': form})
