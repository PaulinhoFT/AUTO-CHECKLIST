import tkinter as tk
from tkinter import messagebox
import pyautogui
import time
import os
import sys
import re

TEXTOS_PRONTOS = {
    "ALMOÇO": "Estou entrando em horário de almoço 🥗, mas para que seu atendimento continue estarei transferindo-o à outro atendente, ahh não precisa se preocupar ele já esta ciente do seu problema e dará continuidade.",
    "LENTIDÃO": "Essa dificuldade que você está enfrentando está relacionada a um serviço específico ou a um dispositivo em particular? Seria possível fornecer mais detalhes? Se achar mais conveniente, pode enviar um áudio explicando.",
    "LOS": "Vou precisar abrir um atendimento para encaminharmos um técnico até o local. Sua conexão alarmou LOS, quando isso acontece, pode se tratar de um problema no conector, modem ou fibra óptica.\nQual numero para contato? Me informe um ponto de referência do local por gentileza.",
    "TRANSFERENCIA DE SETOR": "Neste caso, precisarei transferir seu atendimento ao setor responsável, porem o mesmo só abre as 9hrs, peço aguarde que assim que o setor abrir estarei lhe transferindo.",
    "FIM DO EXPEDIENTE": "Meu expediente chegou ao fim.\nMas para que seu atendimento continue, estarei lhe transferindo para outro atendente.\nNão se preocupe, ele está ciente do problema e dará sequencia no seu atendimento.",
    "SIM ESTOU NO LOCAL": "Obrigado pela confirmação! Informei o técnico que você está no local para recebê-lo, ele já está a caminho para realizar o seu atendimento 😊",
    "NÃO ESTOU NO LOCAL": "Obrigado pela informação, saberia me informar quando terá alguém no local para solicitar o retorno do técnico ?",
    "SOLICITAR QUE ASSINANTE REINICIE O MODEM": "Realizei uma verificação em sua rede onde não identifiquei divergências, porem, fiz algumas modificações no seu aparelho de fibra visando melhor desempenho da sua rede. Por favor, tire da tomada o modem de fibra e ligue novamente. Após a conexão ser restabelecida, faça o teste novamente.",
    "EXPLICAÇÃO PONTO SECUNDARIO": "Neste caso, não conseguimos oferecer suporte para rede interna somente até o ponto principal da Trix Net, pois se trata de equipamentos particulares. Recomendamos que você entre em contato com um técnico de sua confiança para verificar o cabeamento, configuração e integridade dos seus dispositivos no ponto secundário.",
    "EXPLICAÇÃO TV BOX": "Vou lhe passar uma breve explicação sobre o funcionamento desses aparelhos TV Box.\n\nComo esses dispositivos utilizam servidores próprios para transmissão de imagem, podem ocorrer situações de instabilidade, lentidão ou travamentos, especialmente em horários de maior utilização. Além disso, o funcionamento depende diretamente do suporte e das atualizações disponibilizadas pelo fornecedor do aparelho.\n\nComo a dificuldade ocorre apenas no TV Box e os demais dispositivos funcionam normalmente, entendemos que sua conexão de internet está operando corretamente. Neste caso, recomendamos entrar em contato com o suporte do fabricante ou fornecedor do TV Box para verificar possíveis atualizações, configurações ou orientações específicas para o aparelho.",
    "EXPLICAÇÃO IPTV": "Vou lhe passar uma breve explicação sobre o funcionamento desses aplicativos de IPTV.\n\nOs serviços de IPTV utilizam servidores próprios para transmissão de imagem e, em alguns momentos, podem ocorrer instabilidades, lentidão ou travamentos, principalmente em horários de maior utilização. Além disso, o funcionamento do aplicativo depende das configurações, atualizações e suporte disponibilizados pelo fornecedor do serviço.\n\nComo a dificuldade ocorre apenas no IPTV e os demais dispositivos/aplicativos funcionam normalmente, entendemos que sua conexão de internet está operando corretamente. Neste caso, recomendamos entrar em contato com o suporte do serviço de IPTV para verificar possíveis atualizações, configurações ou orientações específicas para melhorar o funcionamento.",
    "TROCA SENHA WI-FI CASO NÃO SEJA ASSINANTE PARA CONFIRMAR DADOS": "Certo, como este numero de contato não está vinculado ao contrato, para que possamos estar alterando preciso da confirmação de alguns dados.\n\nNome completo do assinante.\nCPF/CNPJ completo do contrato.\nData de nascimento.\nEndereço completo.",
    "TROCA SENHA WI-FI CASO SEJA ASSINANTE": "Me informar uma senha nova que estarei alterando para você.\n\nOBS: senha do wi-fi pode ter os caracteres especiais: ! @ # _ - (nenhum além desses), não pode ter acentos e a senha tem que ter no mínimo 8 dígitos e também sem espaços.",
    "REALIZAREI A TROCA DA SENHA WI-FI": "Realizarei a troca da senha de sua rede Wi-Fi, assim que seu dispositivo desconectar, basta se conectar a rede Wi-Fi com a nova senha.\n\nSENHA ANTIGA: \nSENHA NOVA: ",
    "ORIENTAÇÃO TESTE DE VELOCIDADE": "Vou lhe fornecer uma breve explicação sobre o funcionamento das redes Wi-Fi e sobre o teste de velocidade.\n\nA rede 2.4G possui uma limitação de 70 Mbps devido à sua tecnologia mais antiga, mas oferece uma maior distância de alcance.\nPor outro lado, a rede 5G possui uma limitação maior, podendo atingir até 1000 Mbps dependendo do processamento do dispositivo, porém sua área de cobertura é menor.\n\nQuanto aos testes de velocidade, eles são bastante influenciados pelo desempenho do dispositivo utilizado e variam de acordo com a quantidade de aplicativos em execução. Para obter uma precisão maior, é recomendado utilizar um notebook ou computador com suporte para porta de internet gigabit e sem nenhum processo em aberto.",
    "DYINGGASP": "Verifiquei que seu modem de fibra consta como desligado no meu sistema, verifica se possui alguma luz acesa no aparelho de fibra, se tiver me valida se tem alguma vermelha, por favor.",
    "PROCEDIMENTOS NÃO AUTENTICA 1": "Verifiquei que sua conexão não está autenticada porem o sinal óptico está OK. Você está presente no local para que possamos realizar alguns procedimentos e verificações?",
    "PROCEDIMENTOS NÃO AUTENTICA 2": "Por favor, confirme se o nome da rede Wi-Fi permanece o mesmo. Nesta verificação, iremos ver se o roteador foi resetado ou não.",
    "PROCEDIMENTOS NÃO AUTENTICA 3": "Neste caso, o roteador não foi resetado. Agora, por favor, siga o seguinte procedimento, desconecte o roteador e o modem de fibra da tomada por 15 segundos e, em seguida, ligue-os novamente. Estarei monitorando aqui para verificar se a autenticação será restabelecida.",
    "PROCEDIMENTOS NÃO AUTENTICA 4": "Neste caso, o roteador foi resetado, eu posso estar tentando lhe orientando como reconfigurar o roteador ou posso estar encaminhando um tecnico ao local para verificação.",
    "PROCEDIMENTOS NÃO AUTENTICA 5": "Verifiquei que não subiu a autenticação, consegue me mandar uma foto dos cabos atras do roteador e do modem para validar se os cabos estão conectados corretamente, por favor.",
    "ABERTURA DE ATENDIMENTO FAST": "CAIXA: \n\nRECLAMAÇÃO: O(A) CLIENTE INFORMA QUE A CONEXÃO ESTÁ APRESENTANDO OSCILAÇÕES DE FORMA GERAL.\n\nPROCEDIMENTOS REALIZADOS: FOI VERIFICADO QUE NÃO HÁ DIVERGÊNCIAS NA REDE DO(A) CLIENTE. FORAM REALIZADOS TESTES E PROCEDIMENTOS REMOTOS, PORÉM O PROBLEMA AINDA PERSISTE.\n\nORIENTAÇÃO: NECESSÁRIO VALIDAR A CONEXÃO PRESENCIALMENTE NO LOCAL E REPASSAR ORIENTAÇÕES AO(À) CLIENTE.\n\nPPPOE: \n\nCONTATO: \n\nPONTO DE REF.: ",
    "ABERTURA DE ATENDIMENTO LOS": "#LOS#\n\nCAIXA: \n\nEMENDA: \n\nPPPOE: \n\nCONTATO: \n\nPONTO DE REF.: \n\nHISTÓRICO DE SINAL: ",
    "ABERTURA DE ATENDIMENTO DESCONTO": "DESCONTO\n\nQUANDO CAIU: \t\nQUANDO VOLTO: \nTEMPO FORA: \nDESCONTO CONCEDIDO:",
    "SOLICITAR PARA O ASSINANTE RECEBER O TEC NA FRENTE DA CASA": "Bom dia, referente ao atendimento aberto conosco o técnico está na frente da sua residência, teria alguém para estar recebendo o mesmo?",
    "CONTATO PARA TEC DE CAMPO, POR LIGAÇÃO SEM SUCESSO": "Tentativas de contato via ligação, sem sucesso.\n\nIniciado contato via chat.",
    "CONTATO PARA TEC DE CAMPO, SEM SUCESSO CHAT E LIGAÇÃO": "Tentativas de contato sem sucesso, tanto via chat como via ligação.",
    "IP PUBLICO": "IP Publico adicionado a rede;\nIP ATUAL: \nUsuario: \nSenha: \n\nInformo também que, devido à escassez de endereços IP no mundo, o IP público atribuído pode ser removido sem aviso prévio. Além disso, recomendo que, após a adição do IP público à sua rede, seja redobrada a atenção com a segurança da mesma, pois a rede estará se comunicando diretamente com a internet.",
    "QUANDO O TEC VEM ?": "Entre hoje ou amanhã, dependendo da demanda da equipe de campo, não consigo informar um horário específico para a chegada do técnico. Isso ocorre porque os técnicos seguem uma fila cronológica de atendimentos, e o tempo necessário para cada visita varia de acordo com a complexidade de cada caso. Só estar aguardando a visita.",
    "DISTANCIA DO SINAL WI-FI": "Neste caso, você está enfrentando dificuldades com o alcance do sinal Wi-Fi. Para resolver essa situação, há duas opções: a primeira seria reposicionar o equipamento para um local onde o sinal Wi-Fi seja mais necessário. A segunda opção seria realizar a instalação de uma rede interna, ou um roteador secundário no local para ampliar a área de cobertura do sinal Wi-Fi, porem nós não realizamos este tipo de serviço (de instalação de equipamentos particulares) onde seria necessário estar contatando um técnico particular para a estruturação de uma rede interna no local, como provedor de internet, nós prestamos suporte somente até o ponto principal."
}

def carregar_pre_registros():
    caminho_html = r"C:\Users\Paulo Felix\Documents\GitHub\CAT-SYSTEM-V2\pre-registros.html"
    pre_registros = {}
    try:
        if os.path.exists(caminho_html):
            with open(caminho_html, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            match_obj = re.search(r'const preRegistros = \{(.*?)\};', conteudo, re.DOTALL)
            if match_obj:
                obj_str = match_obj.group(1)
                itens = re.findall(r'(\d+):\s*`(.*?)`', obj_str, re.DOTALL)
                textos_dict = {k: v for k, v in itens}
                
                botoes = re.findall(r'<button[^>]*onclick="copyPreRegistro\((\d+)\)"[^>]*>(.*?)</button>', conteudo)
                
                for id_btn, titulo in botoes:
                    if id_btn in textos_dict:
                        pre_registros[titulo.strip()] = textos_dict[id_btn].replace('\\n', '\n')
    except Exception as e:
        print(f"Erro ao ler HTML: {e}")
    
    if not pre_registros:
        pre_registros = {
            "Botão 1 - Lentidão com att de firmware": "LENTIDÃO. \n \nVALIDADO QUE NÃO CONSTA DIVERGENCIA NA REDE DO ASSINANTE \nATIVADO TOPOLOGIA. \nATIVADO UPNP \nDNS 1: 168.121.96.141 \nDNS 2: 168.121.96.142 \nSNTP: 168.121.96.25 \n \nASSINANTE RELATA MELHORA APÓS ATUALIZAÇÃO DA FIRMWARE DA ONU.",
            "Botão 2 - Lentidão com reinicio de equipamento": "LENTIDÃO. \n \nVALIDADO QUE NÃO CONSTA DIVERGENCIA NA REDE DO ASSINANTE \nATIVADO TOPOLOGIA. \nATIVADO UPNP \nDNS 1: 168.121.96.141 \nDNS 2: 168.121.96.142 \nSNTP: 168.121.96.25\n\nASSINANTE RELATA MELHORA APÓS REINICIO DA ONU.",
            "Botão 3 - Conflito de rede interna": "VALIDADO QUE ASSINANTE ESTAVA COM CONFLITO DE REDE INTERNA.\nORIENTADO SOBRE O CONFLITO.\nTESTADO PONTO PRINCIPAL, TUDO OK.",
            "Botão 4 - Assinante sem internet (Tudo OK)": "VERIFICADO QUE NÃO POSSUI NENHUMA DIVERGENCIA NA REDE DO ASSINANTE.\nTESTADO E TUDO OK.",
            "Botão 5 - Teste de velocidade solucionado": "ASSINANTE RELATA NÃO RECEBER OS MEGAS. \nORIENTADO SOBRE AS REDES WI-FI E SOBRE O TESTE DE VELOCIDADE. \nTUDO OK.",
            "Botão 6 - Serviço não homologado (TVBOX/IPTV)": "VALIDADO QUE ASSINANTE POSSUI TVBOX/IPTV NÃO HOMOLOGADO.\nVALIDADO A CONEXÃO DE INTERNET TUDO OK.",
            "Botão 7 - Troca da senha Wi-Fi": "SENHA ANTIGA:  \nSENHA NOVA: \nCONTATO:",
            "Botão 8 - Não autentica solucionado interno": "VALIDADO QUE REDE DO ASSINANTE NÃO ESTAVA AUTENTICADA.\nREALIZADO PROCEDIMENTOS COM ASSINANTE, ONDE SUBIU A CONEXÃO.\nTESTADO E TUDO OK.",
            "Botão 9 - Inatividade (Não falou nada)": "ASSINANTE ENTROU EM CONTATO, POREM NÃO RELATOU NADA.\nATENDIMENTO FINALIZADO COM INATIVIDADE.",
            "Botão 10 - Envio de boleto": "ENVIADO BOLETO PARA ASSINANTE, CONFORME SOLICITADO.",
            "Botão 11 - Assinante enviou comprovante desbloqueio do assinante.": "ASSINANTE DESBLOQUEADO, CONFORME ENVIO DO COMPROVANTE."
        }
    return pre_registros

PRE_REGISTROS = carregar_pre_registros()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def executar_automacao():
    try:
        pyautogui.PAUSE = 0.01 
        
        arquivo = resource_path("coordenadas.txt")
        if not os.path.exists(arquivo):
            raise Exception("O arquivo 'coordenadas.txt' não foi encontrado!\n\nRode o programa 'capturar_coordenadas.py' primeiro.")
            
        with open(arquivo, "r") as f:
            linhas = f.read().strip().split("\n")
            
        if len(linhas) != 6:
            raise Exception("As coordenadas estão incompletas. Rode o 'capturar_coordenadas.py' novamente.")
            
        pontos = []
        for linha in linhas:
            x, y = linha.split(",")
            pontos.append((int(x), int(y)))
            
        pyautogui.click(pontos[0][0], pontos[0][1])
        time.sleep(0.3) 
        
        for i in range(1, 6):
            pyautogui.click(pontos[i][0], pontos[i][1])
            time.sleep(0.01) 
            
    except Exception as e:
        messagebox.showerror("Erro 5 cliques", str(e))

def executar_automacao_8_cliques():
    try:
        pyautogui.PAUSE = 0.01
        
        arquivo = resource_path("coordenadas_8_cliques.txt")
        if not os.path.exists(arquivo):
            raise Exception("O arquivo 'coordenadas_8_cliques.txt' não foi encontrado!\n\nRode o programa 'capturar_coordenadas_8.py' primeiro.")
            
        with open(arquivo, "r") as f:
            linhas = f.read().strip().split("\n")
            
        if len(linhas) != 8:
            raise Exception("As coordenadas estão incompletas. Rode o 'capturar_coordenadas_8.py' novamente.")
            
        pontos = []
        for linha in linhas:
            x, y = linha.split(",")
            pontos.append((int(x), int(y)))
            
        for i in range(8):
            pyautogui.click(pontos[i][0], pontos[i][1])
            if i == 3 or i == 5:
                time.sleep(2.0) 
            else:
                time.sleep(0.01) 
            
    except Exception as e:
        messagebox.showerror("Erro 8 cliques", str(e))

class AppFlutuante:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        
        self.menu_aberto = False
        self.janela_textos = None
        self.menu_pre_aberto = False
        self.janela_pre = None
        
        arquivo_pos = resource_path("posicao_botao.txt")
        if os.path.exists(arquivo_pos):
            with open(arquivo_pos, "r") as f:
                pos = f.read().strip()
                self.root.geometry(f"340x45{pos}") 
        else:
            self.root.geometry("340x45+300+300")
        
        self.root.configure(bg="#333333")
        self.x = 0
        self.y = 0
        
        self.frame_topo = tk.Frame(self.root, bg="#333333")
        self.frame_topo.pack(fill="both", expand=True)
        
        self.frame_topo.columnconfigure(0, weight=1, uniform="btn")
        self.frame_topo.columnconfigure(1, weight=1, uniform="btn")
        self.frame_topo.columnconfigure(2, weight=2)
        self.frame_topo.columnconfigure(3, weight=2)
        self.frame_topo.rowconfigure(0, weight=1)
        
        self.btn1 = tk.Button(self.frame_topo, text="⚡", command=executar_automacao, bg="#00C853", fg="white", font=("Segoe UI Emoji", 16), relief="flat", activebackground="#69F0AE", cursor="hand2")
        self.btn1.grid(row=0, column=0, sticky="nsew", padx=(1, 0), pady=1)
        
        self.btn2 = tk.Button(self.frame_topo, text="⭐", command=executar_automacao_8_cliques, bg="#2980B9", fg="white", font=("Segoe UI Emoji", 16), relief="flat", activebackground="#3498DB", cursor="hand2")
        self.btn2.grid(row=0, column=1, sticky="nsew", padx=1, pady=1)
        
        self.btn_textos = tk.Button(self.frame_topo, text="Textos ▼", command=self.toggle_textos, bg="#8E44AD", fg="white", font=("Arial", 11, "bold"), relief="flat", activebackground="#9B59B6", cursor="hand2")
        self.btn_textos.grid(row=0, column=2, sticky="nsew", padx=(0,1), pady=1)
        
        self.btn_pre_registros = tk.Button(self.frame_topo, text="Pré Registros ▼", command=self.toggle_pre_registros, bg="#D35400", fg="white", font=("Arial", 11, "bold"), relief="flat", activebackground="#E67E22", cursor="hand2")
        self.btn_pre_registros.grid(row=0, column=3, sticky="nsew", padx=(0,1), pady=1)
        
        for b in (self.btn1, self.btn2, self.btn_textos, self.btn_pre_registros):
            b.bind("<Button-3>", self.iniciar_arrasto)
            b.bind("<B3-Motion>", self.arrastar)
            b.bind("<ButtonRelease-3>", self.salvar_posicao)
            b.bind("<Double-Button-3>", lambda e: self.root.destroy())

    def toggle_textos(self):
        self.fechar_pre_se_aberto()
        if self.menu_aberto and self.janela_textos:
            self.janela_textos.destroy()
            self.janela_textos = None
            self.btn_textos.config(text="Textos ▼")
            self.menu_aberto = False
        else:
            self.abrir_janela_textos()
            self.btn_textos.config(text="Textos ▲")
            self.menu_aberto = True

    def fechar_textos_se_aberto(self):
        if self.menu_aberto and self.janela_textos:
            self.janela_textos.destroy()
            self.janela_textos = None
            self.btn_textos.config(text="Textos ▼")
            self.menu_aberto = False

    def toggle_pre_registros(self):
        self.fechar_textos_se_aberto()
        if self.menu_pre_aberto and self.janela_pre:
            self.janela_pre.destroy()
            self.janela_pre = None
            self.btn_pre_registros.config(text="Pré Registros ▼")
            self.menu_pre_aberto = False
        else:
            self.abrir_janela_pre_registros()
            self.btn_pre_registros.config(text="Pré Registros ▲")
            self.menu_pre_aberto = True

    def fechar_pre_se_aberto(self):
        if self.menu_pre_aberto and self.janela_pre:
            self.janela_pre.destroy()
            self.janela_pre = None
            self.btn_pre_registros.config(text="Pré Registros ▼")
            self.menu_pre_aberto = False

    def fechar_todos_menus(self):
        self.fechar_textos_se_aberto()
        self.fechar_pre_se_aberto()

    def abrir_janela_textos(self):
        self.janela_textos = tk.Toplevel(self.root)
        self.janela_textos.overrideredirect(True)
        self.janela_textos.attributes("-topmost", True)
        self.janela_textos.configure(bg="#333333")
        
        x = self.root.winfo_x()
        y = self.root.winfo_y() + 45
        
        # O painel de textos precisa ser largo suficiente (350px) para acomodar os títulos grandes e ter rolagem
        # Aumentamos a altura de 450 para 750 para mostrar mais opções na tela e reduzir o scroll
        self.janela_textos.geometry(f"350x750+{x}+{y}")
        
        borda = tk.Frame(self.janela_textos, bg="#8E44AD", bd=2)
        borda.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(borda, bg="#2b2b2b", highlightthickness=0)
        scrollbar = tk.Scrollbar(borda, orient="vertical", command=canvas.yview)
        
        scrollable_frame = tk.Frame(canvas, bg="#2b2b2b")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=326)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Permitir rolagem pelo mouse (MouseWheel)
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.janela_textos.bind("<MouseWheel>", _on_mousewheel)
        
        # Criando os 32 botões dinamicamente
        for nome, texto in TEXTOS_PRONTOS.items():
            btn = tk.Button(
                scrollable_frame, 
                text=nome, 
                font=("Arial", 9, "bold"), 
                bg="#424242", 
                fg="white", 
                relief="flat", 
                cursor="hand2", 
                anchor="w", 
                wraplength=310, # Permite que nomes grandes pulem de linha
                justify="left", 
                pady=5
            )
            btn.config(command=lambda t=texto, b=btn: self.copiar_texto(t, b))
            btn.pack(fill="x", padx=2, pady=(2, 0))

    def abrir_janela_pre_registros(self):
        self.janela_pre = tk.Toplevel(self.root)
        self.janela_pre.overrideredirect(True)
        self.janela_pre.attributes("-topmost", True)
        self.janela_pre.configure(bg="#333333")
        
        x = self.root.winfo_x()
        y = self.root.winfo_y() + 45
        
        self.janela_pre.geometry(f"350x500+{x}+{y}")
        
        borda = tk.Frame(self.janela_pre, bg="#D35400", bd=2)
        borda.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(borda, bg="#2b2b2b", highlightthickness=0)
        scrollbar = tk.Scrollbar(borda, orient="vertical", command=canvas.yview)
        
        scrollable_frame = tk.Frame(canvas, bg="#2b2b2b")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=326)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.janela_pre.bind("<MouseWheel>", _on_mousewheel)
        
        for nome, texto in PRE_REGISTROS.items():
            btn = tk.Button(
                scrollable_frame, 
                text=nome, 
                font=("Arial", 9, "bold"), 
                bg="#424242", 
                fg="white", 
                relief="flat", 
                cursor="hand2", 
                anchor="w", 
                wraplength=310,
                justify="left", 
                pady=5
            )
            btn.config(command=lambda t=texto, b=btn: self.copiar_texto(t, b))
            btn.pack(fill="x", padx=2, pady=(2, 0))

    def copiar_texto(self, texto, btn_widget):
        self.root.clipboard_clear()
        self.root.clipboard_append(texto)
        self.root.update()
        
        btn_widget.config(bg="#27AE60", text=f"Copiado! ✓")
        
        # Fecha automaticamente o painel flutuante após copiar
        self.root.after(400, self.fechar_todos_menus)

    def salvar_posicao(self, event):
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
        self.fechar_todos_menus()

    def arrastar(self, event):
        x = self.root.winfo_pointerx() - self.x
        y = self.root.winfo_pointery() - self.y
        tam_atual = self.root.geometry().split('+')[0]
        self.root.geometry(f"{tam_atual}+{x}+{y}")

# --- INICIALIZAÇÃO ---
root = tk.Tk()
app = AppFlutuante(root)
root.mainloop()
