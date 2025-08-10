# game/views.py
from django.shortcuts import render
import requests
from decouple import config
from datetime import date, timedelta
from math import ceil

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

def juegos_populares(request):
    api_key  = config('RAWG_API_KEY')
    q        = request.GET.get('search', '').strip()
    ordering = request.GET.get('ordering', '-rating')
    filtro   = request.GET.get('filter', 'all')

    # 1. Parseo seguro del parámetro page
    page_str = request.GET.get('page', '').strip()
    try:
        page = int(page_str)
        if page < 1:
            page = 1
    except (ValueError, TypeError):
        page = 1

    # 2. Configura parámetros para RAWG
    params = {
        'key':       api_key,
        'page_size': 20,
        'page':      page,
        'ordering':  ordering,
    }
    if q:
        params['search'] = q

    # Filtros de fechas
    hoy = date.today()
    if filtro == 'recientes':
        hace_3m = hoy - timedelta(days=90)
        params['dates']    = f"{hace_3m.isoformat()},{hoy.isoformat()}"
        params['ordering'] = '-released'
    elif filtro == 'upcoming':
        dentro_6m = hoy + timedelta(days=180)
        params['dates']    = f"{hoy.isoformat()},{dentro_6m.isoformat()}"
        params['ordering'] = 'released'

    # 3. Llama a RAWG
    try:
        resp = requests.get('https://api.rawg.io/api/games', params=params)
        resp.raise_for_status()
        data        = resp.json()
        juegos      = data.get('results', [])
        total_count = data.get('count', 0)
    except Exception as e:
        print("Error RAWG API:", e)
        juegos      = []
        total_count = 0

    # 4. Calcula total_pages
    total_pages = ceil(total_count / params['page_size']) if total_count else 1

    # 5. Genera ventana deslizante de páginas (tamaño 5)
    window_size = 5
    half_window = window_size // 2

    start = max(1, page - half_window)
    end   = start + window_size - 1
    if end > total_pages:
        end   = total_pages
        start = max(1, end - window_size + 1)

    page_window = list(range(start, end + 1))

    # 6. Renderiza plantilla con contexto completo
    return render(request, 'juegos.html', {
        'juegos':       juegos,
        'search':       q,
        'ordering':     ordering,
        'filter':       filtro,
        'page':         page,
        'total':        total_count,
        'total_pages':  total_pages,
        'page_window':  page_window,
        # Para el botón “Ver más juegos”
        'next_page':    page + 1 if page < total_pages else total_pages,
    })
