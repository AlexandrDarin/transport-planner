-- ==========================================
-- Transport Planner: Набор SQL-запросов (ПР7)
-- ==========================================

-- 1. Список всех остановок
SELECT id, name, latitude, longitude FROM stops ORDER BY name;

-- 2. Список всех маршрутов
SELECT id, title, route_number, transport_type FROM routes ORDER BY route_number;

-- 3. Поиск остановок по фрагменту названия (WHERE LIKE)
SELECT id, name FROM stops WHERE name LIKE '%Центр%';

-- 4. Фильтрация маршрутов по типу транспорта (WHERE)
SELECT id, title, route_number FROM routes WHERE transport_type = 'автобус';

-- 5. Получение списка активных поездок (WHERE)
SELECT id, route_id, user_id, trip_date FROM trips WHERE is_cancelled = 0 ORDER BY trip_date;

-- 6. Полная информация о поездках со сведениями о маршрутах и пользователях (JOIN)
SELECT trips.id, trips.trip_date, routes.title AS route_title, routes.route_number, users.name AS user_name, users.email
FROM trips
JOIN routes ON trips.route_id = routes.id
JOIN users ON trips.user_id = users.id
WHERE trips.is_cancelled = 0
ORDER BY trips.trip_date;

-- 7. Поиск свободных маршрутов на выбранную дату (NOT IN)
SELECT routes.id, routes.title, routes.route_number, routes.transport_type
FROM routes
WHERE routes.id NOT IN (
    SELECT trips.route_id FROM trips WHERE trips.trip_date = ? AND trips.is_cancelled = 0
)
ORDER BY routes.route_number;

-- 8. Общее количество активных поездок (COUNT)
SELECT COUNT(*) AS active_trips_count FROM trips WHERE is_cancelled = 0;

-- 9. Статистика поездок по маршрутам (LEFT JOIN + GROUP BY + COUNT)
SELECT routes.title AS route_title, routes.route_number, COUNT(trips.id) AS trips_count
FROM routes
LEFT JOIN trips ON routes.id = trips.route_id AND trips.is_cancelled = 0
GROUP BY routes.id, routes.title, routes.route_number
ORDER BY trips_count DESC;

-- 10. Популярные маршруты с числом поездок больше заданного (GROUP BY + HAVING)
SELECT routes.title AS route_title, COUNT(trips.id) AS trips_count
FROM routes
JOIN trips ON routes.id = trips.route_id
WHERE trips.is_cancelled = 0
GROUP BY routes.id, routes.title
HAVING COUNT(trips.id) >= 1
ORDER BY trips_count DESC;


-- 11. Пагинация списка остановок (сортировка, LIMIT и OFFSET)
SELECT id, name, latitude, longitude
FROM stops
ORDER BY name
LIMIT 10 OFFSET 0;
