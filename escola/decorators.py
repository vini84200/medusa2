from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Profile, Turma


def get_login_redirect(request):
    return HttpResponseRedirect(reverse('login')+'?next='+request.path)


def is_user_escola(function):
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
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def is_aluno(function):
    """Decorator, adiconado ao Dispatch, verifica se o usario é um aluno"""
    def wrap(request, *args, **kwargs):
        user = request
        if not user.is_authenticated:
            return get_login_redirect(request)
        profile, c = Profile.objects.get_or_create(user=user, defaults={'is_aluno': False, 'is_professor': False})
        if not profile.is_aluno:
            return get_login_redirect(request)
        return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def is_professor(function):
    """Decorator, adiconado ao Dispatch, verifica se o usario é um professor"""
    def wrap(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return get_login_redirect(request)
        profile, c = Profile.objects.get_or_create(user=user, defaults={'is_aluno': False, 'is_professor': False})
        if not profile.is_professor:
            return get_login_redirect(request)
        return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    return wrap
