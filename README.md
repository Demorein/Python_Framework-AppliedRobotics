<center>

# 🚀 Python Framework: AppliedRobotics

</center>

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-GPL2.0-red.svg)

**Простой Python-фреймворк для управления роботами AppliedRobotics**

*Создан для студентов — чтобы сосредоточиться на логике, а не на низкоуровневых деталях*

</div>

---

## ✨ Возможности

| Функция | Описание |
|---------|-----------|
| 🤖 **Поддержка двух роботов** | Управление роботами M1 и M2 одновременно |
| 🎯 **Точное позиционирование** | Плавное перемещение в заданные координаты |
| 🏓 **Работа с объектами** | Захват и отпускание шариков с палеток |
| 🅿️ **Паркинг** | Автоматическое перемещение в зону парковки |
| 📊 **Мониторинг состояния** | Получение текущих координат |

---

## 🚀 Быстрая установка

### 1. Скачайте последнюю версию
Перейдите во вкладку **Releases** и скачайте архив с фреймворком

### 2. Перенесите файлы в проект
```bash
📁 your_project/
├── 📄 ar_framework.py    # ← Перенести из архива
├── 📄 config.py          # ← Перенести из архива  
└── 📄 main.py            # Ваш основной код
```

## 💡 Быстрый страт

``` Python
import ar_framework # Модуль который вы положили в свою папку проекта
import config # Конфиг

# Создаём объект робота M1
Robot_M1 = ar_framework.Robots(iptables=config.iptables, type="M1")

# Посмотреть, где робот стоит сейчас
print(Robot_M1.Robot.get_all_position())  # -> (200, 0, 90)

# Переместить робота на новые координаты
Robot_M1.Robot.move_to(150, 150, 50)  # Робот поедет в точку x=150, y=150, z=50

# Посмотреть текущие координаты
print("X:", Robot_M1.Robot.get_position().x) # -> X:150
print("Y:", Robot_M1.Robot.get_position().y) # -> Y:150
print("Z:", Robot_M1.Robot.get_position().z) # -> Z:50

# Робот берёт шарик
Robot_M1.Robot.pick_ball()

# Робот кладёт шарик
Robot_M1.Robot.drop_ball()

# Отправляем робота на парковку
Robot_M1.Robot.go_to_parking()
```

## 🤝 Пример с двумя роботами

``` Python
import ar_framework
import config

Robot_M1 = ar_framework.Robots(iptables=config.iptables, type="M1")
Robot_M2 = ar_framework.Robots(iptables=config.iptables, type="M2")

Robot_M1.Robot.move_to(150, 150, 50)
Robot_M2.Robot.move_to(140, -180, 90)

print(Robot_M1.Robot.get_all_position())  # -> (150, 150, 50)
print(Robot_M2.Robot.get_all_position())  # -> (140, -180, 90)
```