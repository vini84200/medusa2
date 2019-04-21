#  Developed by Vinicius José Fritzen
#  Last Modified 21/04/19 16:00.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

from django.conf import settings

def google_analytics(*args, **kwargs):
    """Retorna chave do google analytics"""
    if settings.GA_TRACKING_ID:
        return {'GA_TRACKING_ID': settings.GA_TRACKING_ID}
    else:
        return dict()