#  Developed by Vinicius José Fritzen
#  Last Modified 25/04/19 17:13.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import logging

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User

from escola.models import CargoTurma

logger = logging.getLogger(__name__)


def username_present(username):
    if User.objects.filter(username=username).exists():
        return True

    return False


def dar_permissao_user(ocupante, cargo: CargoTurma):
    logger.info(f"Dando permissões para user {ocupante}, do cargo {cargo},"
                f" que possui nivel {cargo.cod_especial}, na turma {cargo.turma}")
    if cargo.cod_especial == 1:
        # PERMISSÔES DE LIDER
        logger.info(f"Permissão de lider")
        cargo.turma.lider = ocupante
        cargo.turma.save()
        logger.info(f"Agora o lider é {cargo.turma.lider}")
    if cargo.cod_especial == 2:
        # PERMISSÔES DE VICELIDER
        logger.info(f"Permissão de vicelider")
        cargo.turma.vicelider = ocupante
        cargo.turma.save()
        logger.info(f"Agora o vicelider é {cargo.turma.vicelider}")
    if cargo.cod_especial == 5:
        # PERMISSÔES DE REGENTE
        logger.info(f"Permissão de regente")
        cargo.turma.regente = ocupante
        cargo.turma.save()
        logger.info(f"Agora o regente é {cargo.turma.regente}")


def genarate_password():
    senha = BaseUserManager().make_random_password(length=8,
                                                   allowed_chars='abcdefghjkmnpqrstuvwxyz23456789')
    return senha


def generate_username(nome):
    # Cria a base do username a partir do primeiro nome
    username = nome.split(' ')[0].lower() + "."
    # Adiciona as iniciais depois do ponto
    for n in nome.split(' '):
        if n[0]:
            username += n[0].lower()
    # Verifica se já foi usado, caso positivo, vai adicionando numeros até o certo
    a = 0
    usernameTeste = username
    while username_present(usernameTeste):
        a += 1
        usernameTeste = username + a.__str__()
    username = usernameTeste
    return username