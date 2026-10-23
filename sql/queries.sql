-- ==========================================================
-- Transport Planner: SQL-запросы проекта (ПР7)
-- Знак ? — параметр, значение передаётся из Python отдельно.
-- Те же запросы выполняют Django-представления.
-- ==========================================================

-- ---------- ВЫБОРКА СПИСКОВ (SELECT ... ORDER BY) ----------

-- 1. Список маршрутов (страница /routes/)
SELECT id, number, transport_type, base_price, travel_time_minutes
FROM routes
ORDER BY number;

-- 2. Список остановок по городам (страница /stops/)
SELECT id, name, city
FROM stops
ORDER BY city, name;

-- 3. Список пользователей (страница /users/)
SELECT id, name, age, has_benefits
FROM users
ORDER BY name;

-- ---------- ФИЛЬТРАЦИЯ (WHERE) ----------

-- 4. Поиск маршрутов по номеру или виду транспорта (/routes/?q=)
SELECT id, number, transport_type, base_price, travel_time_minutes
FROM routes
WHERE number LIKE ? OR transport_type LIKE ?
ORDER BY number;

-- 5. Маршруты с ценой не выше заданной (/routes/?max_price=)
SELECT id, number, transport_type, base_price, travel_time_minutes
FROM routes
WHERE base_price <= ?
ORDER BY base_price;

-- 6. Поиск остановок по названию или городу (/stops/?q=)
SELECT id, name, city
FROM stops
WHERE name LIKE ? OR city LIKE ?
ORDER BY city, name;

-- 7. Поиск пассажиров по имени (/users/?q=)
SELECT id, name, age, has_benefits
FROM users
WHERE name LIKE ?
ORDER BY name;

-- 8. Один маршрут по идентификатору (/routes/<id>/)
SELECT id, number, transport_type, base_price, travel_time_minutes
FROM routes
WHERE id = ?;

-- 9. Одна остановка по идентификатору (/stops/<id>/)
SELECT id, name, city
FROM stops
WHERE id = ?;

-- 10. Один пользователь по идентификатору (/users/<id>/)
SELECT id, name, age, has_benefits
FROM users
WHERE id = ?;

-- 11. Свободные маршруты на дату: нет активной поездки (подзапрос NOT IN)
--     (/routes/available/?date=2026-09-15)
SELECT id, number, transport_type, base_price, travel_time_minutes
FROM routes
WHERE id NOT IN (
    SELECT route_id
    FROM trips
    WHERE trip_date = ?
      AND is_cancelled = 0
)
ORDER BY number;

-- ---------- СОЕДИНЕНИЕ ТАБЛИЦ (JOIN) ----------

-- 12. Все поездки с маршрутом, пассажиром, остановками и ценой
--     с учётом льготы (/trips/)
SELECT
    t.id, t.route_id, t.user_id, t.stop_from_id, t.stop_to_id,
    t.trip_date, t.is_cancelled,
    r.number AS route_number, r.transport_type, r.base_price,
    u.name AS passenger, u.has_benefits,
    sf.name AS origin, st.name AS destination,
    ROUND(r.base_price * CASE WHEN u.has_benefits = 1
                              THEN 0.5 ELSE 1 END, 2) AS price
FROM trips t
JOIN routes r ON r.id = t.route_id
JOIN users u ON u.id = t.user_id
JOIN stops sf ON sf.id = t.stop_from_id
JOIN stops st ON st.id = t.stop_to_id
ORDER BY t.trip_date DESC, t.id DESC;

-- 13. Поездки по статусу: 0 — активные, 1 — отменённые (/trips/?status=)
SELECT
    t.id, t.route_id, t.user_id, t.stop_from_id, t.stop_to_id,
    t.trip_date, t.is_cancelled,
    r.number AS route_number, r.transport_type, r.base_price,
    u.name AS passenger, u.has_benefits,
    sf.name AS origin, st.name AS destination,
    ROUND(r.base_price * CASE WHEN u.has_benefits = 1
                              THEN 0.5 ELSE 1 END, 2) AS price
FROM trips t
JOIN routes r ON r.id = t.route_id
JOIN users u ON u.id = t.user_id
JOIN stops sf ON sf.id = t.stop_from_id
JOIN stops st ON st.id = t.stop_to_id
WHERE t.is_cancelled = ?
ORDER BY t.trip_date DESC, t.id DESC;

-- 14. Одна поездка с полной информацией (/trips/<id>/)
SELECT
    t.id, t.route_id, t.user_id, t.stop_from_id, t.stop_to_id,
    t.trip_date, t.is_cancelled,
    r.number AS route_number, r.transport_type, r.base_price,
    u.name AS passenger, u.has_benefits,
    sf.name AS origin, st.name AS destination,
    ROUND(r.base_price * CASE WHEN u.has_benefits = 1
                              THEN 0.5 ELSE 1 END, 2) AS price
FROM trips t
JOIN routes r ON r.id = t.route_id
JOIN users u ON u.id = t.user_id
JOIN stops sf ON sf.id = t.stop_from_id
JOIN stops st ON st.id = t.stop_to_id
WHERE t.id = ?;

-- 15. Поездки маршрута с именами пассажиров (/routes/<id>/)
SELECT t.id, t.trip_date, t.is_cancelled, u.name AS passenger
FROM trips t
JOIN users u ON u.id = t.user_id
WHERE t.route_id = ?
ORDER BY t.trip_date;

-- 16. Поездки, связанные с остановкой (/stops/<id>/)
SELECT t.id, t.trip_date, t.is_cancelled, r.number
FROM trips t
JOIN routes r ON r.id = t.route_id
WHERE t.stop_from_id = ? OR t.stop_to_id = ?
ORDER BY t.trip_date;

-- 17. Поездки пассажира (/users/<id>/)
SELECT t.id, t.trip_date, t.is_cancelled, r.number
FROM trips t
JOIN routes r ON r.id = t.route_id
WHERE t.user_id = ?
ORDER BY t.trip_date DESC;

-- ---------- АГРЕГАТНЫЕ ФУНКЦИИ (COUNT, SUM, AVG, MIN, MAX) ----------

-- 18. Количество записей во всех таблицах (главная страница)
SELECT
    (SELECT COUNT(*) FROM routes) AS routes,
    (SELECT COUNT(*) FROM stops) AS stops,
    (SELECT COUNT(*) FROM trips) AS trips,
    (SELECT COUNT(*) FROM users) AS users;

-- 19. Статистика цен маршрутов (/routes/)
SELECT
    COUNT(*) AS count,
    MIN(base_price) AS min_price,
    MAX(base_price) AS max_price,
    AVG(base_price) AS avg_price
FROM routes;

-- 20. Количество поездок: всего, активных, отменённых (/trips/)
SELECT
    COUNT(*) AS total,
    SUM(CASE WHEN is_cancelled = 0 THEN 1 ELSE 0 END) AS active,
    SUM(CASE WHEN is_cancelled = 1 THEN 1 ELSE 0 END) AS cancelled
FROM trips;

-- 21. Суммарная стоимость активных поездок (/statistics/)
SELECT SUM(r.base_price * CASE WHEN u.has_benefits = 1
                               THEN 0.5 ELSE 1 END) AS total
FROM trips t
JOIN routes r ON r.id = t.route_id
JOIN users u ON u.id = t.user_id
WHERE t.is_cancelled = 0;

-- 22. Количество пользователей с льготами
SELECT COUNT(*) AS benefit_users
FROM users
WHERE has_benefits = 1;

-- ---------- ГРУППИРОВКА (GROUP BY, HAVING) ----------

-- 23. Активные поездки по маршрутам: LEFT JOIN сохраняет маршруты
--     без поездок со значением 0 (/statistics/)
SELECT r.id, r.number, COUNT(t.id) AS trip_count
FROM routes r
LEFT JOIN trips t
       ON t.route_id = r.id AND t.is_cancelled = 0
GROUP BY r.id, r.number
ORDER BY trip_count DESC, r.number;

-- 24. Популярные маршруты: групп отбирает HAVING (/statistics/?min_trips=)
SELECT r.id, r.number, COUNT(t.id) AS trip_count
FROM routes r
JOIN trips t ON t.route_id = r.id
WHERE t.is_cancelled = 0
GROUP BY r.id, r.number
HAVING COUNT(t.id) >= ?
ORDER BY trip_count DESC, r.number;

-- 25. Маршруты по видам транспорта: количество и средняя цена
SELECT transport_type,
       COUNT(*) AS routes_count,
       AVG(base_price) AS avg_price
FROM routes
GROUP BY transport_type
ORDER BY routes_count DESC, transport_type;

-- 26. Пассажиры: количество активных поездок и потраченная сумма
SELECT u.id, u.name,
       COUNT(t.id) AS trips_count,
       COALESCE(SUM(r.base_price * CASE WHEN u.has_benefits = 1
                                        THEN 0.5 ELSE 1 END), 0)
           AS total_spent
FROM users u
LEFT JOIN trips t ON t.user_id = u.id AND t.is_cancelled = 0
LEFT JOIN routes r ON r.id = t.route_id
GROUP BY u.id, u.name
ORDER BY total_spent DESC, u.name;

-- 27. Количество остановок по городам
SELECT city, COUNT(*) AS stops_count
FROM stops
GROUP BY city
ORDER BY stops_count DESC, city;

-- ---------- LIMIT / OFFSET ----------

-- 28. Три самые загруженные остановки отправления (/statistics/)
SELECT s.id, s.name, COUNT(t.id) AS departures
FROM stops s
LEFT JOIN trips t
       ON t.stop_from_id = s.id AND t.is_cancelled = 0
GROUP BY s.id, s.name
ORDER BY departures DESC, s.name
LIMIT 3 OFFSET 0;

-- 29. Сумма потраченного одним пользователем (/users/<id>/)
SELECT COALESCE(SUM(r.base_price * CASE WHEN u.has_benefits = 1
                                        THEN 0.5 ELSE 1 END), 0) AS total
FROM trips t
JOIN routes r ON r.id = t.route_id
JOIN users u ON u.id = t.user_id
WHERE t.user_id = ? AND t.is_cancelled = 0;
