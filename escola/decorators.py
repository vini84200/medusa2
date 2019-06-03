#  Developed by Vinicius José Fritzen
#  Last Modified 12/04/19 13:19.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

from functools import wraps

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse

from escola.models import Profile


def get_login_redirect(request):
    return HttpResponseRedirect(reverse('login') + '?next=' + request.path)


def is_user_escola(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return get_login_redirect(request)
        profile, c = Profile.objects.get_or_create(user=request.user, defaults={'is_aluno': False, 'is_professor': False})
        if (profile.is_aluno
                or profile.is_professor
                or request.user.is_staff
                or request.user.is_superuser):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap


def is_aluno(function):
    """Decorator, adiconado ao Dispatch, verifica se o usario é um aluno"""
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user = request
        if not user.is_authenticated:
            return get_login_redirect(request)
        profile, c = Profile.objects.get_or_create(user=user, defaults={'is_aluno': False, 'is_professor': False})
        if not profile.is_aluno:
            return get_login_redirect(request)
        return function(request, *args, **kwargs)
    return wrap


def is_professor(function):
    """Decorator, adiconado ao Dispatch, verifica se o usario é um professor"""
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return get_login_redirect(request)
        profile, c = Profile.objects.get_or_create(user=user, defaults={'is_aluno': False, 'is_professor': False})
        if not profile.is_professor:
            return get_login_redirect(request)
        return function(request, *args, **kwargs)
    return wrap
