"""
hotkey_launcher.py
==================
Запускає minecraft_bot.py по гарячій клавіші.
Постав в автозапуск Windows — і бот завжди під рукою.

Гарячі клавіші:
  F6  — запустити бота
  F7  — зупинити бота
"""

import keyboard
import subprocess
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BOT_PATH = os.path.join(SCRIPT_DIR, "minecraft_bot.py")

bot_process = None

def start_bot():
    global bot_process
    if bot_process and bot_process.poll() is None:
        print("[!] Бот вже запущений!")
        return
    print("[✓] Запускаю бота...")
    bot_process = subprocess.Popen(["python", BOT_PATH])

def stop_bot():
    global bot_process
    if bot_process and bot_process.poll() is None:
        bot_process.terminate()
        print("[✓] Бота зупинено.")
    else:
        print("[!] Бот не запущений.")

print("=" * 35)
print("  Hotkey Launcher")
print("=" * 35)
print("F6 — запустити бота")
print("F7 — зупинити бота")
print("F8 — вийти з лаунчера")
print()

keyboard.add_hotkey("F6", start_bot)
keyboard.add_hotkey("F7", stop_bot)
keyboard.add_hotkey("F8", lambda: sys.exit(0))

keyboard.wait()
