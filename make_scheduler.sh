#!/bin/bash

# Is pipx installed?
# You have to install it mannualy
if ! command -v pipx &> /dev/null; then
    echo "pipx is not installed."
    echo "Please install pipx using 'pip install pipx' and then run 'pipx ensurepath'"
    exit 1
fi

# Install add_task 
echo "Installing the add_task project using pipx..."
pipx install .

# Определение пути к целевой директории
TARGET_DIR="${HOME}/.local/opt/add_task_script"

# Проверка существования директории и создание, если не существует
if [ ! -d "$TARGET_DIR" ]; then
    mkdir -p "$TARGET_DIR"
fi

# Путь к исходному скрипту
SOURCE_SCRIPT="run_task.sh"

# Копирование скрипта в целевую директорию
cp "$SOURCE_SCRIPT" "$TARGET_DIR"

# Делаем скрипт исполняемым
chmod +x "${TARGET_DIR}/run_task.sh"

echo "Скрипт успешно скопирован в ${TARGET_DIR}/run_task.sh"


(crontab -l 2>/dev/null; echo "0 10 * * * $TARGET_DIR/run_task.sh > ${HOME}/logfile.log 2>&1") | crontab -
mkdir -p ~/.local/var/spool/anacron 
mkdir -p ~/.local/etc && cp /etc/anacrontab ~/.local/etc
(crontab -l 2>/dev/null; echo "0 * * * *  /usr/sbin/anacron -s -t \"${HOME}/.local/etc/anacrontab\" -S \"${HOME}/.local/var/spool/anacron\"") | crontab -


ANACRONTAB_FILE="${HOME}/.local/etc/anacrontab"
USERNAME=$(whoami)

# Проверяем и обновляем HOME, если необходимо
if grep -q "HOME=" "$ANACRONTAB_FILE"; then
    # Если строка с HOME найдена, обновляем ее
    sed -i "s|HOME=.*|HOME=${HOME}|g" "$ANACRONTAB_FILE"
else
    # Если строка с HOME не найдена, добавляем ее
    echo "HOME=${HOME}" >> "$ANACRONTAB_FILE"
fi

# Проверяем и обновляем LOGNAME, если необходимо
if grep -q "LOGNAME=" "$ANACRONTAB_FILE"; then
    # Если строка с LOGNAME найдена, обновляем ее
    sed -i "s|LOGNAME=.*|LOGNAME=${USERNAME}|g" "$ANACRONTAB_FILE"
else
    # Если строка с LOGNAME не найдена, добавляем ее
    echo "LOGNAME=${USERNAME}" >> "$ANACRONTAB_FILE"
fi

# Проверяем и обновляем RANDOM_DELAY, если необходимо
if grep -q "RANDOM_DELAY=" "$ANACRONTAB_FILE"; then
    # Если строка с RANDOM_DELAY найдена, обновляем ее
    sed -i "s|RANDOM_DELAY=.*|RANDOM_DELAY=15|g" "$ANACRONTAB_FILE"
else
    # Если строка с LOGNAME не найдена, добавляем ее
    echo "RANDOM_DELAY=15" >> "$ANACRONTAB_FILE"
fi