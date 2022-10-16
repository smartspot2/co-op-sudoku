from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse
from .models import Game, User, Player

from sudoku.sudoku.sudoku_numpy import Game as SudokuGame

import json


def create_game(request):
    '''
    create new game and create player objects for user and teammates
    '''
    if request.method == 'POST':
        data = json.loads(request.body)
        teammate_usernames = []
        for username in data.get("usernames"):
            user = User.objects.get(username=username)
            if not user:
                print(f"{username} is not a user")
                continue
            teammate_usernames.append(username)
        sudoku_game = SudokuGame.generate_new(len(teammate_usernames) + 1)
        serialized_game = sudoku_game.serialize_game()
        print(serialized_game)
        game_object = Game(board=serialized_game['board'])
        game_object.save()
        player = Player(user=request.user, game=game_object, visibility_mask=serialized_game['views'][0])
        player.save()
        for username, mask in zip(teammate_usernames, serialized_game['views'][1:]):
            user = User.objects.get(username=username)
            teammate = Player(user=user, game=game_object, visibility_mask=mask)
            teammate.save()
        return JsonResponse({"id": game_object.id}, status=200)
    return JsonResponse({"error": "invalid request method"}, status=401)


def game_info(request):
    '''
    get game id's associated with user
    '''
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
