from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(Turma)
admin.site.register(Professor)
admin.site.register(MateriaDaTurma)
admin.site.register(Aluno)
admin.site.register(ProvaBase)
admin.site.register(ProvaAplicada)
admin.site.register(Horario)
admin.site.register(Turno)