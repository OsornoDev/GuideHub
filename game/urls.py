from django.urls import path
from .views import juegos_populares, game_detail

urlpatterns = [
    path('list/', juegos_populares, name='list-games'),
    path('juegos/<slug:slug>/', game_detail, name='game-detail'),
]
