#  Developed by Vinicius José Fritzen
#  Last Modified 26/04/19 23:30.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
from rolepermissions.checkers import has_role, has_permission
from rolepermissions.permissions import register_object_checker

from escola.models import MateriaDaTurma


@register_object_checker()
def create_tarefa(role, user, materia: MateriaDaTurma):
    """
    Verifica se o usuario tem permissão para criar uma tarefa para essa materia
    :return: Bool se tem perm
    """
    if user.is_superuser:
        return True

    if has_role(user, 'professor'):
        return True

    if has_role(user, 'admin') and materia.turma == user.Aluno.turma and materia.turma.lider == user:
        return True

    return False


@register_object_checker()
def add_aluno(role, user, turma):
    """Verifica se pode adicionar aluno na turma"""
    if user.is_superuser:
        return True

    if user == turma.regente:
        return True

    if has_permission(user, 'add_aluno_g'):
        return True

    return False


@register_object_checker()
def edit_horario(role, user, turma):
    """Verifica se pode mudar o horario da turma"""
    if user.is_superuser:
        return True

    if has_permission(user, 'edit_horario_g'):
        return True

    if user == turma.regente or user == turma.lider or user == turma.vicelider:
        return True

    return False


@register_object_checker()
def add_materia(role, user, turma):
    """Verifica se pode adicionar uma materia a uma turma"""
    if user.is_superuser:
        return True

    if has_permission(user, 'add_materia_g'):
        return True

    if user == turma.regente:
        return True

    return False


@register_object_checker()
def edit_materia(role, user, materia: MateriaDaTurma):
    """Verifica se o user tem previlegios de alterar a materia"""
    if user.is_superuser:
        return True

    if has_permission(user, 'edit_materia_g'):
        return True

    if user == materia.professor.user:
        return True

    return False


@register_object_checker()
def delete_materia(role, user, materia: MateriaDaTurma):
    """Verifica se o user tem previlegios de apagar a materia"""
    if user.is_superuser:
        return True

    if has_permission(user, 'delete_materia_g'):
        return True

    if user == materia.professor.user:
        return True

    return False


@register_object_checker()
def add_tarefa(role, user, turma):
    if user.is_superuser:
        return True

    if has_permission(user, 'add_tarefa_g'):
        return True

    if user == turma.regente or user == turma.lider or user == turma.vicelider:
        return True

    if user in [mat.professor.user for mat in turma.materias.all()]:
        return True

    return False


@register_object_checker()
def add_tarefa_mat(role, user, materia):
    if user.is_superuser:
        return True

    if has_permission(user, 'add_tarefa_g'):
        return True

    if user == materia.turma.regente or user == materia.turma.lider or user == materia.turma.vicelider:
        return True

    if user == materia.professor.user:
        return True
    return False

@register_object_checker()
def edit_tarefa(role, user, tarefa):
    if user.is_superuser:
        return True

    if has_permission(user, 'edit_tarefa_g'):
        return True

    if user == tarefa.turma.regente or user == tarefa.turma.lider:
        return True

    if user == tarefa.materia.professor.user:
        return True

    return False


@register_object_checker()
def delete_tarefa(role, user, tarefa):
    if user.is_superuser:
        return True

    if has_permission(user, 'delete_tarefa_g'):
        return True

    if user == tarefa.turma.regente or user == tarefa.turma.lider:
        return True

    if user == tarefa.materia.professor.user:
        return True

    return False


@register_object_checker()
def add_cargo(role, user, turma):
    if user.is_superuser:
        return True

    if has_permission(user, 'add_cargo_g'):
        return True

    return False


@register_object_checker()
def marcar_prova_m_turma(role, user, turma):
    if has_role(user, 'professor'):
        return True
    if user.is_staff:
        return True
    return False
