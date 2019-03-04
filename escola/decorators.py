from django.core.exceptions import PermissionDenied
from .models import Profile, Professor, Aluno


def is_user_escola(function):
    def wrap(request, *args, **kwargs):
        try:
            profile = request.user.profile_escola
        except:
            profile = Profile(user=request.user, is_aluno=False, is_professor=False)
            profile.save()

        if (profile.is_aluno
                or profile.is_aluno
                or request.user.is_staff
                or request.user.is_superuser):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap