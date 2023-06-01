import pygame
from pygame.locals import *
import pygame.mixer
import subprocess
import sys

pygame.init()
pygame.mixer.music.load("assets/RUST.mp3")
largura_tela = 450
altura_tela = 800
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Escapando do Tsunami")

cor_fundo = (20, 20, 20)  # preto
background = pygame.image.load("assets/background.png")
background = pygame.transform.scale(background, (largura_tela, altura_tela))
click = pygame.mixer.Sound("assets/click.mp3")
hover = pygame.mixer.Sound("assets/hover.mp3")
hover.set_volume(0.5)

pygame.mixer.init()

pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)
cor_texto = (200, 200, 200)  # branco

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
        self.played = False

    def desenhar(self, tela, sprite_borda, pos_mouse):
        sprite_borda_redimensionada = pygame.transform.scale(sprite_borda, (self.largura, self.altura))
        tela.blit(sprite_borda_redimensionada, (self.x, self.y))

        cor = self.cor
        if self.x < pos_mouse[0] < self.x + self.largura and self.y < pos_mouse[1] < self.y + self.altura:
            cor = self.cor_hover
            if not self.played:
                hover.play()
                self.played = True

        else:
            self.played = False

        pygame.draw.rect(tela, cor, (self.x, self.y, self.largura, self.altura))
        pygame.draw.rect(tela, cor_fundo, (self.x, self.y, self.largura, self.altura), 2)

        fonte = pygame.font.Font("assets/LuckiestGuy-Regular.ttf", 28)
        texto = fonte.render(self.texto, True, cor_fundo)
        pos_texto = texto.get_rect(center=(self.x + self.largura / 2, self.y + self.altura / 2 + 3))
        tela.blit(texto, pos_texto)

    def executar_acao(self):
        if self.acao:
            click.play()
            self.acao()

def tratar_eventos_menu(botoes):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                for botao in botoes:
                    if botao.x < event.pos[0] < botao.x + botao.largura and botao.y < event.pos[1] < botao.y + botao.altura:
                        botao.executar_acao()

    sprite_borda = pygame.image.load("assets/Button.png")
    pos_mouse = pygame.mouse.get_pos()  # obter a posição do mouse
    for botao in botoes:
        botao.desenhar(tela, sprite_borda, pos_mouse)  # passar a posição do mouse para o método desenhar do botão

def iniciar_jogo1():
    dificuldade = ['30', '-5', '(0,255,255,50)', '1']
    # Executa o arquivo game.py
    pygame.mixer.music.stop()
    subprocess.run([sys.executable, "game.py"] + dificuldade)
    pygame.mixer.music.play()
    # Fecha o menu.py
    sys.exit()

def iniciar_jogo2():
    dificuldade = ['50', '-10', '(0,0,255,50)', '2']
    # Executa o arquivo game.py
    pygame.mixer.music.stop()
    subprocess.run([sys.executable, "game.py"] + dificuldade)
    pygame.mixer.music.play()
    # Fecha o menu.py
    sys.exit()

def iniciar_jogo3():
    dificuldade = ['100', '-15', '(255,0,0,50)', '3']
    # Executa o arquivo game.py
    pygame.mixer.music.stop()
    subprocess.run([sys.executable, "game.py"] + dificuldade)
    pygame.mixer.music.play()
    # Fecha o menu.py
    sys.exit()

def mostrar_como_jogar():
    exibir_menu_como_jogar()

def mostrar_sobre():
    print("Sobre...")

def exibir_menu():
    botoes = []
    sprite_borda = pygame.image.load("assets/Button.png")  # Carregar a imagem da sprite de borda

    botao_iniciar = Botao(125, 200, 200, 50, cor_texto, "Iniciar Jogo", exibir_menu_niveis)
    botao_como_jogar = Botao(125, 275, 200, 50, cor_texto, "Como Jogar", mostrar_como_jogar)
    botao_sobre = Botao(125, 350, 200, 50, cor_texto, "Sobre", mostrar_sobre)
    botao_sair = Botao(125, 425, 200, 50, cor_texto, "Sair", pygame.quit)

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
        tela.blit(sprite_fundo, (75, 150))  # Desenha a sprite de fundo atrás dos botões
        for botao in botoes:
            botao.desenhar(tela, sprite_borda, pygame.mouse.get_pos())  # Passar a posição do mouse para o método desenhar do botão
        pygame.display.update()

def exibir_menu_niveis():
    botoes_niveis = []
    sprite_borda = pygame.image.load("assets/Button.png")  # Carregar a imagem da sprite de borda

    botao_nivel1 = Botao(125, 200, 200, 50, cor_texto, "Nível 1", iniciar_jogo1)
    botao_nivel2 = Botao(125, 275, 200, 50, cor_texto, "Nível 2", iniciar_jogo2)
    botao_nivel3 = Botao(125, 350, 200, 50, cor_texto, "Nível 3", iniciar_jogo3)
    botao_voltar = Botao(125, 425, 200, 50, cor_texto, "Voltar", exibir_menu)

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
        tela.blit(sprite_fundo, (75, 150))  # Desenha a sprite de fundo atrás dos botões
        for botao in botoes_niveis:
            botao.desenhar(tela, sprite_borda, pygame.mouse.get_pos())  # Passar a posição do mouse para o método desenhar do botão
        pygame.display.update()


def exibir_menu_como_jogar():
    tela.fill(cor_fundo)
    sprite_fundo = pygame.image.load("assets/back_op.png")
    sprite_fundo = pygame.transform.scale(sprite_fundo, (300, 375))
    tela.blit(sprite_fundo, (75, 150))

    fonte_como_jogar = pygame.font.Font("assets/LuckiestGuy-Regular.ttf", 12)
    texto_como_jogar = fonte_como_jogar.render("Para jogar, utilize as teclas do teclado WASD", True, cor_texto)
    pos_texto_como_jogar = texto_como_jogar.get_rect(center=(largura_tela // 2, 200))
    tela.blit(texto_como_jogar, pos_texto_como_jogar)

    texto_wasd = fonte_como_jogar.render("Conforme imagem abaixo:", True, cor_texto)
    pos_texto_wasd = texto_wasd.get_rect(center=(largura_tela // 2, 225))
    tela.blit(texto_wasd, pos_texto_wasd)

    imagem_wasd = pygame.image.load("assets/wasd.png")
    nova_largura = 275
    nova_altura = 250
    imagem_wasd = pygame.transform.scale(imagem_wasd, (nova_largura, nova_altura))
    pos_imagem_wasd = imagem_wasd.get_rect(center=(largura_tela // 2, 375))
    tela.blit(imagem_wasd, pos_imagem_wasd)

    sprite_borda = pygame.image.load("assets/Button.png")
    botao_voltar = Botao(125, 600, 200, 50, cor_texto, "Voltar", exibir_menu)
    botao_voltar.desenhar(tela, sprite_borda, pygame.mouse.get_pos())

    while True:
        tratar_eventos_menu([botao_voltar])
        pygame.display.update()

if __name__ == "__main__":
    exibir_menu()
