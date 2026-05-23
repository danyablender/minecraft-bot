import pyautogui, pygetwindow as gw, subprocess, time, sys, os, keyboard

TLAUNCHER_PATH = r"C:\Users\danya_dgvjdwc\AppData\Roaming\.minecraft\TLauncher.exe"
DELAY_AFTER_LAUNCH = 20
DELAY_AFTER_PLAY = 30
DELAY_AFTER_JOIN = 15
DELAY_CLICK = 1.5

COORDS = {
    "play_button":     (1111, 819),
    "multiplayer":     (965, 571),
    "first_server":    (950, 370),
    "grifer_survival": (922, 461),
    "grif_4":          (919, 391),
}

pyautogui.FAILSAFE = True

def click(name, double=False, right=False):
    x, y = COORDS[name]
    print(f"[+] Клік: {name} -> ({x}, {y})")
    if double: pyautogui.doubleClick(x, y)
    elif right: pyautogui.rightClick(x, y)
    else: pyautogui.click(x, y)
    time.sleep(DELAY_CLICK)

def wait(s, r=""):
    print(f"[~] Чекаємо {s}с {r}")
    time.sleep(s)

keyboard.add_hotkey("F10", lambda: sys.exit(0))

if not os.path.exists(TLAUNCHER_PATH):
    print(f"[!] Не знайдено: {TLAUNCHER_PATH}")
    sys.exit(1)

print("=== Запускаємо TLauncher ===")
subprocess.Popen([TLAUNCHER_PATH])
wait(DELAY_AFTER_LAUNCH, "TLauncher")

print("=== Тиснемо Грати ===")
click("play_button")
wait(DELAY_AFTER_PLAY, "Minecraft")

print("=== Мультиплеєр ===")
click("multiplayer")
wait(3)
click("first_server", double=True)
wait(DELAY_AFTER_JOIN, "сервер")

print("=== Компас -> Гриф ===")
pyautogui.rightClick()
wait(2)
click("grifer_survival")
wait(2)
for i in range(5):
    print(f"[+] Гриф 4 - {i+1}/5")
    click("grif_4")
    wait(1)
print("[OK] Готово!")
