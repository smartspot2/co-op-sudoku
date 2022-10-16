from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse
from .models import Game, User, Player

import json


def create_game(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        teammate_usernames = data.get("usernames")
        #TODO: integrate board generation
        new_game = Game(board="")
        new_game.save()
        #TODO: add board mask
        player = Player(user=request.user, game=new_game, visibility_mask="")
        player.save()
        for username in teammate_usernames:
            user = User.objects.get(username=username)
            if not user:
                continue
            #TODO: add board mask
            teammate = Player(user=user, game=new_game, visibility_mask="")
            teammate.save()
        return JsonResponse({"id": new_game.id}, status=200)
    return JsonResponse({"error": "invalid request method"}, status=401)

#get game info for user
def game_info(request):
    if request.method == 'GET':
        user = request.user
        print(user, dir(user))
        players = user.player_set.all()
        print(players)
        active_games = []
        for player in players:
            active_games.append(player.game.id)
        return JsonResponse({"games": active_games}, status=200)
    return JsonResponse({"error": "invalid request method"}, status=401)

# LOGIN

def login_user(request):
    """
    POST /api/login {username: username}
    """
    body = json.loads(request.body)
    username = body.get("username", "")
    if username == "":
        return JsonResponse({"error": "Invalid username"}, status=401)

    filtered_user = User.objects.filter(username=username)
    if filtered_user.exists():
        user = User.objects.get(username=username)
        user.backend = "django.contrib.auth.backends.ModelBackend"
        login(request, user)
        return JsonResponse({}, status=200)
    else:
        return JsonResponse({"error": "User not found."}, status=403)


def register_user(request):
    """
    POST /api/register {username: username}
    """
    body = json.loads(request.body)
    username = body.get("username", "")
    if username == "":
        return JsonResponse({"error": "Invalid username"}, status=401)
    user, _ = User.objects.get_or_create(username=username)
    user.backend = "django.contrib.auth.backends.ModelBackend"
    user.save()
    login(request, user)
    return JsonResponse({}, status=200)
