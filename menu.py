import pygame
from pygame.locals import *
import pygame.mixer
import subprocess


pygame.init()
#pygame.mixer.init()
#pygame.mixer.music.load("assets/RUST.mp3")
#pygame.mixer.music.play(-1)
largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Escapando do Tsunami")

cor_fundo = (0, 0, 0)  # preto
background = pygame.image.load("assets/back_blue.jpg")
background = pygame.transform.scale(background, (largura_tela, altura_tela))


cor_texto = (255, 255, 255)  # branco

class Botao:
    def __init__(self, x, y, largura, altura, cor, texto, acao=None):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.cor = cor
        self.cor_hover = (4, 125, 155)  # cor de destaque
        self.texto = texto
        self.acao = acao

    def desenhar(self, tela, sprite_borda, pos_mouse):
        sprite_borda_redimensionada = pygame.transform.scale(sprite_borda, (self.largura, self.altura))
        tela.blit(sprite_borda_redimensionada, (self.x, self.y))

        cor = self.cor
        if self.x < pos_mouse[0] < self.x + self.largura and self.y < pos_mouse[1] < self.y + self.altura:
            cor = self.cor_hover

        pygame.draw.rect(tela, cor, (self.x, self.y, self.largura, self.altura))
        pygame.draw.rect(tela, cor_fundo, (self.x, self.y, self.largura, self.altura), 2)

        fonte = pygame.font.Font("assets/Montserrat-Black.ttf", 28)
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

    sprite_borda = pygame.image.load("assets/Button.png")
    pos_mouse = pygame.mouse.get_pos()  # obter a posição do mouse
    for botao in botoes:
        botao.desenhar(tela, sprite_borda, pos_mouse)  # passar a posição do mouse para o método desenhar do botão

def iniciar_jogo():
    print("Iniciando o jogo...")
    subprocess.call(["python", "game.py"])


def mostrar_como_jogar():
    print("Como jogar...")

def mostrar_sobre():
    print("Sobre...")

def exibir_menu():
    botoes = []
    sprite_borda = pygame.image.load("assets/Button.png")  # Carregar a imagem da sprite de borda

    botao_iniciar = Botao(300, 200, 200, 50, cor_texto, "Iniciar Jogo", exibir_menu_niveis)
    botao_como_jogar = Botao(300, 275, 200, 50, cor_texto, "Como Jogar", mostrar_como_jogar)
    botao_sobre = Botao(300, 350, 200, 50, cor_texto, "Sobre", mostrar_sobre)
    botao_sair = Botao(300, 425, 200, 50, cor_texto, "Sair", pygame.quit)

    botoes.append(botao_iniciar)
    botoes.append(botao_como_jogar)
    botoes.append(botao_sobre)
    botoes.append(botao_sair)

    # Carregar a sprite de fundo dos botões
    sprite_fundo = pygame.image.load("assets/back_op.png")
    sprite_fundo = pygame.transform.scale(sprite_fundo, (300, 375))  # Ajustar o tamanho da sprite para cobrir os botões

    while True:
        tratar_eventos_menu(botoes)
        tela.blit(background, (0, 0))  # Desenha a imagem de fundo na tela
        tela.blit(sprite_fundo, (250, 150))  # Desenha a sprite de fundo atrás dos botões
        for botao in botoes:
            botao.desenhar(tela, sprite_borda, pygame.mouse.get_pos())  # Passar a posição do mouse para o método desenhar do botão
        pygame.display.update()

def exibir_menu_niveis():
    botoes_niveis = []
    sprite_borda = pygame.image.load("assets/Button.png")  # Carregar a imagem da sprite de borda

    botao_nivel1 = Botao(300, 200, 200, 50, cor_texto, "Nível 1", iniciar_jogo)
    botao_nivel2 = Botao(300, 275, 200, 50, cor_texto, "Nível 2", iniciar_jogo)
    botao_nivel3 = Botao(300, 350, 200, 50, cor_texto, "Nível 3", iniciar_jogo)
    botao_voltar = Botao(300, 425, 200, 50, cor_texto, "Voltar", exibir_menu)

    botoes_niveis.append(botao_nivel1)
    botoes_niveis.append(botao_nivel2)
    botoes_niveis.append(botao_nivel3)
    botoes_niveis.append(botao_voltar)

    # Carregar a sprite de fundo dos botões
    sprite_fundo = pygame.image.load("assets/back_op.png")
    sprite_fundo = pygame.transform.scale(sprite_fundo, (300, 375))  # Ajustar o tamanho da sprite para cobrir os botões

    while True:
        tratar_eventos_menu(botoes_niveis)
        tela.blit(background, (0, 0))  # Desenha a imagem de fundo na tela
        tela.blit(sprite_fundo, (250, 150))  # Desenha a sprite de fundo atrás dos botões
        for botao in botoes_niveis:
            botao.desenhar(tela, sprite_borda, pygame.mouse.get_pos())  # Passar a posição do mouse para o método desenhar do botão
        pygame.display.update()

if __name__ == "__main__":
    exibir_menu()
