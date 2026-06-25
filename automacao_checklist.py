import tkinter as tk
from tkinter import messagebox
import pyautogui
import time
import os
import sys

# Tenta importar o keyboard (necessário para atalhos globais)
try:
    import keyboard
except ImportError:
    keyboard = None

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def executar_automacao():
    try:
        pyautogui.PAUSE = 0.01 # Zera o atraso padrão de segurança do PyAutoGUI
        
        arquivo = resource_path("coordenadas.txt")
        if not os.path.exists(arquivo):
            raise Exception("O arquivo 'coordenadas.txt' não foi encontrado!\n\nPor favor, rode o programa 'capturar_coordenadas.py' primeiro para ensinar ao programa onde ele deve clicar.")
            
        # Lê as coordenadas salvas
        with open(arquivo, "r") as f:
            linhas = f.read().strip().split("\n")
            
        if len(linhas) != 6:
            raise Exception("As coordenadas estão incompletas. Por favor, rode o 'capturar_coordenadas.py' novamente.")
            
        pontos = []
        for linha in linhas:
            x, y = linha.split(",")
            pontos.append((int(x), int(y)))
            
        # 1. Clica na palavra Checklist
        pyautogui.click(pontos[0][0], pontos[0][1])
        time.sleep(0.3) # Tempo ultra rápido só para o menu descer
        
        # 2. Clica nas 5 caixinhas (Modo Metralhadora)
        for i in range(1, 6):
            pyautogui.click(pontos[i][0], pontos[i][1])
            time.sleep(0.01) # Quase zero de pausa entre os cliques
            
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def disparar_atalho():
    # Ao pressionar F12 em qualquer lugar, manda o Tkinter executar a função
    root.after(0, executar_automacao)

# Configuração da Interface Gráfica
root = tk.Tk()
root.title("Auto Checklist")
root.geometry("380x160")
root.attributes("-topmost", True)

label = tk.Label(root, text="Automação por Coordenadas", font=("Arial", 12, "bold"))
label.pack(pady=10)

btn = tk.Button(root, text="Marcar Checklist (F9)", command=executar_automacao, 
                bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), 
                padx=20, pady=10, cursor="hand2")
btn.pack(pady=5)

rodape = tk.Label(root, text="Dica: Deixe a janela aberta e pressione F9 a qualquer momento.", font=("Arial", 9), fg="#666666")
rodape.pack()

# Ativa o atalho F9 se a biblioteca estiver instalada
if keyboard:
    keyboard.add_hotkey('F9', disparar_atalho)
else:
    messagebox.showwarning("Atalho F9", "Para o F9 funcionar, abra seu terminal e instale a biblioteca digitando:\n\npip install keyboard")

root.mainloop()
