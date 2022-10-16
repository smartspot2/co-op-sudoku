from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from random import randint
from time import sleep
import json

from interaction.models import Game, Player

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
        self.user = self.scope["user"]
        data = json.loads(text_data)
        if data["type"] == "START":
            # Send message to user
            game = Game.objects.get(id=self.game_id)
            board = game.board
            candidates = game.candidates
            player = Player.objects.get(game=game, user=self.user)

            async_to_sync(self.channel_layer.send)(
                self.channel_name, {"type": "game_init", "board": board, "candidates": candidates, "view": player.visibility_mask}
            )

        elif data["type"] == "UPDATE":
            board = data["board"]
            candidates = data["candidates"]

            game = Game.objects.get(id=self.game_id)
            game.board = board
            game.candidates = candidates
            game.save()

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.game_group_name, {"type": "game_move", "board": board, "candidates": candidates}
            )


    def disconnect(self):
        # when websocket disconnects
        print("disconnected",)
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name, self.channel_name
        )

    def game_init(self, event):
        board = json.loads(event["board"])
        candidates = json.loads(event["candidates"])
        view = json.loads(event["view"])
        self.send(text_data=json.dumps({"type": "INIT", "board": board, "candidates": candidates, "view": view}))

    # Receive message from game group
    def game_move(self, event):
        board = event["board"]
        candidates = event["candidates"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"board": board, "candidates": candidates}))