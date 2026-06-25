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

class AppFlutuante:
    def __init__(self, root):
        self.root = root
        
        # Remove a barra de título do Windows para ficar um botão limpo
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        
        # Tenta carregar a última posição em que o usuário deixou o botão
        arquivo_pos = resource_path("posicao_botao.txt")
        if os.path.exists(arquivo_pos):
            with open(arquivo_pos, "r") as f:
                pos = f.read().strip()
                self.root.geometry(f"45x45{pos}")
        else:
            self.root.geometry("45x45+300+300")
        
        # Cor da borda
        self.root.configure(bg="#333333")
        
        # Variáveis para arrastar a janela
        self.x = 0
        self.y = 0
        
        # Botão principal
        self.btn = tk.Button(
            self.root, 
            text="⚡", 
            command=executar_automacao, 
            bg="#00C853", 
            fg="white", 
            font=("Segoe UI Emoji", 16), 
            relief="flat",
            activebackground="#69F0AE",
            cursor="hand2"
        )
        self.btn.pack(expand=True, fill="both", padx=1, pady=1)
        
        self.btn.bind("<Button-3>", self.iniciar_arrasto)
        self.btn.bind("<B3-Motion>", self.arrastar)
        self.btn.bind("<ButtonRelease-3>", self.salvar_posicao) # Salva ao soltar o mouse
        
        # Para fechar o programa, o usuário dá um duplo clique com o BOTÃO DIREITO
        self.btn.bind("<Double-Button-3>", lambda e: self.root.destroy())

    def salvar_posicao(self, event):
        # geometry() retorna algo como "45x45+1920+100", pegamos só o final
        atual = self.root.geometry()
        pos = atual[atual.find('+'):] 
        arquivo_pos = resource_path("posicao_botao.txt")
        try:
            with open(arquivo_pos, "w") as f:
                f.write(pos)
        except:
            pass

    def iniciar_arrasto(self, event):
        self.x = event.x
        self.y = event.y

    def arrastar(self, event):
        x = self.root.winfo_pointerx() - self.x
        y = self.root.winfo_pointery() - self.y
        self.root.geometry(f"+{x}+{y}")

# --- INICIALIZAÇÃO ---
root = tk.Tk()

# Ativa o atalho F9
if keyboard:
    keyboard.add_hotkey('F9', disparar_atalho)
else:
    print("Módulo keyboard não encontrado. Atalho F9 desativado.")

app = AppFlutuante(root)
root.mainloop()
