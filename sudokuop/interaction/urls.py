from django.urls import path
from . import views

urlpatterns = [
    path("game/create/", views.create_game, name='game-create'),
    path("game/info/", views.game_info, name="game-detail"),
    path("login/", views.login_user, name="login"),
    path("register/", views.register_user, name="register")
]
