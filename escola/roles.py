#  Developed by Vinicius José Fritzen
#  Last Modified 26/04/19 23:27.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

from rolepermissions.roles import AbstractUserRole


class Aluno(AbstractUserRole):
    available_permissions = {
        # '': True

    }
    permissions_role = []


class Admin(AbstractUserRole):
    available_permissions = {
        'add_turma': True,
        'populate_alunos': True,
        'add_aluno_g': True,
        'edit_horario_g': True,
        'add_professor': True,
        'add_materia_g': True,
        'add_cargo_g': True,
        'marcar_prova_g': True,
        'add_prova_area_geral': True,
        'marcar_prova_area': True,
        'send_aviso': True,
    }
    permissions_role = [
        'add_turma',
        'populate_alunos',
        'add_aluno_g',
        'edit_horario_g',
        'add_professor',
        'add_materia_g',
        'add_cargo_g',
        'marcar_prova_g',
        'add_prova_area_geral',
        'marcar_prova_area',
        'send_aviso',
        'send_avisos',
        ]


class Professor(AbstractUserRole):
    available_permissions = {
        'marcar_prova_area': True,
        'create_provas': True,
        'send_aviso': True,
    }
    permissions_role = [
        'marcar_prova_area',
        'create_provas',
        'send_aviso',
        'send_avisos',
        ]
