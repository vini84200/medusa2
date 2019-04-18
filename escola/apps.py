#  Developed by Vinicius José Fritzen
#  Last Modified 17/04/19 23:16.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

from django.apps import AppConfig


class EscolaConfig(AppConfig):
    name = 'escola'

    def ready(self):
        from django.db.models.signals import post_migrate
        from .signals import populate_models
        post_migrate.connect(populate_models, sender=self)
