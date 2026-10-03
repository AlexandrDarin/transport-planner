"""View-функции приложения homepage.

Модуль задаёт общий HTML-каркас всех страниц проекта (page()),
главную страницу (index()) и страницу «О проекте» (about()).
"""

from django.http import HttpResponse


BOOTSTRAP_CSS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
    "/dist/css/bootstrap.min.css"
)

CUSTOM_CSS = """
body { background-color: #f5f7fa; }
.navbar-brand { font-weight: 600; letter-spacing: 0.5px; }
.card { border: none; border-radius: 12px; }
.card-title { font-weight: 600; }
.list-group-item { border-left: none; border-right: none; }
.list-group-item:first-child { border-top: none; }
.badge-time { background-color: #6c757d; }
.badge-price { background-color: #0d6efd; }
.footer-note { color: #6c757d; font-size: 0.85rem; }
.breadcrumb { background: transparent; padding-left: 0; }
h1, h2, h3 { color: #1f2937; }
.stat-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.stat-value { font-size: 1.75rem; font-weight: 700; color: #0d6efd; }
.stat-label { color: #6c757d; font-size: 0.9rem; }
"""


NAV_ITEMS = [
    ("/", "Главная", "home"),
    ("/routes/", "Маршруты", "routes"),
    ("/stops/", "Остановки", "stops"),
    ("/trips/", "Поездки", "trips"),
    ("/users/", "Пользователи", "users"),
    ("/about/", "О проекте", "about"),
]


def _nav_html(active: str) -> str:
    """Собрать навигацию с подсветкой активного пункта."""
    parts = []
    for url, label, key in NAV_ITEMS:
        cls = "nav-link"
        if key == active:
            cls += " active fw-bold text-white"
        else:
            cls += " text-white-50"
        parts.append(f'<a class="{cls}" href="{url}">{label}</a>')
    return "".join(parts)


def _breadcrumbs(items) -> str:
    """Собрать хлебные крошки из списка (label, url|None)."""
    parts = []
    for label, url in items:
        if url is None:
            parts.append(
                f'<li class="breadcrumb-item active">{label}</li>'
            )
        else:
            parts.append(
                f'<li class="breadcrumb-item">'
                f'<a href="{url}">{label}</a></li>'
            )
    return (
        '<nav aria-label="breadcrumb">'
        '<ol class="breadcrumb">' + "".join(parts) + "</ol></nav>"
    )


def page(title: str, content: str, active: str = "",
         breadcrumbs: str = "") -> str:
    """Единый HTML-каркас всех страниц проекта."""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{BOOTSTRAP_CSS}">
    <style>{CUSTOM_CSS}</style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
        <div class="container">
            <a class="navbar-brand" href="/">🚌 Сервис поездок</a>
            <div class="navbar-nav">{_nav_html(active)}</div>
        </div>
    </nav>
    <main class="container py-4">
        {breadcrumbs}
        {content}
    </main>
    <footer class="text-center py-4 mt-5 footer-note">
        Сервис планирования поездок на общественном транспорте
    </footer>
</body>
</html>"""


def index(request):
    """Главная страница: описание и навигация."""
    content = """
    <div class="p-5 mb-4 bg-white rounded-3 shadow-sm">
        <h1 class="display-5">Сервис планирования поездок</h1>
        <p class="lead mb-3">
            Планирование поездок на общественном транспорте:
            маршруты, остановки, поездки пассажиров.
        </p>
        <hr>
        <p class="mb-2"><strong>Доступные разделы:</strong></p>
        <a href="/routes/" class="btn btn-primary me-2">
            🚏 Маршруты
        </a>
        <a href="/stops/" class="btn btn-primary me-2">
            📍 Остановки
        </a>
        <a href="/trips/" class="btn btn-secondary me-2">
            🎫 Поездки
        </a>
        <a href="/users/" class="btn btn-secondary me-2">
            👤 Пользователи
        </a>
        <a href="/about/" class="btn btn-outline-secondary">
            ℹ️ О проекте
        </a>
    </div>

    <div class="row g-4">
        <div class="col-md-6 col-lg-3">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">🚏 Маршруты</h5>
                    <p class="card-text">
                        Городские маршруты с ценой, видом транспорта
                        и временем в пути.
                    </p>
                    <a href="/routes/"
                       class="btn btn-outline-primary">Открыть</a>
                </div>
            </div>
        </div>
        <div class="col-md-6 col-lg-3">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">📍 Остановки</h5>
                    <p class="card-text">
                        Остановки общественного транспорта
                        по городам.
                    </p>
                    <a href="/stops/"
                       class="btn btn-outline-primary">Открыть</a>
                </div>
            </div>
        </div>
        <div class="col-md-6 col-lg-3">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">🎫 Поездки</h5>
                    <p class="card-text">
                        Активные и отменённые поездки с расчётом
                        стоимости.
                    </p>
                    <a href="/trips/"
                       class="btn btn-outline-primary">Открыть</a>
                </div>
            </div>
        </div>
        <div class="col-md-6 col-lg-3">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">👤 Пользователи</h5>
                    <p class="card-text">
                        Пассажиры с информацией о льготах
                        и их поездках.
                    </p>
                    <a href="/users/"
                       class="btn btn-outline-primary">Открыть</a>
                </div>
            </div>
        </div>
    </div>

    <div class="alert alert-light mt-4 border">
        <strong>Консольная версия:</strong>
        полный набор операций доступен и в консоли —
        <code>python main.py</code>.
    </div>
    """
    return HttpResponse(page(
        "Сервис планирования поездок", content, active="home"
    ))


def about(request):
    """Страница «О проекте»."""
    content = """
    <h1 class="mb-3">О проекте</h1>
    <div class="card shadow-sm mb-3">
        <div class="card-body">
            <h5 class="card-title">Назначение</h5>
            <p class="card-text mb-0">
                Консольное приложение, дополненное веб-интерфейсом
                на Django. Позволяет просматривать маршруты,
                остановки, поездки и пользователей.
            </p>
        </div>
    </div>
    <div class="row g-3">
        <div class="col-md-6">
            <div class="card shadow-sm h-100">
                <div class="card-body">
                    <h5 class="card-title">Предметная область</h5>
                    <p class="card-text mb-0">
                        Городские пассажирские перевозки: маршруты,
                        остановки, расписание, стоимость проезда.
                    </p>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card shadow-sm h-100">
                <div class="card-body">
                    <h5 class="card-title">Сущности</h5>
                    <ul class="mb-0">
                        <li>Пользователь (пассажир)</li>
                        <li>Маршрут</li>
                        <li>Остановка</li>
                        <li>Поездка</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
    <div class="card shadow-sm mt-3">
        <div class="card-body">
            <h5 class="card-title">Технологии</h5>
            <ul class="mb-0">
                <li>Python 3, Django 5.2</li>
                <li>Bootstrap 5.3 (через CDN)</li>
                <li>JSON-хранилище из ПР3</li>
                <li>pytest и flake8</li>
            </ul>
        </div>
    </div>
    """
    crumbs = _breadcrumbs([("Главная", "/"), ("О проекте", None)])
    return HttpResponse(page(
        "О проекте", content, active="about", breadcrumbs=crumbs
    ))