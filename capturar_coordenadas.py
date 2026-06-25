import tkinter as tk
from tkinter import messagebox
import pyautogui
import time
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

class Capturador:
    def __init__(self, root):
        self.root = root
        self.root.title("Calibrar Tela")
        self.root.geometry("450x200")
        self.root.attributes("-topmost", True)
        
        self.lbl_status = tk.Label(root, text="Clique em Iniciar para gravar as posições do seu sistema.", font=("Arial", 11), wraplength=430, justify="center")
        self.lbl_status.pack(pady=20)
        
        self.btn_iniciar = tk.Button(root, text="Iniciar Captura", command=self.iniciar_captura, font=("Arial", 12, "bold"), bg="#FF9800", fg="white")
        self.btn_iniciar.pack(pady=10)
        
    def countdown_and_capture(self, item_name):
        for i in range(3, 0, -1):
            self.lbl_status.config(text=f"Posicione o mouse em: {item_name}\nCapturando em {i} segundo(s)...")
            self.root.update()
            time.sleep(1)
        
        x, y = pyautogui.position()
        self.lbl_status.config(text=f"{item_name} CAPTURADO! (X:{x}, Y:{y})")
        self.root.update()
        time.sleep(1)
        return x, y

    def iniciar_captura(self):
        self.btn_iniciar.config(state=tk.DISABLED)
        coordenadas = []
        
        try:
            # 1. Checklist
            x, y = self.countdown_and_capture("Botão 'Checklist'")
            coordenadas.append(f"{x},{y}")
            
            self.lbl_status.config(text="Se o checklist estiver fechado, por favor abra-o agora.\nAguardando 4 segundos para você se preparar...")
            self.root.update()
            time.sleep(4)
            
            # 2. Caixas
            for i in range(1, 6):
                x, y = self.countdown_and_capture(f"Caixinha {i}")
                coordenadas.append(f"{x},{y}")
                
            # Salvar
            filepath = resource_path("coordenadas.txt")
            with open(filepath, "w") as f:
                f.write("\n".join(coordenadas))
                
            messagebox.showinfo("Sucesso", "Todas as posições foram salvas com sucesso!\nPode fechar esta janela e rodar o automacao_checklist.py")
            self.root.destroy()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao capturar: {e}")
            self.btn_iniciar.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = Capturador(root)
    root.mainloop()
