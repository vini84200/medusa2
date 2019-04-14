#  Developed by Vinicius José Fritzen
#  Last Modified 13/04/19 22:45.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

import logging

logger = logging.getLogger(__name__)

INITIAL_GROUPS = {
    'Admin': ['perm'],
    'Todos_Alunos': [],
}

def populate_models(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission

    logger.info("Iniciando modulo, para adição de Itens pós migrate.")
    logger.info("Iniciando verificação de grupos:")
    for g in INITIAL_GROUPS.keys():
        group, created = Group.objects.get_or_create(name=g)
        if created:
            logger.info(f"Criado grupo {g}.")
        else:
            logger.info(f"Grupo {g} já existe.")



