"""
Задание №6: SQL-инъекции
Шаг 3: Уязвимый скрипт авторизации (НЕ ИСПОЛЬЗОВАТЬ В РЕАЛЬНЫХ ПРОЕКТАХ!)

Этот скрипт демонстрирует, как конкатенация строк при формировании
SQL-запроса делает систему уязвимой к SQL-инъекциям.
"""

import psycopg2

DB_CONFIG = {
    "dbname": "test_injection_db",
    "user": "ubuntu",
    "host": "localhost",
}


def vulnerable_login(username: str, password: str) -> list:
    """
    УЯЗВИМАЯ функция авторизации.
    Формирует SQL-запрос через конкатенацию строк —
    злоумышленник может внедрить произвольный SQL-код.
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # ОПАСНО: конкатенация пользовательского ввода в SQL-запрос
    query = (
        "SELECT * FROM users WHERE username = '"
        + username
        + "' AND password = '"
        + password
        + "'"
    )

    print(f"[УЯЗВИМЫЙ] Сформированный запрос:\n  {query}\n")
    cur.execute(query)
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows


def main():
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ УЯЗВИМОГО ВХОДА (конкатенация строк)")
    print("=" * 60)

    # Тест 1: Легитимный вход
    print("\n--- Тест 1: Легитимный вход (admin / 12345) ---")
    result = vulnerable_login("admin", "12345")
    print(f"  Найдено записей: {len(result)}")
    for row in result:
        print(f"  -> id={row[0]}, user={row[1]}, role={row[3]}")

    # Тест 2: Неверный пароль
    print("\n--- Тест 2: Неверный пароль (admin / wrong) ---")
    result = vulnerable_login("admin", "wrong")
    print(f"  Найдено записей: {len(result)}")

    # Тест 3: SQL-инъекция ' OR '1' = '1
    print("\n--- Тест 3: SQL-ИНЪЕКЦИЯ (admin / ' OR '1'='1) ---")
    result = vulnerable_login("admin", "' OR '1'='1")
    print(f"  Найдено записей: {len(result)}")
    for row in result:
        print(f"  -> id={row[0]}, user={row[1]}, role={row[3]}")

    if len(result) > 1:
        print("\n  !!! АТАКА УСПЕШНА: получены ВСЕ записи из таблицы !!!")


if __name__ == "__main__":
    main()
