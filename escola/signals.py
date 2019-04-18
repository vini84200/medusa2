#  Developed by Vinicius José Fritzen
#  Last Modified 17/04/19 16:41.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

import logging


logger = logging.getLogger(__name__)

INITIAL_GROUPS = {
    'Admin': [
              'escola.add_turma',
              'escola.add_aluno',
              'escola.can_add_aluno',
              'escola.mudar_horario',
              'escola.can_populate_turma',
              ],
    'Todos_Alunos': [],
}


def populate_models(sender, **kwargs):
    from django.apps import apps
    from django.contrib.auth.management import create_permissions

    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, verbosity=0)
        app_config.models_module = None

    from django.contrib.auth.models import Group, Permission
    from escola.permission_utils import permission_names_to_objects

    logger.info("Iniciando modulo, para adição de Itens pós migrate.")
    logger.info("Iniciando verificação de grupos:")
    for g in INITIAL_GROUPS.keys():
        group, created = Group.objects.get_or_create(name=g)
        if created:
            logger.info(f"Criado grupo {g}.")
        else:
            logger.info(f"Grupo {g} já existe.")

        logger.info(f"Iniciando metodo de dar Permissões para o grupo {g}")
        logger.debug(f"Permissões a serem dadas:{INITIAL_GROUPS[g]}")
        perms_to_add = permission_names_to_objects(INITIAL_GROUPS[g])
        logger.info(f"Dando permissões {perms_to_add.__str__()} para o grupo {g}")
        group.permissions.add(*perms_to_add)
        if not created:
            # Group already existed - make sure it doesn't have any perms we didn't want
            to_remove = set(group.permissions.all()) - set(INITIAL_GROUPS[g])
            # if to_remove:
            #     logger.warning(f"Retirando a(s) permissão(ões):{to_remove}")
            #     group.permissions.remove(*to_remove)



