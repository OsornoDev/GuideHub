// juegos.js

    document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);

    // Mapa texto → clave de filtro
    const mapFiltro = {
        'Todos':               'all',
        'Recientes':           'recientes',
        'Mejor Valorados':     'mejores',
        'Próximos Lanzamientos':'upcoming'
    };

    // --- FILTROS ---
    document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
            // marca activo
            document.querySelectorAll('.filter-btn')
                    .forEach(b => b.classList.replace('btn-primary','btn-outline-primary'));
            btn.classList.replace('btn-outline-primary','btn-primary');

            const label = btn.textContent.trim();
            params.set('filter', mapFiltro[label] || 'all');
            params.set('page', '1');
            window.location.search = params.toString();
            });
        });

  // --- BUSCADOR (Enter) ---
    const inputSearch = document.querySelector('input[placeholder="Buscar juegos..."]');
    inputSearch.value = params.get('search') || '';
    inputSearch.addEventListener('keypress', e => {
        if (e.key === 'Enter') {
        params.set('search', inputSearch.value.trim());
        params.set('page', '1');
        window.location.search = params.toString();
        }
    });

    // --- ORDENAMIENTO ---
    const selectOrd = document.querySelector('select.form-select');
    selectOrd.value = params.get('ordering') || '-rating';
    selectOrd.addEventListener('change', () => {
        params.set('ordering', selectOrd.value);
        params.set('page', '1');
        window.location.search = params.toString();
    });

    // --- PAGINACIÓN ---
document.querySelectorAll('.page-link').forEach(link => {
        link.addEventListener('click', e => {
        const num = parseInt(link.textContent);
        if (!isNaN(num)) {
            params.set('page', num);
            window.location.search = params.toString();
        }
        e.preventDefault();
        });
    });
    });
