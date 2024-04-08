#!/bin/bash


# Установка переменной PATH
export PATH=$PATH:$HOME/.local/bin

# Случайная задержка
sleep $((RANDOM % 900))
# echo $((RANDOM % 900)) >> test.txt

# Выполнение команды
echo 'run add_task'
add_task --date=today
