#!/bin/bash

# TODO: расширить. В установке планировщика делается гораздо больше вещей

# Деинсталляция add_task через pipx
echo "Uninstalling the add_task project using pipx..."
pipx uninstall add_task

# Удаление скрипта из целевой директории
TARGET_DIR="${HOME}/.local/opt/add_task_script"
echo "Removing script from ${TARGET_DIR}..."
rm -rf "$TARGET_DIR"

# Удаление задач из crontab
echo "Cleaning up crontab..."
(crontab -l | grep -v "$TARGET_DIR/run_task.sh" | crontab -)
(crontab -l | grep -v "/usr/sbin/anacron" | crontab -)

echo "Cleanup complete."
