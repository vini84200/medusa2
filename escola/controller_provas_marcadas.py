#  Developed by Vinicius José Fritzen
#  Last Modified 20/05/19 14:36.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import logging
from datetime import date
from typing import List

from django.contrib.auth.models import User
from django.utils import timezone

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

def get_data_for_sort(prova):
    return prova.get_data()


def sort_provas(provas: List):
    provas.sort(key=get_data_for_sort)
    return provas


def get_provas_turma_futuras(turma: Turma, qnt=0):
    a = [(a) for a in ProvaMateriaMarcada.objects.all() if a.get_turma() == turma and a.get_data() > timezone.now()]
    a += [(a) for a in ProvaAreaMarcada.objects.all() if a.get_turma() == turma and a.get_data() > timezone.now()]
    logger.info(f"Coletou {len(a)} provas")
    a = sort_provas(a)
    if qnt > 0:
        return a[:qnt]
    return a