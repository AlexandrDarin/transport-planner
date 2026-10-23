# Transport Planner — сервис планирования поездок

Учебный индивидуальный проект (ПР1–ПР7): консольное приложение на Python
с веб-интерфейсом на Django, шаблонами DTL и реляционным хранилищем SQLite.

## 1. Назначение

Сервис хранит маршруты общественного транспорта, остановки, пассажиров
и их поездки, считает стоимость с учётом льгот (скидка 50 %) и показывает
информацию через веб-интерфейс Django. Консольная версия (`main.py`)
сохранена и работает с JSON-файлами.

## 2. Технологии

Python 3, Django 5.2, Django Template Language, HTML5, CSS3, JavaScript,
Bootstrap 5, SQLite (модуль `sqlite3`), JSON, pytest, flake8, Git.

## 3. Запуск

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows PowerShell
python -m pip install -r requirements.txt
python -m db.import_json          # (пере)создать таблицы и загрузить JSON
python manage.py check
python manage.py runserver
```

Сайт: http://127.0.0.1:8000/

Пересоздать базу с нуля (PowerShell):

```powershell
Remove-Item .\data\transport_planner.sqlite3
python -m db.import_json
```

## 4. Страницы

| URL | Что показывает | Источник данных |
|---|---|---|
| `/` | главная, количество записей | SQLite (COUNT) |
| `/routes/` | список, поиск `?q=`, фильтр цены `?max_price=` | SQLite (WHERE, LIKE) |
| `/routes/<id>/` | маршрут и его поездки, 404 если нет | SQLite (JOIN) |
| `/routes/available/?date=` | свободные маршруты на дату | SQLite (подзапрос NOT IN) |
| `/stops/`, `/stops/<id>/` | остановки, поиск, связанные поездки | SQLite |
| `/trips/`, `/trips/<id>/` | поездки, фильтр `?status=active|cancelled` | SQLite (JOIN 5 таблиц) |
| `/users/`, `/users/<id>/` | пассажиры, поиск, траты | SQLite |
| `/statistics/` | агрегаты, GROUP BY, HAVING `?min_trips=`, LIMIT | SQLite |
| `/about/` | о проекте | — |

## 5. ПР6 — шаблоны Django

- `templates/base.html` — общий каркас (`{% block title %}`,
  `{% block content %}`), подключён через `DIRS` в `settings.py`;
- `templates/includes/navigation.html` — навигация через `{% include %}`
  и `{% url %}`, активный пункт определяется по `request.resolver_match`;
- дочерние шаблоны используют `{% extends "base.html" %}`;
- включаемые фрагменты: `routes_app/includes/route_card.html`,
  `trips_app/includes/trip_status.html`;
- данные передаются через `context` в `render()`; циклы
  `{% for %}…{% empty %}`, условия `{% if %}`;
- именованные URL и пространства имён (`app_name`): `homepage`, `routes`,
  `stops`, `trips`, `users` (`{% url 'routes:detail' route.id %}`);
- фильтры: `length`, `default`, `floatformat`;
- статика `homepage/static/homepage/`: `css/style.css`, `js/main.js`
  (текущий год в подвале), `img/logo.png`;
- HTML в Python не формируется, функция `page()` удалена;
- 404 для несуществующих объектов: страница из шаблона со статусом 404.

## 6. ПР7 — слой базы данных

База: `data/transport_planner.sqlite3` (в репозитории).

| Таблица | Поля |
|---|---|
| `routes` | `id` INTEGER PK, `number` TEXT, `transport_type` TEXT, `base_price` REAL, `travel_time_minutes` INTEGER |
| `stops` | `id` INTEGER PK, `name` TEXT, `city` TEXT |
| `users` | `id` INTEGER PK, `name` TEXT, `age` INTEGER, `has_benefits` INTEGER (0/1) |
| `trips` | `id` INTEGER PK, `route_id` FK→routes, `user_id` FK→users, `stop_from_id` FK→stops, `stop_to_id` FK→stops, `trip_date` TEXT (YYYY-MM-DD), `is_cancelled` INTEGER (0/1) |

Первичные ключи — поля `id`; внешние ключи — в таблице `trips`
(четыре связи). Все поля обязательны (`NOT NULL`), добавлены `CHECK`
и индексы.

Файлы:

- `sql/schema.sql` — создание таблиц (`CREATE TABLE IF NOT EXISTS`);
- `sql/queries.sql` — 29 проверенных запросов с комментариями (выборка
  списков, WHERE, JOIN, COUNT/SUM/AVG/MIN/MAX, GROUP BY, HAVING,
  LIMIT/OFFSET, подзапрос);
- `db/database.py` — `get_connection()`: `PRAGMA foreign_keys = ON`,
  `row_factory = sqlite3.Row` (поля по имени: `{{ route.number }}`);
- `db/import_json.py` — перенос данных из JSON (`executemany`, параметры
  `?`, `commit`/`rollback`). Запуск: `python -m db.import_json`.

Django-представления выполняют SQL-запросы напрямую через `sqlite3`,
значения передаются **только параметрами `?`** (без f-строк).
Django ORM пока не используется (следующие практические работы).
JSON-хранилище (`storage.py`, `models/`, `main.py`) сохранено.

## 7. Структура

```
templates/                 base.html, includes/navigation.html
homepage/ routes_app/ stops_app/ trips_app/ users_app/
    views.py urls.py templates/<app>/ (+ includes/)
homepage/static/homepage/  css/ js/ img/
db/                        database.py, import_json.py
sql/                       schema.sql, queries.sql
data/                      *.json, transport_planner.sqlite3
models/ storage.py main.py utils.py   — ПР1–ПР3 (консольная версия)
tests/                     pytest-тесты (модели, БД, веб)
```

## 8. Проверка

```bash
python manage.py check
pytest -v
flake8 . --extend-exclude=venv,.venv
```

## 9. Git

Коммиты этапов начинаются с префиксов `PR6:` и `PR7:`.

## 10. Дальнейшее развитие

Подключение базы данных к Django через модели и ORM, формы Django,
операции создания/изменения/удаления.
