#  Developed by Vinicius José Fritzen
#  Last Modified 20/05/19 14:36.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import logging
from datetime import date

from django.contrib.auth.models import User

from escola.models import Turma, Professor, MateriaDaTurma, ProvaMateriaMarcada, ProvaAreaMarcada

logger = logging.getLogger(__name__)


def get_dia_eventos(dia: date, user: User):
    """Return the eventos for any given dia for User """
    pass


def get_dia_color(dia: date, turma: Turma):
    """Return the hex code for the color of the day"""
    pass


def has_a_prova_in_day(dia: date, turma: Turma):
    """Return a bool if the given day has a prova for turma"""
    pass


def get_materias_professor_for_day(professor: Professor, dia: date):
    """Return a list of materias of the professor for today"""
    return MateriaDaTurma.helper.filter_from_professor_for_day(professor, dia)


def get_provas_turma(turma: Turma):
    a = [a if a.get_turma() == turma else None for a in ProvaMateriaMarcada.objects.all()]
    a += [a if a.get_turma() == turma else None for a in ProvaAreaMarcada.objects.all()]
    logger.info(f"Coletou {len(a)} provas")
    return a
