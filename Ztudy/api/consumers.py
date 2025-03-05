import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room

from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Lấy code_invite từ URL
        self.code_invite = self.scope['url_route']['kwargs']['code_invite']

        # Kiểm tra xem room có tồn tại không
        try:
            self.room = await sync_to_async(self.get_room)(self.code_invite)
            self.room_group_name = f'chat_{self.room.id}'  # Dùng ID của room làm group name
        except Room.DoesNotExist:
            # Nếu room không tồn tại, đóng kết nối WebSocket
            await self.close()

        # Tham gia vào group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()  # Chấp nhận kết nối WebSocket

    async def disconnect(self, close_code):
        # Thoát khỏi room group khi kết nối WebSocket ngắt
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Nhận tin nhắn từ WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Gửi tin nhắn tới group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Nhận tin nhắn từ group và gửi tới WebSocket
    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

    # Method to fetch room (synchronous)
    def get_room(self, code_invite):
        return Room.objects.get(code_invite=code_invite)
