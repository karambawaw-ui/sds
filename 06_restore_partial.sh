#!/bin/bash
# =============================================================
# Задание №5: Восстановление из частичной резервной копии
# =============================================================

# Восстановление таблицы users из частичной копии
psql -d practice_db < ~/backups/partial_backup_users.sql

# Восстановление таблицы orders из частичной копии
psql -d practice_db < ~/backups/partial_backup_orders.sql

echo "Восстановление из частичных копий выполнено."

# Проверка количества записей
psql -d practice_db -c "SELECT 'users' AS table_name, COUNT(*) FROM users UNION ALL SELECT 'orders', COUNT(*) FROM orders;"
