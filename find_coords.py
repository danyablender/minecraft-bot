"""
find_coords.py — помічник для знаходження координат
====================================================
Запусти цей скрипт, наводь мишу на кнопки в TLauncher/Minecraft
і дивись які координати виводяться в консоль.
Скопіюй їх у COORDS в minecraft_bot.py

Зупинити: Ctrl+C
"""

import pyautogui
import time

print("Наводь мишу на кнопки. Координати оновлюються щосекунди.")
print("Ctrl+C щоб зупинити\n")

try:
    while True:
        x, y = pyautogui.position()
        print(f"X: {x:4d}   Y: {y:4d}", end="\r")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nГотово!")
