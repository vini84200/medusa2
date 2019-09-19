#  Developed by Vinicius José Fritzen
#  Last Modified 12/04/19 13:19.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

from django.contrib import admin

from .models import *

admin.site.register(Turma)
admin.site.register(MateriaDaTurma)
admin.site.register(Horario)
admin.site.register(Turno)
admin.site.register(Periodo)
admin.site.register(TurnoAula)
admin.site.register(Tarefa)
admin.site.register(TarefaComentario)
admin.site.register(Notificacao)
admin.site.register(Conteudo)
admin.site.register(CategoriaConteudo)
admin.site.register(LinkConteudo)
# Prova Marcada Register
admin.site.register(AreaConhecimento)
admin.site.register(Evento)
admin.site.register(EventoTurma)
admin.site.register(EventoEscola)
admin.site.register(ProvaMarcada)
admin.site.register(ProvaMateriaMarcada)
admin.site.register(ProvaAreaMarcada)
