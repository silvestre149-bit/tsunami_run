import pygame
from pygame.locals import *

pygame.init()
largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Escapando do Tsunami")

cor_fundo = (0, 0, 0)  # preto
cor_texto = (255, 255, 255)  # branco

class Botao:
    def __init__(self, x, y, largura, altura, cor, texto, acao=None):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.cor = cor
        self.texto = texto
        self.acao = acao

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, (self.x, self.y, self.largura, self.altura))
        fonte = pygame.font.SysFont(None, 32)
        texto = fonte.render(self.texto, True, cor_fundo)
        pos_texto = texto.get_rect(center=(self.x + self.largura / 2, self.y + self.altura / 2))
        tela.blit(texto, pos_texto)

    def executar_acao(self):
        if self.acao:
            self.acao()

def tratar_eventos_menu(botoes):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                for botao in botoes:
                    if botao.x < event.pos[0] < botao.x + botao.largura and botao.y < event.pos[1] < botao.y + botao.altura:
                        botao.executar_acao()

def iniciar_jogo():
    print("Iniciando o jogo...")

def mostrar_como_jogar():
    print("Como jogar...")

def mostrar_sobre():
    print("Sobre...")

def exibir_menu():
    botoes = []
    botao_iniciar = Botao(300, 200, 200, 50, cor_texto, "Iniciar Jogo", iniciar_jogo)
    botao_como_jogar = Botao(300, 275, 200, 50, cor_texto, "Como Jogar", mostrar_como_jogar)
    botao_sobre = Botao(300, 350, 200, 50, cor_texto, "Sobre", mostrar_sobre)
    botao_sair = Botao(300, 425, 200, 50, cor_texto, "Sair", pygame.quit)
    botoes.append(botao_iniciar)
    botoes.append(botao_como_jogar)
    botoes.append(botao_sobre)
    botoes.append(botao_sair)

    while True:
        tratar_eventos_menu(botoes)
        tela.fill(cor_fundo)
        for botao in botoes:
            botao.desenhar(tela)
        pygame.display.update()

if __name__ == "__main__":
    exibir_menu()
