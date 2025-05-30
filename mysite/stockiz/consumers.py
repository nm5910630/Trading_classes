import json
import yfinance as yf
from channels.generic.websocket import AsyncWebsocketConsumer

class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.symbol = self.scope['url_route']['kwargs']['symbol']
        self.group_name = f'stock_{self.symbol}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # When we receive a message from client, send updated stock data
        stock = yf.Ticker(self.symbol)
        hist = stock.history(period='1d')
        
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'stock_update',
                'data': {
                    'price': round(hist['Close'].iloc[-1], 2),
                    'change': round(hist['Close'].pct_change().iloc[-1] * 100, 2),
                    'volume': hist['Volume'].iloc[-1]
                }
            }
        )

    async def stock_update(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event['data']))