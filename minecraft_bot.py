"""
Minecraft TLauncher Bot
=======================
Автоматично:
1. Відкриває TLauncher
2. Вибирає Forge 1.16.5
3. Заходить на перший сервер у списку
4. Натискає компас → "Гриферское выживание" → "4 гриф"

Залежності:
    pip install pyautogui pillow pygetwindow keyboard

Підготовка:
    - Зроби скріншоти кнопок і збережи їх у папку ./images/
    - Список потрібних зображень описаний нижче у IMAGES
"""

import pyautogui
import pygetwindow as gw
import time
import subprocess
import sys
import os
import keyboard

# ──────────────────────────────────────────────
# НАЛАШТУВАННЯ — змінюй під себе
# ──────────────────────────────────────────────

TLAUNCHER_PATH = r"C:\Users\%USERNAME%\AppData\Roaming\.tlauncher\TLauncher.exe"
# Або вкажи повний шлях, наприклад:
# TLAUNCHER_PATH = r"C:\Program Files\TLauncher\TLauncher.exe"

# Затримки між діями (секунди)
DELAY_AFTER_LAUNCH   = 15   # чекаємо поки TLauncher завантажиться
DELAY_AFTER_LOGIN    = 60   # чекаємо поки Minecraft запуститься
DELAY_AFTER_JOIN     = 30   # чекаємо поки завантажиться сервер
DELAY_SHORT          = 2    # коротка пауза між кліками

# Папка зі скріншотами кнопок для розпізнавання
IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")

# Словник зображень для пошуку на екрані
# Ключ — назва, значення — ім'я файлу в папці images/
IMAGES = {
    "forge_version":   "forge_1165.png",       # кнопка/текст "Forge 1.16.5" у TLauncher
    "play_button":     "play_button.png",       # кнопка "Грати" / "Play" у TLauncher
    "multiplayer":     "multiplayer.png",       # кнопка "Мультиплеєр" у головному меню
    "first_server":    "first_server.png",      # перший сервер у списку (або просто фон)
    "join_button":     "join_server.png",       # кнопка "Підключитися"
    "compass":         "compass.png",           # іконка компаса на сервері
    "grifer_survival": "grifer_survival.png",   # кнопка "Гриферское выживание"
    "grif_4":          "grif_4.png",            # кнопка "4 гриф"
}

# ──────────────────────────────────────────────
# УТИЛІТИ
# ──────────────────────────────────────────────

pyautogui.FAILSAFE = True   # миша в кут екрану — зупинити скрипт
pyautogui.PAUSE    = 0.3    # пауза між будь-якими pyautogui діями


def img(name: str) -> str:
    """Повертає повний шлях до файлу зображення."""
    return os.path.join(IMAGES_DIR, IMAGES[name])


def find_and_click(image_name: str,
                   confidence: float = 0.85,
                   timeout: int = 30,
                   description: str = "") -> bool:
    """
    Шукає зображення на екрані і клікає по ньому.
    Повторює спроби кожну секунду до timeout секунд.
    Повертає True якщо знайдено і натиснуто.
    """
    desc = description or image_name
    print(f"[~] Шукаю: {desc}...")

    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            location = pyautogui.locateCenterOnScreen(img(image_name),
                                                      confidence=confidence)
            if location:
                pyautogui.click(location)
                print(f"[✓] Натиснуто: {desc}")
                return True
        except pyautogui.ImageNotFoundException:
            pass
        except Exception as e:
            print(f"[!] Помилка пошуку '{desc}': {e}")

        time.sleep(1)

    print(f"[✗] Не знайдено: {desc} (timeout {timeout}s)")
    return False


def wait_for_window(title_fragment: str, timeout: int = 60) -> bool:
    """Чекає поки з'явиться вікно з заданим підрядком у назві."""
    print(f"[~] Чекаю вікно: '{title_fragment}'...")
    deadline = time.time() + timeout
    while time.time() < deadline:
        windows = gw.getWindowsWithTitle(title_fragment)
        if windows:
            windows[0].activate()
            print(f"[✓] Вікно знайдено: {windows[0].title}")
            return True
        time.sleep(1)
    print(f"[✗] Вікно '{title_fragment}' не з'явилось")
    return False


def focus_minecraft():
    """Переводить фокус на вікно Minecraft."""
    for title in ["Minecraft", "minecraft"]:
        wins = gw.getWindowsWithTitle(title)
        if wins:
            wins[0].activate()
            time.sleep(0.5)
            return True
    return False


# ──────────────────────────────────────────────
# КРОКИ БОТА
# ──────────────────────────────────────────────

def step_open_tlauncher():
    """Крок 1: Відкриваємо TLauncher."""
    print("\n=== Крок 1: Відкриваємо TLauncher ===")
    path = os.path.expandvars(TLAUNCHER_PATH)

    if not os.path.exists(path):
        print(f"[!] TLauncher не знайдено за шляхом:\n    {path}")
        print("    Відредагуй змінну TLAUNCHER_PATH у скрипті.")
        sys.exit(1)

    subprocess.Popen([path])
    print(f"[✓] TLauncher запущено. Чекаємо {DELAY_AFTER_LAUNCH}с...")
    time.sleep(DELAY_AFTER_LAUNCH)


def step_select_forge():
    """Крок 2: Вибираємо версію Forge 1.16.5 і тиснемо Грати."""
    print("\n=== Крок 2: Вибираємо Forge 1.16.5 ===")

    if not wait_for_window("TLauncher", timeout=30):
        print("[!] TLauncher не відкрився.")
        sys.exit(1)

    # Клік на дропдаун версій і вибір Forge 1.16.5
    if not find_and_click("forge_version",
                          confidence=0.80,
                          timeout=20,
                          description="Forge 1.16.5"):
        print("[!] Не вдалось вибрати версію. Переконайся що зображення forge_1165.png правильне.")
        sys.exit(1)

    time.sleep(DELAY_SHORT)

    # Тиснемо кнопку "Грати"
    if not find_and_click("play_button",
                          confidence=0.85,
                          timeout=10,
                          description="Кнопка Грати"):
        sys.exit(1)

    print(f"[~] Чекаємо запуск Minecraft ({DELAY_AFTER_LOGIN}с)...")
    time.sleep(DELAY_AFTER_LOGIN)


def step_join_first_server():
    """Крок 3: Заходимо на перший сервер у списку."""
    print("\n=== Крок 3: Заходимо на сервер ===")

    focus_minecraft()
    time.sleep(1)

    # Мультиплеєр
    if not find_and_click("multiplayer",
                          confidence=0.82,
                          timeout=30,
                          description="Мультиплеєр"):
        sys.exit(1)

    time.sleep(DELAY_SHORT * 2)

    # Перший сервер у списку — подвійний клік або кнопка Join
    # Спробуємо знайти перший сервер і подвійно клікнути
    if not find_and_click("first_server",
                          confidence=0.75,
                          timeout=15,
                          description="Перший сервер"):
        print("[!] Спробуємо знайти кнопку 'Підключитися' напряму...")

    time.sleep(DELAY_SHORT)

    # Кнопка підключитися
    if not find_and_click("join_button",
                          confidence=0.82,
                          timeout=10,
                          description="Підключитися"):
        # Якщо кнопка не знайшлась — пробуємо Enter
        print("[~] Пробуємо Enter замість кнопки...")
        pyautogui.press("enter")

    print(f"[~] Чекаємо завантаження сервера ({DELAY_AFTER_JOIN}с)...")
    time.sleep(DELAY_AFTER_JOIN)


def step_navigate_menu():
    """Крок 4: Компас → Гриферское выживание → 4 гриф."""
    print("\n=== Крок 4: Навігація в меню сервера ===")

    focus_minecraft()
    time.sleep(1)

    # Відкриваємо інвентар або меню (залежить від сервера)
    # Якщо компас у хотбарі — просто клікаємо по ньому
    if not find_and_click("compass",
                          confidence=0.80,
                          timeout=20,
                          description="Компас"):
        print("[!] Компас не знайдено. Можливо потрібно відкрити інвентар (E).")
        pyautogui.press("e")
        time.sleep(1)
        if not find_and_click("compass",
                              confidence=0.78,
                              timeout=10,
                              description="Компас (в інвентарі)"):
            sys.exit(1)

    time.sleep(DELAY_SHORT)

    # Гриферское выживание
    if not find_and_click("grifer_survival",
                          confidence=0.80,
                          timeout=15,
                          description="Гриферское выживание"):
        sys.exit(1)

    time.sleep(DELAY_SHORT)

    # 4 гриф
    if not find_and_click("grif_4",
                          confidence=0.80,
                          timeout=15,
                          description="4 гриф"):
        sys.exit(1)

    print("\n[✓✓✓] Бот успішно виконав всі дії!")


# ──────────────────────────────────────────────
# ГОЛОВНА ФУНКЦІЯ
# ──────────────────────────────────────────────

def main():
    print("=" * 50)
    print("  Minecraft TLauncher Bot")
    print("=" * 50)
    print("Натисни F10 у будь-який момент щоб зупинити бота.\n")

    # Перевіряємо наявність папки з зображеннями
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
        print(f"[!] Папку images/ створено: {IMAGES_DIR}")
        print("    Поклади туди скріншоти кнопок (список нижче):")
        for key, fname in IMAGES.items():
            print(f"      {fname}  ←  {key}")
        print("\n    Як зробити скріншот кнопки:")
        print("    1. Запусти TLauncher / Minecraft вручну")
        print("    2. Зроби знімок екрану (Win+Shift+S)")
        print("    3. Обріж тільки саму кнопку/текст")
        print("    4. Збережи з відповідним ім'ям у папку images/")
        sys.exit(0)

    # Хоткей зупинки
    keyboard.add_hotkey("F10", lambda: (print("\n[!] Зупинено користувачем."),
                                        sys.exit(0)))

    # Виконуємо кроки
    step_open_tlauncher()
    step_select_forge()
    step_join_first_server()
    step_navigate_menu()


if __name__ == "__main__":
    main()
