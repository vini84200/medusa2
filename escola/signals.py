# ADMIN_LIST_PERMISSIONS =

#  Developed by Vinicius José Fritzen
#  Last Modified 13/04/19 18:39.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

import logging

logger = logging.getLogger(__name__)

def populate_models(sender, **kwargs):
    from django.apps import apps
    from .apps import EscolaConfig
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType

    logger.info("Iniciando modulo, para adição de Itens pós migrate.")
    logger.info("Iniciando verificação de grupos:")
    admin_group, created = Group.objects.get_or_create(name="Admin")
    if created:
        logger.info("Criado grupo ADMIN")
    else:
        logger.info("Grupo ADMIN já existe.")


