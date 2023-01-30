from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
import json

class Hall(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        if user.is_authenticated:
            await self.accept()
            self.user = user
            self.room_name = "hall-01"
            await self.channel_layer.group_add(self.room_name, self.channel_name)
            await self.channel_layer.group_add("notification_%d" % self.user.id, self.channel_name)
            cache.set("notification_%d" % self.user.id, self.channel_name, 5 * 60)
            print('accept')
        else:
            await self.close()


    async def disconnect(self, close_code):
        if hasattr(self, 'room_name') and self.room_name:
            await self.channel_layer.group_discard(self.room_name, self.channel_name)
            await self.channel_layer.group_discard("notification_%d" % self.user.id, self.channel_name)
            cache.delete("notification_%d" % self.user.id)

    async def group_send_event(self, data):
        await self.send(text_data=json.dumps(data))

    async def send_hall_message(self, data):
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': "group_send_event",
                'event': "hall_message",
                'msg': {
                    'userId': data['userId'],
                    'username': data['username'],
                    'photo': data['photo'],
                    'text': data['text'],
                }
            }
        )

    async def send_heartbeat(self, data):
        cache.set("notification_%d" % data['userId'], self.channel_name, 5 * 60)

    async def receive(self, text_data):
        data = json.loads(text_data)
        event = data['event']
        if event == 'hall_message':
            await self.send_hall_message(data)
        elif event == 'heartbeat':
            await self.send_heartbeat(data)
