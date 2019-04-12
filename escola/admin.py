#  Developed by Vinicius José Fritzen
#  Last Modified 12/04/19 13:19.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

from django.contrib import admin

from .models import *

admin.site.register(Profile)
admin.site.register(Turma)
admin.site.register(Professor)
admin.site.register(MateriaDaTurma)
admin.site.register(Aluno)
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

