#  Developed by Vinicius José Fritzen
#  Last Modified 28/04/19 11:42.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

import logging

from escola.models import Turno

logger = logging.getLogger(__name__)


def populate_models(sender, **kwargs):
    # Cria turnos
    logger.info("Iniciando Verificações de turnos, e sua reposiçãp")
    if not Turno.objects.filter(cod=1).all():
        logger.info("Nenhum Turno 1 encontrado, criando...")
        matutino = Turno()
        matutino.nome = "Matutino"
        matutino.cod = 1
        matutino.save()

    if not Turno.objects.filter(cod=2).all():
        logger.info("Nenhum Turno 2 encontrado, criando...")
        turno = Turno()
        turno.nome = "Tarde"
        turno.cod = 2
        turno.save()

    if not Turno.objects.filter(cod=3).all():
        logger.info("Nenhum Turno 3 encontrado, criando...")
        turno = Turno()
        turno.nome = "Noturno"
        turno.cod = 3
        turno.save()




