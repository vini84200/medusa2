#  Developed by Vinicius José Fritzen
#  Last Modified 13/04/19 18:13.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

from django.apps import AppConfig
from django.db.models.signals import post_migrate

class EscolaConfig(AppConfig):
    name = 'escola'

    def ready(self):
        from .signals import populate_models
        post_migrate.connect(populate_models, sender=self)
