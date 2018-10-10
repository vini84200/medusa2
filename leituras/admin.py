from django.contrib import admin
from .models import Autor, Livro, Leitura, Editora, Serie, Leitura_Update
# Register your models here.
admin.site.register(Autor)
admin.site.register(Livro)
admin.site.register(Leitura)
admin.site.register(Editora)
admin.site.register(Serie)
admin.site.register(Leitura_Update)