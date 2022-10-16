from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Game(models.Model):
    board = models.CharField(max_length=500)


class User(AbstractUser):
    pass


class Player(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    game = models.ForeignKey(
        "Game", null=True, blank=True, on_delete=models.CASCADE)
    visibility_mask = models.CharField(max_length=500)
