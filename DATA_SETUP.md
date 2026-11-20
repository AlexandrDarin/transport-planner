# Подготовка базы данных для ПР9–ПР10

Основная БД Django — `db.sqlite3` в корне проекта. Исходная SQLite-база предыдущих этапов находится в `data/transport_planner.sqlite3` и не является основной БД сайта.

В новом окружении выполните из каталога с `manage.py`:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py import_legacy_data
python manage.py seed_demo_data
python manage.py createsuperuser
python manage.py check
python manage.py makemigrations --check --dry-run
pytest -v
```

`import_legacy_data` переносит исходные записи с сохранением первичных ключей и связей. Затем `seed_demo_data` добавляет демонстрационный набор: 10 маршрутов, 12 остановок, 10 пассажиров и до 30 поездок. Команда повторно запускается без дублирования созданных ею записей.

Если доменные таблицы уже заполнены, обычный импорт не нужен: запустите только `python manage.py seed_demo_data`. Опция `import_legacy_data --replace` очищает доменные ORM-таблицы и повторно переносит исходную базу; используйте её только после резервного копирования.

После создания суперпользователя войдите в `/admin/`. Модели Django Admin — это доменные сущности проекта; `Passenger` не является учётной записью Django. Вход в административную панель осуществляется учётной записью суперпользователя.
