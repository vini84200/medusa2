import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Sessao

class PainelPresencaConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        #await self.send({
        #    "type":"websocket.accept"
        #})
        if Sessao.there_is_sessao_hoje():
            sessao = Sessao.sessao_hoje().first()
            self.sessao_channel = f"presenca_ses_{sessao.id}"
            print(self.sessao_channel)
            await self.channel_layer.group_add(
                self.sessao_channel,
                self.channel_name
            )
            self.send(
                {"type":"websocket.accept"}
            )


    async def websocket_receive(self, event):
        print("Received ", event)

    async def websocket_disconnect(self, event):
        print("Disconnected ", event)