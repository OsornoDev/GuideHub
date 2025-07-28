# views.py

from django.shortcuts import render
import requests
from decouple import config
from datetime import date, timedelta

def juegos_populares(request):
    api_key  = config('RAWG_API_KEY')
    q        = request.GET.get('search', '').strip()
    ordering = request.GET.get('ordering', '-rating')
    filtro   = request.GET.get('filter', 'all')
    page     = request.GET.get('page', '1')

    params = {
        'key': api_key,
        'page_size': 20,
        'page': page,
        'ordering': ordering,
    }
    if q:
        params['search'] = q

    hoy = date.today()
    if filtro == 'recientes':
        hace_3m = hoy - timedelta(days=90)
        params['dates'] = f"{hace_3m.isoformat()},{hoy.isoformat()}"
        params['ordering'] = '-released'
    elif filtro == 'upcoming':
        dentro_6m = hoy + timedelta(days=180)
        params['dates'] = f"{hoy.isoformat()},{dentro_6m.isoformat()}"
        params['ordering'] = 'released'
    # 'all' y 'mejores' usan ordering por defecto

    try:
        resp = requests.get('https://api.rawg.io/api/games', params=params)
        resp.raise_for_status()
        data = resp.json()
        juegos = data.get('results', [])
        total = data.get('count', 0)
    except Exception as e:
        print("Error RAWG:", e)
        juegos, total = [], 0

    return render(request, 'juegos.html', {
        'juegos': juegos,
        'search':  q,
        'ordering': ordering,
        'filter':   filtro,
        'page':     int(page),
        'total':    total,
    })
