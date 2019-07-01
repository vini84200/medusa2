#  Developed by Vinicius José Fritzen
#  Last Modified 04/05/19 15:55.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from escola.form import EmailChangeForm

logger = logging.getLogger(__name__)


@login_required()
def email_change(request):
    form = EmailChangeForm(request.user)
    if request.method == 'POST':
        form = EmailChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('escola:index'))

    return render(request, "escola/email_change.html", {'form': form})
