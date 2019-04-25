#  Developed by Vinicius José Fritzen
#  Last Modified 25/04/19 14:26.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

from rolepermissions.permissions import register_object_checker

from escola.models import MateriaDaTurma
from escola.roles import Aluno, Professor


@register_object_checker()
def create_tarefa(role, user, materia: MateriaDaTurma):
    """
    Verifica se o usuario tem permissão para criar uma tarefa para essa materia
    :return: Bool se tem perm
    """
    if role == Professor:
        return True

    if role == Aluno and materia.turma == user.Aluno.turma and materia.turma.lider == user:
        return True

    return False
