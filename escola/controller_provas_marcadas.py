#  Developed by Vinicius José Fritzen
#  Last Modified 20/05/19 14:36.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import logging
from calendar import HTMLCalendar, LocaleHTMLCalendar
from datetime import date
from typing import List

from django.contrib.auth.models import User
from django.utils import timezone

from escola.models import Turma, Professor, MateriaDaTurma, ProvaMateriaMarcada, ProvaAreaMarcada, EventoTurma

logger = logging.getLogger(__name__)


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


def get_professors(list_materias: List[MateriaDaTurma]):
    professores = []
    for mat in list_materias:
        professores.append(mat.get_professor())
    return professores


def get_provas_professor_futuras(professor, qnt=0):
    a = [a for a in ProvaMateriaMarcada.objects.all() if professor in get_professors(a.get_materias()) and a.get_data() > timezone.now()]
    a += [a for a in ProvaAreaMarcada.objects.all() if professor in get_professors(a.get_materias()) and a.get_data() > timezone.now()]
    logger.info(f"Coletou {len(a)} provas")
    a = sort_provas(a)
    if qnt > 0:
        return a[:qnt]
    return a


class CalendarioDatasLivresTurma(HTMLCalendar):
    DEFAULT_COLOR = '#ffffff'
    OCUPADO_COLOR = "#ff9e9e"
    INVALID_COLOR = "#a3a3a3"

    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(CalendarioDatasLivresTurma, self).__init__(firstweekday=6)

    def formatday(self, day, events):
        events_per_day: List[EventoTurma] = events.filter(evento__data__day=day)
        d = ''
        background_color = self.DEFAULT_COLOR
        for event in events_per_day:
            d += f'<li> {event.get_nome()} </li>'
            if event.block_prova:
                background_color = self.OCUPADO_COLOR

        if day != 0:
            return f"<td style='background-color: {background_color};'><span class='date'>{day}</span><ul> {d} </ul></td>"
        return f"<td style='background-color: {self.INVALID_COLOR};'></td>"

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    def formatmonth(self, turma, withyear=True, ):
        events = EventoTurma.objects.filter(evento__data__year=self.year, evento__data__month=self.month, turma=turma)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal
