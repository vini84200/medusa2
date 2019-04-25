#  Developed by Vinicius José Fritzen
#  Last Modified 25/04/19 18:04.
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
        'add_aluno_g': True,
        'edit_horario_g': True,
    }


class Professor(AbstractUserRole):
    available_permissions = {

    }