# Transport Planner — индивидуальный проект ПР1–ПР7

Веб-сервис планирования поездок на общественном транспорте. Проект содержит консольную версию на Python, Django-веб-интерфейс и реляционное хранилище SQLite.

## Запуск

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python db/import_json.py
python manage.py check
python manage.py migrate
python manage.py runserver
```

Откройте `http://127.0.0.1:8000/`.

## Страницы

| URL | Назначение |
|---|---|
| `/` | Главная страница и сводные показатели |
| `/about/` | Информация о проекте |
| `/statistics/` | Агрегатная статистика, GROUP BY и HAVING |
| `/routes/`, `/routes/<id>/` | Список и карточка маршрута, поиск по номеру/виду транспорта |
| `/stops/`, `/stops/<id>/` | Список и карточка остановки, поиск |
| `/trips/`, `/trips/<id>/` | Список, фильтрация статуса и карточка поездки |
| `/users/`, `/users/<id>/` | Список и карточка пассажира, поиск |

## ПР6 — шаблоны Django

- Общий каркас в `homepage/templates/base.html`.
- Страницы используют `{% extends %}`, `{% block %}`, `{% include %}`, циклы и условия.
- Навигация использует именованные URL-маршруты и namespace приложений.
- CSS и JavaScript находятся в `homepage/static/homepage/`.
- HTML не формируется конкатенацией строк во view-функциях.

## ПР7 — SQLite и SQL

- `sql/schema.sql` — таблицы `routes`, `stops`, `users`, `trips`, внешние ключи и индексы.
- `db/database.py` — подключение SQLite с `sqlite3.Row` и `PRAGMA foreign_keys = ON`.
- `db/import_json.py` — импорт исходных JSON в `data/transport_planner.sqlite3`; JSON-файлы сохраняются для консольной версии.
- `sql/queries.sql` — 12 примеров запросов, включая WHERE, JOIN, агрегаты, GROUP BY и HAVING.
- Django-представления используют SQLite, параметризованные запросы и выводят результаты на страницах сайта.

## Структура

- `models/`, `storage.py`, `main.py`, `data/*.json` — предметная модель и консольная версия предыдущих практических работ.
- `homepage/`, `routes_app/`, `stops_app/`, `trips_app/`, `users_app/` — Django-веб-приложение.
- `db/` и `sql/` — доступ к SQLite, импорт данных, схема и запросы.
- `tests/` — тесты предыдущих этапов.

## Проверка

```bash
python db/import_json.py
python manage.py check
pytest -v
```

База SQLite создаётся/обновляется из JSON при запуске импорта. Для повторного импорта можно снова выполнить `python db/import_json.py`.
