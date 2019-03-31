from django.contrib import admin

from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _

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


# Define a new FlatPageAdmin
class FlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': (
                'enable_comments',
                'registration_required',
                'template_name',
            ),
        }),
    )


# Re-register FlatPageAdmin
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
