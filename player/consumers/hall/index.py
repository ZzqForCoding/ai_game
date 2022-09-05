from channels.generic.websocket import AsyncWebsocketConsumer
import json

class Hall(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        if user.is_authenticated:
            await self.accept()
            self.user = user
            self.room_name = "hall-01"
            await self.channel_layer.group_add(self.room_name, self.channel_name)
            print('accept')
        else:
            await self.close()


    async def disconnect(self, close_code):
        if hasattr(self, 'room_name') and self.room_name:
            await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def group_send_event(self, data):
        await self.send(text_data=json.dumps(data))

    async def send_hall_message(self, data):
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': "group_send_event",
                'event': "hall_message",
                'msg': {
                    'username': data['username'],
                    'photo': data['photo'],
                    'text': data['text'],
                }
            }
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        event = data['event']
        if event == 'hall_message':
            await self.send_hall_message(data)
