#  Developed by Vinicius José Fritzen
#  Last Modified 21/04/19 16:00.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest


logger = logging.getLogger(__name__)

def google_analytics(*args, **kwargs):
    """Retorna chave do google analytics"""
    if settings.GA_TRACKING_ID:
        return {'GA_TRACKING_ID': settings.GA_TRACKING_ID}
    else:
        return dict()

def warnings(request: HttpRequest):
    """Adiciona alguns avisos no content"""
    warning = list()
    if hasattr(request, 'user'):
        user: User = request.user
        if not user.is_anonymous:
            # Testa email
            if user.email is None or user.email == "":
                warning.append({
                    'message': 'Você não possui um e-mail registrado, por favor registre um',
                    'link_page_name': 'escola:self-email-change'
                })
    else:
        logger.info("Não há atributo user")

    return {'warnings': warning}
