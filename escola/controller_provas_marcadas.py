#  Developed by Vinicius José Fritzen
#  Last Modified 20/05/19 14:36.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import logging
from calendar import HTMLCalendar
from datetime import date
from typing import List

from django.utils import timezone
from django.utils.html import escape

from escola.models import (EventoTurma, MateriaDaTurma,
                           ProvaAreaMarcada, ProvaMateriaMarcada, Turma,
                           Tarefa, EventoEscola)
from users.models import Professor

logger = logging.getLogger(__name__)


def get_materias_professor_for_day(professor: Professor, dia: date):
    """Return a list of materias of the professor for today"""
    return MateriaDaTurma.helper.filter_from_professor_for_day(professor, dia.isoweekday())


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
    cssclass_month_head = "month"
    WEEKDAYSABREVIADO = ["Seg",
                         "Ter",
                         "Qua",
                         "Qui",
                         "Sex",
                         "Sab",
                         "Dom"]

    WEEKDAYS = ["Segunda-feira",
                         "Terça-feira",
                         "Quarta-feira",
                         "Quinta-feira",
                         "Sexta-feira",
                         "Sábado",
                         "Domingo"]
    MONTH_NAMES = [
        "",
        "Janeiro",
        'Fevereiro',
        'Março',
        'Abril',
        'Maio',
        'Junho',
        'Julho',
        'Agosto',
        'Setembro',
        'Outubro',
        'Novembro',
        'Dezembro']

    MONTH_ABBRNAMES = ["Jan",
                       'Fev',
                       'Mar',
                       'Abr',
                       'Mai',
                       'Jun',
                       'Jul',
                       'Ago',
                       'Set',
                       'Out',
                       'Nov',
                       'Dez']

    DEFAULT_COLOR = '#ffffff'
    OCUPADO_COLOR = "#ff9e9e"
    INVALID_COLOR = "#a3a3a3"
    WEEKEND_COLOR = "#c3dbdb"

    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(CalendarioDatasLivresTurma, self).__init__(firstweekday=6)

    def formatweekday(self, day):
        """
        Return a weekday name as a table header.
        """
        return '<th scope="col" class="%s">%s</th>' % (
            self.cssclasses_weekday_head[day], self.WEEKDAYSABREVIADO[day])

    def formatmonthname(self, theyear, themonth, withyear=True):
        """
        Return a month name as a table row.
        """
        if withyear:
            s = '%s %s' % (self.MONTH_NAMES[themonth], theyear)
        else:
            s = '%s' % self.MONTH_NAMES[themonth]
        return '<caption class="%s">%s</caption>' % (
            self.cssclass_month_head, s)
    
    def formatweekheader(self):
        """
        Return a header for a week as a table row.
        """
        s = ''.join(self.formatweekday(i) for i in self.iterweekdays())
        return '<tr class="weekdays">%s</tr>' % s

    def formatday(self, day, events, weekday):
        events_per_day = events.filter(evento__data__day=day)
        # Pega o dia em formato de datetime.date
        if day != 0:
            dia_date = date(self.year, self.month, day)
        else:
            dia_date = None
        
        if dia_date == date.today():
            today_class = "date-today"
        else:
            today_class = "date"
        # Define o fundo para default ou weekend
        background_color = self.DEFAULT_COLOR
        if weekday == 6 or weekday == 5:
            background_color = self.WEEKEND_COLOR

        html_events = ''
        # Separa os eventos em que são provas e que não são
        eventos_nao_prova_da_turma = events_per_day.filter(prova__isnull=True)
        provas = events_per_day.filter(prova__isnull=False)

        eventos_escola = EventoEscola.objects.filter(evento__data__day=day,
         evento__data__month=self.month,
         evento__data__year=self.year)
        # Adiciona eventos da turmas
        for event in eventos_nao_prova_da_turma:
            html_events += f'<div class="event"><span class="badge badge-pill badge-success">E</span> {escape(event.get_nome())} </div>'
            if event.block_prova:
                background_color = self.OCUPADO_COLOR
        # Adiciona eventos da Escola
        for event in eventos_escola:
            html_events += f'<div class="event"><span class="badge badge-pill badge-success">E</span> {escape(event.get_nome())} </div>'
            if event.block_prova:
                background_color = self.OCUPADO_COLOR

        # Adicina Provas
        for event in provas:
            html_events += f'<div class="event"><span class="badge badge-pill badge-warning">P</span> {escape(event.get_nome())} </div>'
            if event.block_prova:
                background_color = self.OCUPADO_COLOR
        # Adiciona Tarefas
        if day != 0:
            tarefas = Tarefa.objects.filter(deadline=dia_date)
        else:
            tarefas = []
        for tarefa in tarefas:
            html_events += f'<div class="event"><span class="badge badge-pill badge-primary">T</span> {escape(tarefa.titulo)} </div>'

        # Gera HTML
        if day != 0:
            return f"<td class='day overflow-auto' style='background-color:"\
                   f"{background_color};'><div class='{today_class}'>{day}</div>{html_events}</td>"
        return f"<td class='day other-month' style='background-color: {self.INVALID_COLOR};'></td>"

    def formatweek(self, theweek, events=[]):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events, weekday)
        return f'<tr class="days"> {week} </tr>'

    def formatmonth(self, turma, withyear=True, ):
        events = EventoTurma.objects.filter(evento__data__year=self.year, evento__data__month=self.month, turma=turma)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" id="calendar" class="table">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal
