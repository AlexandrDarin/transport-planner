# Transport Planner

Учебный веб-проект для просмотра городских транспортных маршрутов, остановок и поездок. Django отвечает за страницы и шаблоны, а данные предметной области читаются из SQLite через стандартный модуль `sqlite3`.

## Запуск

1. Установите Python 3.10+.
2. Создайте и активируйте виртуальное окружение.
3. Установите зависимости:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. При необходимости пересоздайте структуру БД из корня проекта:

   ```bash
   python -c "import sqlite3; from pathlib import Path; p=Path('data/transport_planner.sqlite3'); p.parent.mkdir(exist_ok=True); c=sqlite3.connect(p); c.executescript(Path('sql/schema.sql').read_text(encoding='utf-8')); c.commit(); c.close()"
   ```

5. Импортируйте актуальные данные из JSON (скрипт можно запускать повторно):

   ```bash
   python -m db.import_json
   ```

6. Запустите проверки и сервер:

   ```bash
   python manage.py check
   pytest -v
   python manage.py runserver
   ```

Откройте `http://127.0.0.1:8000/`.

## Страницы

- `/` — главная страница со сводными показателями;
- `/routes/` — список маршрутов из SQLite;
- `/stops/` — список остановок из SQLite;
- `/trips/` — активные поездки со связанными данными маршрута и пользователя;
- `/routes/available/` — поиск маршрутов, свободных на выбранную дату;
- `/statistics/` — статистика поездок по маршрутам.

## Структура проекта

- `config/` — настройки Django и корневые URL;
- `homepage/` — представления, URL приложения и шаблоны;
- `homepage/templates/homepage/base.html` — базовый шаблон;
- `homepage/templates/partials/nav.html` — навигация, подключаемая через `{% include %}`;
- `static/css/style.css`, `static/js/main.js` — статические ресурсы;
- `sql/schema.sql` — схема SQLite с первичными и внешними ключами;
- `sql/queries.sql` — 11 запросов SQL, включая SELECT, WHERE, JOIN, COUNT, GROUP BY, HAVING, LIMIT и OFFSET;
- `db/database.py` — подключение к БД и включение проверки внешних ключей;
- `db/import_json.py` — транзакционный перенос данных из JSON в SQLite;
- `data/*.json` — исходные данные;
- `data/transport_planner.sqlite3` — файл базы данных.

## Реализованные требования ПР6

- Единый базовый шаблон и наследование через `{% extends %}` / `{% block %}`;
- подключение фрагмента навигации через `{% include %}`;
- подключение CSS и JavaScript через `{% load static %}`;
- именованные URL-маршруты с пространством имён `homepage`;
- адаптивная навигация и единый стиль страниц.

## Реализованные требования ПР7

- Реляционная схема SQLite: `stops`, `routes`, `users`, `trips`;
- первичные ключи и внешние ключи `trips.route_id` и `trips.user_id`;
- подключение через `sqlite3.connect()` и `PRAGMA foreign_keys = ON`;
- импорт JSON через `executemany()`, параметризованные запросы, `commit()` и `rollback()`;
- SQL-запросы с фильтрацией, соединениями, агрегатными функциями, группировкой, `HAVING`, сортировкой и ограничением выборки;
- получение данных в Django-представлениях и отображение в шаблонах;
- поиск свободных маршрутов по дате и статистика поездок;
- тесты целостности БД и сравнения количества импортированных записей с JSON.

## Проверки

```bash
python manage.py check
pytest -v
flake8 . --extend-exclude=venv
```

Для Git-контрольной точки выполните в локальном репозитории коммит с префиксом `PR7:`, например `PR7: add SQLite database and SQL queries`. Git-история в ZIP-архив не входит.
