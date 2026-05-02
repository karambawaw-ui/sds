-- Задание №6: SQL-инъекции
-- Шаг 1: Создание базы данных и таблицы пользователей

CREATE DATABASE test_injection_db;

\c test_injection_db

CREATE TABLE users (
    id       SERIAL PRIMARY KEY,
    username VARCHAR(50)  NOT NULL,
    password VARCHAR(50)  NOT NULL,
    role     VARCHAR(20)  DEFAULT 'user'
);

INSERT INTO users (username, password, role) VALUES
    ('admin',    '12345',    'admin'),
    ('user1',    'password', 'user'),
    ('manager',  'qwerty',   'manager'),
    ('guest',    'guest123', 'user');

SELECT * FROM users;
