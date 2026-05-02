"""
Задание №6: SQL-инъекции
Шаг 4: Защищённый скрипт авторизации

Демонстрирует три метода защиты от SQL-инъекций:
1. Параметризованные запросы (prepared statements)
2. Экранирование специальных символов
3. Валидация входных данных
"""

import re

import psycopg2
from psycopg2 import sql as psycopg2_sql
from psycopg2.extensions import adapt

DB_CONFIG = {
    "dbname": "test_injection_db",
    "user": "ubuntu",
    "host": "localhost",
}


# ──────────────────────────────────────────────
# Метод 1: Параметризованные запросы (РЕКОМЕНДУЕМЫЙ)
# ──────────────────────────────────────────────
def secure_login_parameterized(username: str, password: str) -> list:
    """
    Параметризованный запрос: данные передаются отдельно от SQL-кода.
    База данных воспринимает их только как значения, а не как команды.
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    print(f"[ЗАЩИТА-1] Параметризованный запрос:")
    print(f"  Шаблон: {query}")
    print(f"  Параметры: ({username!r}, {password!r})\n")

    cur.execute(query, (username, password))
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows


# ──────────────────────────────────────────────
# Метод 2: Экранирование спецсимволов
# ──────────────────────────────────────────────
def secure_login_escaped(username: str, password: str) -> list:
    """
    Экранирование: специальные символы (кавычки и др.)
    заменяются безопасными последовательностями.
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    safe_user = adapt(username).getquoted().decode()
    safe_pass = adapt(password).getquoted().decode()

    query = (
        f"SELECT * FROM users WHERE username = {safe_user} "
        f"AND password = {safe_pass}"
    )
    print(f"[ЗАЩИТА-2] Запрос с экранированием:")
    print(f"  {query}\n")

    cur.execute(query)
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows


# ──────────────────────────────────────────────
# Метод 3: Валидация входных данных
# ──────────────────────────────────────────────
def validate_input(value: str) -> bool:
    """
    Проверяет, что строка содержит только допустимые символы:
    буквы, цифры, точку, дефис и подчёркивание.
    """
    pattern = r"^[A-Za-z0-9._-]+$"
    return bool(re.match(pattern, value))


def secure_login_validated(username: str, password: str) -> list:
    """
    Валидация: перед выполнением запроса проверяем,
    что ввод не содержит опасных символов.
    """
    print(f"[ЗАЩИТА-3] Валидация ввода:")
    print(f"  username={username!r}, password={password!r}")

    if not validate_input(username):
        print(f"  ОТКЛОНЕНО: недопустимые символы в username\n")
        return []

    if not validate_input(password):
        print(f"  ОТКЛОНЕНО: недопустимые символы в password\n")
        return []

    print(f"  Ввод прошёл валидацию — выполняем запрос\n")

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username = %s AND password = %s",
        (username, password),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def main():
    test_cases = [
        ("admin", "12345", "Легитимный вход"),
        ("admin", "' OR '1'='1", "SQL-инъекция"),
    ]

    # ── Метод 1 ──
    print("=" * 60)
    print("МЕТОД 1: Параметризованные запросы (prepared statements)")
    print("=" * 60)
    for user, pwd, label in test_cases:
        print(f"\n--- {label} ({user} / {pwd}) ---")
        result = secure_login_parameterized(user, pwd)
        print(f"  Найдено записей: {len(result)}")
        for row in result:
            print(f"  -> id={row[0]}, user={row[1]}, role={row[3]}")

    # ── Метод 2 ──
    print("\n" + "=" * 60)
    print("МЕТОД 2: Экранирование спецсимволов")
    print("=" * 60)
    for user, pwd, label in test_cases:
        print(f"\n--- {label} ({user} / {pwd}) ---")
        result = secure_login_escaped(user, pwd)
        print(f"  Найдено записей: {len(result)}")
        for row in result:
            print(f"  -> id={row[0]}, user={row[1]}, role={row[3]}")

    # ── Метод 3 ──
    print("\n" + "=" * 60)
    print("МЕТОД 3: Валидация входных данных")
    print("=" * 60)
    for user, pwd, label in test_cases:
        print(f"\n--- {label} ({user} / {pwd}) ---")
        result = secure_login_validated(user, pwd)
        print(f"  Найдено записей: {len(result)}")
        for row in result:
            print(f"  -> id={row[0]}, user={row[1]}, role={row[3]}")


if __name__ == "__main__":
    main()
