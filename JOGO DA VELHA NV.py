# Importa o módulo tkinter para criar a interface gráfica
import tkinter as tk
# Importa o módulo messagebox para exibir caixas de diálogo
from tkinter import messagebox

# Função para inicializar o tabuleiro
def inicializar_tabuleiro():
    """
    Cria uma matriz 3x3 representando o tabuleiro do jogo.
    Cada célula começa com um espaço vazio (" ").
    """
    return [[" " for _ in range(3)] for _ in range(3)]

# Função para desenhar (atualizar) o tabuleiro na interface
def desenhar_tabuleiro():
    """
    Atualiza os textos dos botões da interface com base no estado atual do tabuleiro.
    """
    for i in range(3):
        for j in range(3):
            botoes[i][j].config(text=tabuleiro[i][j], state=tk.NORMAL)

# Função para verificar se há um vencedor
def verificar_vencedor():
    """
    Verifica se há um vencedor no jogo.
    Retorna "X", "O" se houver vencedor, ou None se ainda não houver.
    """
    # Verifica cada linha
    for linha in tabuleiro:
        if linha[0] == linha[1] == linha[2] and linha[0] != " ":
            return linha[0]
    
    # Verifica cada coluna
    for coluna in range(3):
        if tabuleiro[0][coluna] == tabuleiro[1][coluna] == tabuleiro[2][coluna] and tabuleiro[0][coluna] != " ":
            return tabuleiro[0][coluna]
    
    # Verifica as diagonais
    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] and tabuleiro[0][0] != " ":
        return tabuleiro[0][0]
    if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] and tabuleiro[0][2] != " ":
        return tabuleiro[0][2]
    
    # Retorna None se não houver vencedor
    return None

# Função para verificar se houve empate
def verificar_empate():
    """
    Verifica se todas as células do tabuleiro estão preenchidas
    e não há vencedor (empate).
    Retorna True se for empate, ou False se ainda há jogadas possíveis.
    """
    for linha in tabuleiro:
        if " " in linha:  # Se ainda houver espaços vazios
            return False
    return True

# Função chamada quando um botão é clicado
def clique_botao(linha, coluna):
    """
    Executa a ação correspondente ao clique de um botão no tabuleiro.
    """
    global jogador_atual  # Jogador atual (X ou O)

    # Verifica se a célula clicada está vazia
    if tabuleiro[linha][coluna] == " ":
        # Marca o movimento no tabuleiro e atualiza o botão
        tabuleiro[linha][coluna] = jogador_atual
        botoes[linha][coluna].config(text=jogador_atual, state=tk.DISABLED)

        # Verifica se há um vencedor
        vencedor = verificar_vencedor()
        if vencedor:
            # Atualiza o placar, exibe mensagem de vitória e pergunta para próxima rodada
            atualizar_placar(vencedor)
            messagebox.showinfo("Jogo da Velha", f"Jogador {vencedor} venceu!")
            perguntar_nova_rodada()
        elif verificar_empate():
            # Exibe mensagem de empate e pergunta para próxima rodada
            messagebox.showinfo("Jogo da Velha", "Empate!")
            perguntar_nova_rodada()
        else:
            # Troca o jogador e atualiza o tabuleiro
            jogador_atual = "O" if jogador_atual == "X" else "X"
            desenhar_tabuleiro()

# Função para atualizar o placar
def atualizar_placar(vencedor):
    """
    Atualiza o placar global com base no jogador vencedor.
    """
    global placar_x, placar_o
    if vencedor == "X":
        placar_x += 1
    elif vencedor == "O":
        placar_o += 1
    # Atualiza o rótulo do placar na interface
    rotulo_placar.config(text=f"Placar - X: {placar_x} | O: {placar_o}")

# Função para perguntar ao usuário se deseja jogar novamente
def perguntar_nova_rodada():
    """
    Exibe uma caixa de diálogo para perguntar se o jogador quer jogar outra rodada.
    """
    resposta = messagebox.askquestion("Fim de Jogo", "Quer jogar outra rodada?", icon='question')
    if resposta == "yes":
        reiniciar_jogo()  # Reseta o tabuleiro para começar nova rodada
    else:
        janela_principal.quit()  # Encerra o aplicativo

# Função para resetar o jogo
def reiniciar_jogo():
    """
    Reseta o tabuleiro e inicia uma nova rodada com o jogador "X".
    """
    global tabuleiro, jogador_atual
    tabuleiro = inicializar_tabuleiro()  # Reinicia o tabuleiro
    jogador_atual = "X"  # Define "X" como o primeiro jogador
    desenhar_tabuleiro()  # Atualiza a interface

# Criação da janela principal
janela_principal = tk.Tk()
janela_principal.title("Jogo da Velha")  # Define o título da janela

# Variáveis globais do jogo
tabuleiro = inicializar_tabuleiro()  # Tabuleiro inicial
jogador_atual = "X"  # Jogador inicial
placar_x = 0  # Placar do jogador X
placar_o = 0  # Placar do jogador O

# Rótulo para exibir o placar
rotulo_placar = tk.Label(janela_principal, text=f"Placar - X: {placar_x} | O: {placar_o}", font=("Arial", 14))
rotulo_placar.grid(row=0, column=0, columnspan=3)  # Posiciona o rótulo na interface

# Criação dos botões para o tabuleiro
botoes = [[None for _ in range(3)] for _ in range(3)]  # Matriz para armazenar os botões
for i in range(3):
    for j in range(3):
        # Cria um botão para cada célula do tabuleiro
        botoes[i][j] = tk.Button(janela_principal, text=" ", font=("Arial", 40), width=5, height=2, 
                                  command=lambda i=i, j=j: clique_botao(i, j))
        botoes[i][j].grid(row=i+1, column=j)  # Posiciona o botão na interface

# Inicia o loop principal da interface gráfica
janela_principal.mainloop()
