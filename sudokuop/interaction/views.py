from django.shortcuts import render
from django.http import JsonResponse
from .models import Game, User, Player

# Create your views here.
def create_game(request):
    if request.method == 'POST':
        data = request.POST
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
        return JsonResponse({}, status=200)
    return JsonResponse({"error": "invalid request method"}, status=403)

#get game info for user
def game_info(request):
    if request.method == 'GET':
        players = Player.objects.filter(user=request.user)
        active_games = []
        for player in players:
            active_games.append(player.game.id)
        return JsonResponse({"games": active_games}, status=200)
    return JsonResponse({"error": "invalid request method"}, status=403)