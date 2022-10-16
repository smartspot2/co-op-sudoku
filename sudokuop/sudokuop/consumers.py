from channels.consumer import WebsocketConsumer
from random import randint
from time import sleep

class GameConsumer(WebsocketConsumer):

    def connect(self):
        # when websocket connects
        print("connected")
        self.send({"type": "websocket.accept",
                         })

        self.send({"type":"websocket.send",
                         "text":0})


    def receive(self):
        # when messages is received from websocket
        print("receive")
        self.send({"type": "websocket.send",
                         "text":str(randint(0,100))})

    def disconnect(self):
        # when websocket disconnects
        print("disconnected",)