# Auto Checklist 🚀

Automação em Python desenvolvida para marcar rapidamente os itens de um checklist no sistema Trixnet, poupando tempo e cliques repetitivos.

## Funcionalidades
- **Calibragem por Coordenadas**: Um assistente visual ensina o programa onde clicar no seu monitor.
- **Atalho Global**: Pressione `F9` a qualquer momento para rodar a automação sem precisar focar na janela.
- **Velocidade Turbo**: O script zera os delays de segurança internos, marcando o checklist inteiro na velocidade da luz.

## Como Usar
1. Instale as dependências:
   ```bash
   pip install pyautogui keyboard
   ```
2. Execute o assistente de calibragem **uma vez** para mapear sua tela:
   ```bash
   python capturar_coordenadas.py
   ```
3. Deixe o programa principal rodando em segundo plano:
   ```bash
   python automacao_checklist.py
   ```
4. Sempre que o checklist aparecer na tela, pressione **F9**!

## Arquivos
- `capturar_coordenadas.py`: Interface com timer de 3 segundos para gravar as posições exatas do mouse na tela.
- `automacao_checklist.py`: O robô principal que lê as coordenadas e dispara os cliques de forma instantânea.
