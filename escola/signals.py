#  Developed by Vinicius José Fritzen
#  Last Modified 25/04/19 13:51.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

import logging

logger = logging.getLogger(__name__)

INITIAL_GROUPS = {
    'Admin': ['perm'],
    'Todos_Alunos': [],
}

def populate_models(sender, **kwargs):
    pass



