#  Developed by Vinicius José Fritzen
#  Last Modified 25/04/19 14:00.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

from rolepermissions.roles import AbstractUserRole


class Aluno(AbstractUserRole):
    available_permissions = {
        # '':True
    }

class Admin(AbstractUserRole):
    available_permissions = {

    }

class Professor(AbstractUserRole):
    available_permissions = {

    }