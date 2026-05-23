import pyautogui, subprocess, time, sys, os, keyboard

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
    print(f"[+] Click: {name} -> ({x}, {y})")
    if double: pyautogui.doubleClick(x, y)
    elif right: pyautogui.rightClick(x, y)
    else: pyautogui.click(x, y)
    time.sleep(DELAY_CLICK)

def wait(s, r=""):
    print(f"[~] Wait {s}s {r}")
    time.sleep(s)

keyboard.add_hotkey("F10", lambda: sys.exit(0))

if not os.path.exists(TLAUNCHER_PATH):
    print(f"[!] Not found: {TLAUNCHER_PATH}")
    sys.exit(1)

print("=== Starting TLauncher ===")
subprocess.Popen([TLAUNCHER_PATH])
wait(DELAY_AFTER_LAUNCH, "TLauncher")

print("=== Click Play ===")
click("play_button")
wait(DELAY_AFTER_PLAY, "Minecraft")

print("=== Multiplayer ===")
click("multiplayer")
wait(3)
click("first_server", double=True)
wait(DELAY_AFTER_JOIN, "server")

print("=== Compass -> Grif ===")
pyautogui.rightClick()
wait(2)
click("grifer_survival")
wait(2)
for i in range(5):
    print(f"[+] Grif 4 - {i+1}/5")
    click("grif_4")
    wait(1)
print("[OK] Done!")
print("[~] Keeping alive...")
while True:
    time.sleep(60)
