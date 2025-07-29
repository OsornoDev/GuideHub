document.addEventListener('DOMContentLoaded', () => {
    const params        = new URLSearchParams(window.location.search);
    const currentPage   = parseInt(params.get('page'))     || 1;
    const currentFilter = params.get('filter')             || 'all';
    const currentOrder  = params.get('ordering')           || '-rating';

    // Mapa texto → clave de filtro
    const mapFiltro = {
        'Todos':                 'all',
        'Recientes':             'recientes',
        'Mejor Valorados':       'mejores',
        'Próximos Lanzamientos': 'upcoming'
    };

    // ─── Iniciar filtros ─────────────────────────────────────
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('btn-primary','active');
        btn.classList.add('btn-outline-primary');
        const clave = mapFiltro[ btn.textContent.trim() ] || 'all';
        if (clave === currentFilter) {
        btn.classList.replace('btn-outline-primary','btn-primary');
        btn.classList.add('active');
        }
    });

    // ─── Click en filtros ────────────────────────────────────
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
        // UI
        document.querySelectorAll('.filter-btn')
            .forEach(b => b.classList.replace('btn-primary','btn-outline-primary') || b.classList.remove('active'));
        btn.classList.replace('btn-outline-primary','btn-primary');
        btn.classList.add('active');
        // params
        params.set('filter', mapFiltro[btn.textContent.trim()]);
        params.set('page', '1');
        window.location.search = params.toString();
        });
    });

    // ─── Buscador (Enter) ───────────────────────────────────
    const inputSearch = document.querySelector('#input-search');
    if (inputSearch) {
        inputSearch.value = params.get('search') || '';
        inputSearch.addEventListener('keydown', e => {
        if (e.key === 'Enter') {
            e.preventDefault();
            params.set('search', inputSearch.value.trim());
            params.set('page', '1');
            window.location.search = params.toString();
        }
        });
    }

    // ─── Ordenamiento ───────────────────────────────────────
    const selectOrd = document.querySelector('select.form-select');
    if (selectOrd) {
        selectOrd.value = currentOrder;
        selectOrd.addEventListener('change', () => {
        params.set('ordering', selectOrd.value);
        params.set('page', '1');
        window.location.search = params.toString();
        });
    }

    // ─── Paginación ─────────────────────────────────────────
    document.querySelectorAll('.pagination .page-item').forEach(li => {
        const a = li.querySelector('a.page-link');
        li.classList.remove('active','disabled');

        // Flecha «Anterior»
        if (a.getAttribute('aria-label') === 'Anterior') {
        if (currentPage <= 1) {
            li.classList.add('disabled');
        } else {
            li.addEventListener('click', e => {
            e.preventDefault();
            params.set('page', currentPage - 1);
            window.location.search = params.toString();
            });
        }
        }
        // Flecha «Siguiente»
        else if (a.getAttribute('aria-label') === 'Siguiente') {
        li.addEventListener('click', e => {
            e.preventDefault();
            params.set('page', currentPage + 1);
            window.location.search = params.toString();
        });
        }
        // Página numérica
        else {
        const num = parseInt(a.textContent.trim(), 10);
        if (num === currentPage) {
            li.classList.add('active');
        }
        li.addEventListener('click', e => {
            e.preventDefault();
            params.set('page', num);
            window.location.search = params.toString();
        });
        }
    });
    });