from channels.routing import ProtocolTypeRouter, URLRouter

from django.conf.urls import url
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from voting.consumers import PainelPresencaConsumer

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket':AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    url('presenca/tela/', PainelPresencaConsumer),
                ]
            )
        )
    )
})