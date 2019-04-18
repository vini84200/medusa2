"""Mantem funções para criar usuarios, e seus grupos padrões."""
#  Developed by Vinicius José Fritzen
#  Last Modified 14/04/19 16:12.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import logging

from django.contrib.auth.models import User, Group

from escola.models import Profile, Aluno, Professor, Turma

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
    u = User.objects.create_user(username, password=password, email=kwargs.get('email'))
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
    user = User.objects.create_user(username, password=password, email=kwargs.get('email'))
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
        logger.warning("Por algum motivo o Grupo admin não havia sido criado.")
    return g


def create_aluno_user(username, senha, turma: Turma, nome, *args, **kwargs):
    """
    Cria um usuario como aluno
    :param username: Nome de usuario
    :param senha: senha
    :param turma: Turma do aluno
    :param nome: Nome completo do aluno
    :keyword n_chamda: Numero da chmada do aluno.
    :return:
    """
    u = create_user(username, senha)
    p = u.profile_escola
    p.is_aluno = True
    p.save()
    a = Aluno()
    a.user = u
    a.turma = turma
    a.nome = nome
    if kwargs.get('n_chamda'):
        a.chamada = kwargs.get('n_chamda')
    a.save()
    u.groups.add(get_all_alunos_group())
    u.groups.add(get_turma_alunos_group(turma.pk))
    return u


def get_all_alunos_group():
    g, created = Group.objects.get_or_create(name='Todos_Alunos')
    return g


def get_turma_alunos_group(turma_pk):
    g, created = Group.objects.get_or_create(name=f'Alunos_{turma_pk}')
    return g


def create_professor_user(username, password, name):
    u = create_user(username, password)
    p = u.profile_escola
    p.is_professor = True
    u.groups.add(get_all_professor_group())
    P = Professor()
    P.user = u
    P.nome = name
    return u


def get_all_professor_group():
    g, created = Group.objects.get_or_create(name='Todos_Professor')
    return g