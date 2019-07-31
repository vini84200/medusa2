"""Testes Mixin"""

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from rolepermissions.checkers import has_permission, has_object_permission


def redirect(path):
    return HttpResponseRedirect(path)


class UserCheckMixin:
    user_check_failure_path = ''  # can be path, url name or reverse_lazy

    def check_user(self, user):
        return True

    def user_check_failed(self, request, *args, **kwargs):
        return redirect(self.user_check_failure_path)

    def dispatch(self, request, *args, **kwargs):
        if not self.check_user(request.user):
            return self.user_check_failed(request, *args, **kwargs)
        return super(UserCheckMixin, self).dispatch(request, *args, **kwargs)


class UserCheckHasPermission(UserCheckMixin):
    user_check_permission = ''

    def check_user(self, user):
        return has_permission(user, self.user_check_permission)


class UserCheckReturnForbbiden(UserCheckMixin):
    def user_check_failed(self, request, *args, **kwargs):
        raise PermissionDenied


class UserCheckHasObjectPermission(UserCheckMixin):
    user_check_obj_permission = ''
    user_check_object_name = 'object'

    def user_check_get_object(self):
        return getattr(self, self.user_check_object_name)

    def check_user(self, user):
        return has_object_permission(self.user_check_obj_permission, user, self.user_check_get_object())


class UserCheckHasObjectPermissionGet(UserCheckHasObjectPermission):
    def user_check_get_object(self):
        return self.get_object()