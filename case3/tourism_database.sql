-- База данных "Туризм"
-- Создание базы данных
CREATE DATABASE IF NOT EXISTS tourism_db;
USE tourism_db;

-- Таблица справочник: Страны
CREATE TABLE countries (
    country_id INT PRIMARY KEY AUTO_INCREMENT,
    country_name VARCHAR(100) NOT NULL,
    country_code VARCHAR(3) NOT NULL UNIQUE
);

-- Таблица справочник: Отели
CREATE TABLE hotels (
    hotel_id INT PRIMARY KEY AUTO_INCREMENT,
    hotel_name VARCHAR(200) NOT NULL,
    country_id INT NOT NULL,
    stars INT CHECK (stars >= 1 AND stars <= 5),
    address TEXT,
    phone VARCHAR(20),
    FOREIGN KEY (country_id) REFERENCES countries(country_id)
);

-- Таблица справочник: Услуги
CREATE TABLE services (
    service_id INT PRIMARY KEY AUTO_INCREMENT,
    service_name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL
);

-- Таблица переменной информации: Заказы туров
CREATE TABLE tour_orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(100) NOT NULL,
    customer_phone VARCHAR(20),
    customer_email VARCHAR(100),
    hotel_id INT NOT NULL,
    service_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'confirmed', 'cancelled') DEFAULT 'pending',
    FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id),
    FOREIGN KEY (service_id) REFERENCES services(service_id)
);

-- Вставка тестовых данных
INSERT INTO countries (country_name, country_code) VALUES
('Россия', 'RUS'),
('Турция', 'TUR'),
('Египет', 'EGY'),
('Испания', 'ESP'),
('Италия', 'ITA');

INSERT INTO hotels (hotel_name, country_id, stars, address, phone) VALUES
('Гранд Отель Москва', 1, 5, 'ул. Тверская, 1, Москва', '+7-495-123-45-67'),
('Пальма Резорт', 2, 4, 'ул. Пляжная, 15, Анталья', '+90-242-123-45-67'),
('Пирамида Отель', 3, 4, 'ул. Нильская, 25, Каир', '+20-2-123-45-67'),
('Солнечный Барселона', 4, 3, 'ул. Рамбла, 10, Барселона', '+34-93-123-45-67'),
('Венеция Палас', 5, 5, 'ул. Канале, 5, Венеция', '+39-41-123-45-67');

INSERT INTO services (service_name, description, price) VALUES
('Экскурсия по городу', 'Обзорная экскурсия с гидом', 50.00),
('Трансфер из аэропорта', 'Доставка от аэропорта до отеля', 30.00),
('Питание полупансион', 'Завтрак и ужин включены', 25.00),
('Питание полный пансион', 'Завтрак, обед и ужин включены', 40.00),
('СПА процедуры', 'Массаж и спа процедуры', 80.00);

INSERT INTO tour_orders (customer_name, customer_phone, customer_email, hotel_id, service_id, start_date, end_date, total_price) VALUES
('Иванов Иван', '+7-999-123-45-67', 'ivanov@mail.ru', 1, 1, '2024-06-01', '2024-06-07', 500.00),
('Петрова Анна', '+7-999-234-56-78', 'petrova@gmail.com', 2, 3, '2024-07-15', '2024-07-22', 800.00),
('Сидоров Петр', '+7-999-345-67-89', 'sidorov@yandex.ru', 3, 2, '2024-08-10', '2024-08-17', 600.00);

-- Примеры запросов для проверки
SELECT 'Все страны:' as info;
SELECT * FROM countries;

SELECT 'Все отели:' as info;
SELECT h.hotel_name, c.country_name, h.stars 
FROM hotels h 
JOIN countries c ON h.country_id = c.country_id;

SELECT 'Все заказы:' as info;
SELECT o.order_id, o.customer_name, h.hotel_name, s.service_name, o.total_price
FROM tour_orders o
JOIN hotels h ON o.hotel_id = h.hotel_id
JOIN services s ON o.service_id = s.service_id; 