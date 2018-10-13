from django.contrib import admin
from .models import TipoMocao, Mocao, Cargo, Cadeira, CasaVotante, Votacao, Sessao, TipoSesao, Presenca

admin.site.register(TipoMocao)
admin.site.register(Mocao)
admin.site.register(Cargo)
admin.site.register(Cadeira)
admin.site.register(CasaVotante)
admin.site.register(Votacao)
admin.site.register(Sessao)
admin.site.register(TipoSesao)
admin.site.register(Presenca)
