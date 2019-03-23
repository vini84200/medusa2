from django.contrib.auth.models import User, Group
from guardian.shortcuts import assign_perm

from escola.models import CargoTurma


def username_present(username):
    if User.objects.filter(username=username).exists():
        return True

    return False


def dar_permissao_user(ocupante, cargo: CargoTurma):
    if cargo.cod_especial == 1:
        # PERMISSÔES DE LIDER
        group: Group = cargo.turma.get_or_create_lider_group()
        for user in group.user_set.all():
            group.user_set.remove(user)
        ocupante.groups.add(group)
    if cargo.cod_especial == 2:
        # PERMISSÔES DE VICELIDER
        group: Group = cargo.turma.get_or_create_vicelider_group()
        for user in group.user_set.all():
            group.user_set.remove(user)
        ocupante.groups.add(group)
    if cargo.cod_especial == 5:
        # PERMISSÔES DE REGENTE
        group: Group = cargo.turma.get_or_create_regente_group()
        for user in group.user_set.all():
            group.user_set.remove(user)
        ocupante.groups.add(group)
        # Permissões de Regente


def dar_permissao_perm_a_user_of_level(perm, level_min, turma, obj):
    if level_min == 1:
        assign_perm(perm,turma.get_or_create_lider_group(), obj)
        assign_perm(perm,turma.get_or_create_vicelider_group(), obj)
        assign_perm(perm,turma.get_or_create_regente_group(), obj)
    if level_min == 2:
        assign_perm(perm,turma.get_or_create_lider_group(), obj)
        assign_perm(perm,turma.get_or_create_regente_group(), obj)
    if level_min == 3:
        assign_perm(perm,turma.get_or_create_regente_group(), obj)