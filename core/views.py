from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from decouple import config
import requests
from django.http import JsonResponse


# Create your views here.
def home(request):
    return render(request, 'home.html')

def home(request):
    api_key = config('RAWG_API_KEY')
    params = {
        'key': api_key,
        'page_size': 8,    # cuantos juegos quieres en el home
        'page': 1,
        'ordering': '-rating',
    }
    resp = requests.get('https://api.rawg.io/api/games', params=params)
    juegos = resp.json().get('results', [])
    return render(request, 'home.html', {
        'juegos':    juegos,
        'next_page': 2,
    })

def game_detail(request, slug):
    api_key = config('RAWG_API_KEY')
    url = f'https://api.rawg.io/api/games/{slug}'
    params = {'key': api_key}
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        # podrías mostrar 404 o un mensaje de error
        return render(request, '404.html', status=404)

    juego = resp.json()
    # juego ahora contiene descripción, géneros, trailers, etc.

    return render(request, 'game.html', {
        'juego': juego
    })

def privacy_policy(request):
    return render(request, 'privacidad.html')

def cerrar_sesion(request):
    logout(request)
    return redirect('home')

def session_status(request):
    if request.user.is_authenticated:
        return JsonResponse({'active': True})
    return JsonResponse({'active': False})