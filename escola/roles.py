#  Developed by Vinicius José Fritzen
#  Last Modified 25/04/19 14:31.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

from rolepermissions.roles import AbstractUserRole


class Aluno(AbstractUserRole):
    available_permissions = {
        # '': True

    }


class Admin(AbstractUserRole):
    available_permissions = {
        'add_turma': True,
        'populate_alunos': True,
    }


class Professor(AbstractUserRole):
    available_permissions = {

    }