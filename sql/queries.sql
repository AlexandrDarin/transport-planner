-- 1. Список маршрутов
SELECT id, number, transport_type, base_price FROM routes ORDER BY number;

-- 2. Список остановок по названию
SELECT id, name, city FROM stops ORDER BY name LIMIT 10;

-- 3. Фильтрация маршрутов по максимальной цене (параметр ?)
SELECT id, number, base_price FROM routes WHERE base_price <= ? ORDER BY base_price;

-- 4. Поиск остановок по городу
SELECT id, name, city FROM stops WHERE city = ? ORDER BY name;

-- 5. Поездки с названиями маршрутов и пассажиров (JOIN)
SELECT t.id, r.number, u.name, t.trip_date, t.is_cancelled FROM trips t JOIN routes r ON r.id=t.route_id JOIN users u ON u.id=t.user_id ORDER BY t.trip_date;

-- 6. Подробная информация о поездках с остановками (JOIN)
SELECT t.id, r.number, u.name AS passenger, sf.name AS origin, st.name AS destination, t.trip_date FROM trips t JOIN routes r ON r.id=t.route_id JOIN users u ON u.id=t.user_id JOIN stops sf ON sf.id=t.stop_from_id JOIN stops st ON st.id=t.stop_to_id;

-- 7. Общее количество поездок
SELECT COUNT(*) AS trip_count FROM trips;

-- 8. Средняя, минимальная и максимальная цена маршрута
SELECT AVG(base_price) AS average_price, MIN(base_price) AS min_price, MAX(base_price) AS max_price FROM routes;

-- 9. Количество поездок по маршрутам (GROUP BY)
SELECT r.number, COUNT(t.id) AS trip_count FROM routes r LEFT JOIN trips t ON t.route_id=r.id GROUP BY r.id, r.number ORDER BY trip_count DESC;

-- 10. Маршруты, у которых поездок больше указанного количества (GROUP BY + HAVING)
SELECT r.number, COUNT(t.id) AS trip_count FROM routes r JOIN trips t ON t.route_id=r.id GROUP BY r.id, r.number HAVING COUNT(t.id) > ?;

-- 11. Активные поездки на выбранную дату (WHERE)
SELECT id, route_id, user_id, trip_date FROM trips WHERE is_cancelled=0 AND trip_date=? ORDER BY id;

-- 12. Количество пользователей с льготами
SELECT COUNT(*) AS benefit_users FROM users WHERE has_benefits=1;
