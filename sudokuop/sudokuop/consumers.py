from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from random import randint
from time import sleep
import json

from interaction.models import Game

class GameConsumer(WebsocketConsumer):

    def connect(self):
        # when websocket connects
        print("connected")
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.game_group_name = "group_%s" % self.game_id
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.game_group_name, self.channel_name
        )

        self.accept()

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        board = text_data_json["board"]
        candidates = text_data_json["candidates"]

        game = Game.objects.get(self.game_id)
        game.board = board
        game.candidates = candidates
        game.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "game_move", "board": board, "candidates": candidates}
        )


    def disconnect(self):
        # when websocket disconnects
        print("disconnected",)
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name, self.channel_name
        )

    # Receive message from game group
    def game_move(self, event):
        board = event["board"]
        candidates = event["candidates"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"board": board, "candidates": candidates}))