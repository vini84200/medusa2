""" Permissões personalizadas da API"""
#  Developed by Vinicius José Fritzen
#  Last Modified 12/04/19 13:19.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

from django.views import View
from rest_framework.permissions import BasePermission, DjangoModelPermissions
from rest_framework.request import Request


class IsAdminOrIsTheUser(DjangoModelPermissions):
    """Verifica se o usuario é adiministrador, ou esta no campo User do obj;"""
    def has_object_permission(self, request: Request, view: View, obj):
        """Verifica se tem permisão sobre obj"""
        if request.user.is_staff:
            return True
        return obj.user == request.user

