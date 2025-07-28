from django.urls import path
from .views import juegos_populares

urlpatterns = [
    path('list/', juegos_populares, name='list-games')
]
