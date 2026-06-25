import pyautogui
import time
import sys

print("Pressione Ctrl+C para sair.")
print("Mova o mouse para a posição que deseja mapear...\n")

try:
    while True:
        x, y = pyautogui.position()
        position_str = f'Posição atual do mouse: X: {x:4d} | Y: {y:4d}'
        print(position_str, end='')
        print('\b' * len(position_str), end='', flush=True)
        time.sleep(0.1)
except KeyboardInterrupt:
    print('\nConcluído.')
    sys.exit()
