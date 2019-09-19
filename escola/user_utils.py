"""Mantem funções para criar usuarios, e seus grupos padrões."""
#  Developed by Vinicius José Fritzen
#  Last Modified 26/04/19 16:30.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import logging

from django.contrib.auth.models import User, Group
from rolepermissions.roles import assign_role

from escola.models import Aluno, Professor
from users.models import Profile

logger = logging.getLogger(__name__)


def create_user(username, password, **kwargs) -> User:
    """
    Cria um usuario com esses dados
    :param username: Nome de usuario
    :param password: Senha
    :param kwargs: Veja abaixo...
    :keyword email:
        Opicional email do usuario
    :return: Usuario Criado
    :rtype User
    """
    u = User.objects.create_user(
        username, password=password, email=kwargs.get('email'))
    p = Profile(user=u)
    p.is_professor = False
    p.is_aluno = False
    p.save()
    return u


def give_admin(user: User) -> None:
    """
    Transforma o usuario em admin;
    :param User user:
    :return: None
    """
    user.is_staff = True
    user.groups.add(get_admin_group())
    user.save()


def create_admin_user(username: str, password: str, *args, **kwargs) -> User:
    """
    Cria um usuario com status de admin.
    :param username: Nome de usuario para ele
    :param password: Senha
    :keyword email:
        Opicional, email da conta a ser criada
    :return: Usuario criado
    :rtype: User
    """
    user = User.objects.create_user(
        username, password=password, email=kwargs.get('email'))
    give_admin(user)
    return user


def get_admin_group() -> Group:
    """
    Pega ou cria o grupo de Admins
    :return: Grupo de Admins
    :rtype: Group
    LOGS:"Por algum motivo o Grupo admin não havia sido criado." se um Grupo ainda não tiver sido criado,
    o que não deveria acontecer, já que esse grupo é criado após os migrates.
    """
    g, c = Group.objects.get_or_create(name="Admin")
    if c:
        give_admin_group_permissions()
    return g


def give_admin_group_permissions():
    pass


def create_aluno_user(username, senha, turma, nome, num=0) -> User:
    u = create_user(username, senha)
    p = u.profile_escola
    p.is_aluno = True
    p.save()
    a = Aluno()
    a.user = u
    a.turma = turma
    a.nome = nome
    a.chamada = num
    a.save()
    assign_role(u, 'aluno')
    return u


def alunos_group_assert_permission():
    pass


def get_all_alunos_group():
    g, created = Group.objects.get_or_create(name='Todos_Alunos')
    if created:
        alunos_group_assert_permission()
    return g


def get_turma_alunos_group(turma_pk):
    g, created = Group.objects.get_or_create(name=f'Alunos_{turma_pk}')
    return g


def create_professor_user(username, password, name):
    u = create_user(username, password)
    assign_role(u, 'professor')
    p = u.profile_escola
    p.is_professor = True
    p.save()
    P = Professor()
    P.user = u
    P.nome = name
    P.save()
    return u


def get_all_professor_group():
    g, created = Group.objects.get_or_create(name='Todos_Professor')
    return g
