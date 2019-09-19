from django.contrib import admin

from users.models import Profile, Aluno, Professor
# Register your models here.

admin.site.register(Aluno)
admin.site.register(Professor)
admin.site.register(Profile)
