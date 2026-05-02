#!/bin/bash
# =============================================================
# Задание №5: Частичное резервное копирование (отдельных таблиц)
# =============================================================

# Создаём директорию для резервных копий
mkdir -p ~/backups

# Частичное резервное копирование — только таблица users
pg_dump -t users practice_db > ~/backups/partial_backup_users.sql

# Частичное резервное копирование — только таблица orders
pg_dump -t orders practice_db > ~/backups/partial_backup_orders.sql

echo "Частичное резервное копирование выполнено:"
ls -lh ~/backups/partial_backup_users.sql
ls -lh ~/backups/partial_backup_orders.sql
