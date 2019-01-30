import asyncio
import json
from django.contrib.auth import get_user_model
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Sessao

class PainelPresencaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connected")
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
            await self.accept()
        else:
            print('No session')


    async def websocket_receive(self, event):
        print("Received ", event)

    async def ses_regPresenca(self, event):
        print(f"Presenca: {event}")
        self.send(text_data=json.dumps({
            'type': "websocket.receive",
            'text' : json.dumps({'type': 'regPresenca', 'user': event['user']})
        }))

    async def websocket_disconnect(self, event):
        print("Disconnected ", event)
class RegistraPresencaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connected")
        #await self.send({
        #    "type":"websocket.accept"
        #})
        if Sessao.there_is_sessao_hoje():
            sessao = self.scope['url_route']['kwargs']['sessao']
            self.sessao_channel = f"presenca_ses_{sessao}"
            print(self.sessao_channel)
            await self.channel_layer.group_add(
                self.sessao_channel,
                self.channel_name
            )
            await self.accept()
        else:
            print('No session')


    async def websocket_receive(self, event):
        print("Received ", event)

    async def websocket_disconnect(self, event):
        print("Disconnected ", event)