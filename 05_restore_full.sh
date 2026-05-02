#!/bin/bash
# =============================================================
# Задание №5: Восстановление из полной резервной копии
# =============================================================

# Восстановление всей базы данных из полной копии
psql -d practice_db < ~/backups/full_backup.sql

echo "Восстановление из полной копии выполнено."

# Проверка количества записей
psql -d practice_db -c "SELECT 'users' AS table_name, COUNT(*) FROM users UNION ALL SELECT 'orders', COUNT(*) FROM orders;"
