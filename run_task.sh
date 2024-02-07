#!/bin/bash


# Установка переменной PATH
export PATH=$PATH:$HOME/.local/bin

# Случайная задержка
sleep $((RANDOM % 900))
# echo $((RANDOM % 900)) >> test.txt

# Выполнение команды
add_task --date=today
