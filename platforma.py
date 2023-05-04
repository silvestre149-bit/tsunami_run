import pygame
from pygame.locals import *
import random

pygame.init()

# Define as dimensões da janela
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Define a cor de fundo da janela
BACKGROUND_COLOR = (255, 255, 255)

# Carrega a imagem de fundo
background_image = pygame.image.load('2.png')

# Transforma a imagem para o tamanho da janela
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Define a velocidade do jogador e a velocidade da gravidade
PLAYER_SPEED = 5
GRAVITY = 0.4
JUMP_FORCE = 10

# Cria a janela
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Define o título da janela
pygame.display.set_caption('Meu Jogo')

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.vel_x = 0
        self.vel_y = 0
        self.is_jumping = False
        self.image = pygame.image.load("sprite_0.png").convert_alpha()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect(x=self.x, y=self.y)

    def move(self, keys_pressed, platforms):
        if keys_pressed[K_a]:
            self.vel_x = -PLAYER_SPEED
        elif keys_pressed[K_d]:
            self.vel_x = PLAYER_SPEED
        else:
            self.vel_x = 0

        if keys_pressed[K_w] and not self.is_jumping:
            self.is_jumping = True
            self.vel_y = -JUMP_FORCE

        self.vel_y += GRAVITY

        self.x += self.vel_x
        self.y += self.vel_y

        # Atualiza o retângulo do jogador para refletir sua nova posição
        self.rect.x = self.x
        self.rect.y = self.y

        if self.y >= WINDOW_HEIGHT - self.height:
            self.is_jumping = False
            self.y = WINDOW_HEIGHT - self.height - 1
            self.vel_y = 0

        # Verifica a colisão do jogador com as plataformas
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.is_jumping = False
                            

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = random.randint(50, 100)
        self.height = 12
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 255), self.rect)

class Ground(Platform):
    def __init__(self):
        super().__init__(0, WINDOW_HEIGHT - 10)  # Chama o construtor da classe Platform
        self.image = pygame.image.load("Tile_37.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (WINDOW_WIDTH, self.image.get_height()))
        self.rect = self.image.get_rect(x=self.x, y=WINDOW_HEIGHT - self.height)

    def draw(self, surface):
        surface.blit(self.image, self.rect)  # Desenha o sprite do chão na tela

ground = Ground()

# Gera as plataformas aleatoriamente
platforms = []
for i in range(random.randint(5, 10)):
    platform = Platform(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))
    platforms.append(platform)

player = Player(100, 100)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    keys_pressed = pygame.key.get_pressed()

    player.move(keys_pressed, platforms)

    
    window.fill(BACKGROUND_COLOR)
    window.blit(background_image,(0,0))
    
    #Desenha o chão
    ground.draw(window)

    # Desenha as plataformas na tela
    for platform in platforms:
        platform.draw(window)

    player.draw(window)

    pygame.display.update()

    clock.tick(60)
