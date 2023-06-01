import sys
import pygame
import random
import pygame.mixer
import subprocess

Point = pygame.Vector2
# initialise pygame
pygame.init()

target = int(sys.argv[1])
acrescimo = int(sys.argv[2])
cor_agua = eval(sys.argv[3])

# target = 10
# acrescimo = -10
# cor_agua = (0,0,255,200)

# game window dimensions
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 800

# create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tsunami Run")

# set frame rate
clock = pygame.time.Clock()
FPS = 45


# game variables
SCROLL_THRESH = 200
GRAVITY = 0.9
MAX_PLATFORMS = 10
scroll = 0
game_over = False
fade_counter = 0
score = 0
scale = 1.5

#spritesheet
spritesheet = pygame.image.load('assets/spritesheet.png')

sprite_width = 32
sprite_height = 32
sprites = []

for j in range(spritesheet.get_height() // sprite_height):
    for i in range(spritesheet.get_width() // sprite_width):
        rect = pygame.Rect(i * sprite_width, j * sprite_height, sprite_width, sprite_height)
        sprite = spritesheet.subsurface(rect)
        sprite = pygame.transform.scale(sprite, (sprite_width*scale, sprite_height*scale))
        sprites.append(sprite)

# define font
font_path = ("assets/LuckiestGuy-Regular.ttf")
font_small = pygame.font.Font(font_path, 25)
font_big = pygame.font.Font(font_path, 30)

# load images
bg_image = pygame.image.load("assets/background.png").convert_alpha()
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
platform_image = pygame.image.load("assets/bricks.jpg").convert_alpha()
platform_image = pygame.transform.scale(platform_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.mixer.music.load("assets/RUST.mp3")
jump = pygame.mixer.Sound("assets/jump.mp3")
death = pygame.mixer.Sound("assets/death.mp3")
won = pygame.mixer.Sound("assets/win.mp3")
lose = pygame.mixer.Sound("assets/lose.mp3")
splash = pygame.mixer.Sound("assets/splash.mp3")
land = pygame.mixer.Sound("assets/land.mp3")
tsunami = pygame.mixer.Sound("assets/tsunami.mp3")
jump.set_volume(1.5)
lose.set_volume(0.2)
won.set_volume(0.2)
land.set_volume(0.1)
tsunami.set_volume(0.09)

text_outline_color = (50, 50, 50)
text_color = (200, 200, 200)
score_outline_color = (50, 50, 50)
score_color = (200, 200, 200)
wait_bg = (0,0,100)

def draw_text(text, font, text_col, x, y, outline_color, center=False, right_align=False):
    # Renderiza o texto principal
    img = font.render(text, True, text_col)
    
    # Renderiza o contorno do texto
    outline = font.render(text, True, outline_color)
    
    # Obtém o retângulo do texto para alinhar corretamente
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    elif right_align:
        rect.topright = (x, y)
    else:
        rect.topleft = (x, y)

    # Desenha o contorno primeiro
    for pos in [(rect.x-1, rect.y-1), (rect.x+1, rect.y-1), (rect.x-1, rect.y+1), (rect.x+1, rect.y+1)]:
        screen.blit(outline, pos)

    # Desenha o texto principal por cima do contorno
    screen.blit(img, rect)



# function for drawing the background
def draw_bg():
    screen.blit(bg_image, (0, 0))


class WaterSpring:
    def __init__(self, x=0, target_height=None):
        if not target_height:
            self.target_height = SCREEN_HEIGHT + 200
        else:
            self.target_height = target_height
        self.dampening = 0.05  # adjust accordingly
        self.tension = 0.1
        self.height = self.target_height
        self.vel = -5
        self.x = x

    def update(self):
        dh = self.target_height - self.height
        if abs(dh) < 0.01:
            self.height = self.target_height
        self.vel += self.tension * dh - self.vel * self.dampening
        self.height += self.vel

    def draw(self, surf: pygame.Surface):
        pygame.draw.circle(surf, "white", (self.x, self.height), 1)


class Wave:
    def __init__(self):
        diff = 20
        self.springs = [
            WaterSpring(x=i * diff + 0) for i in range(SCREEN_WIDTH // diff + 2)
        ]
        self.points = []
        self.diff = diff

    def get_spring_index_for_x_pos(self, x):
        return int(x // self.diff)

    def get_target_height(self):
        return self.springs[0].target_height

    def set_target_height(self, height):
        for i in self.springs:
            i.target_height = height

    def add_height(self, height):
        self.set_target_height(self.get_target_height() + height)

    def update(self):
        for i in self.springs:
            i.update()
        self.spread_wave()
        self.points = [Point(i.x, i.height) for i in self.springs]
        self.points.extend(
            [Point(SCREEN_WIDTH, SCREEN_HEIGHT), Point(0, SCREEN_HEIGHT)]
        )

    def draw(self, surf: pygame.Surface):
        pygame.draw.polygon(surf, cor_agua, self.points)

    def draw_line(self, surf: pygame.Surface):
        pygame.draw.lines(surf, "white", False, self.points[:-2], 5)

    def spread_wave(self):
        spread = 0.5
        for i in range(len(self.springs)):
            if i > 0:
                self.springs[i - 1].vel += spread * (
                    self.springs[i].height - self.springs[i - 1].height
                )
            try:
                self.springs[i + 1].vel += spread * (
                    self.springs[i].height - self.springs[i + 1].height
                )
            except IndexError:
                pass

    def splash(self, index, vel):
        try:
            self.springs[index].vel += vel
        except IndexError:
            pass


class Player:
    def __init__(self, x, y):
        self.sprite_stand = [sprites[11]]
        self.sprites_right = sprites[1:4]
        self.sprites_left = [pygame.transform.flip(sprite, True, False) for sprite in self.sprites_right]
        self.sprites_jump_start_right = [sprites[4]]
        self.sprites_jump_start_left = [pygame.transform.flip(sprite, True, False) for sprite in self.sprites_jump_start_right]
        self.sprites_jump_air_right = [sprites[5]]
        self.sprites_jump_air_left = [pygame.transform.flip(sprite, True, False) for sprite in self.sprites_jump_air_right]
        self.sprites_jump_fall_right = [sprites[6]]
        self.sprites_jump_fall_left = [pygame.transform.flip(sprite, True, False) for sprite in self.sprites_jump_fall_right]
        self.sprites_jump_land_right = [sprites[7]]
        self.sprites_jump_land_left = [pygame.transform.flip(sprite, True, False) for sprite in self.sprites_jump_land_right]
        self.image = self.sprite_stand[0]  # Imagem padrão é a sprite parado
        self.current_sprite_list = self.sprite_stand
        self.current_sprite_index = 0
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.last_direction = 'right'  # Armazene a última direção que o personagem se moveu
        self.can_jump = False  # Initialize the can_jump variable
        self.jumping = False
        self.falling = False
        self.land_counter = 0
        self.land_sound = False

    def move(self):
        # reset variables
        scroll = 0
        dx = 0
        dy = 0
        score = 0
        # process keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx = -10
            self.current_sprite_list = self.sprites_left
            self.last_direction = 'left'  # Atualize a última direção
        elif key[pygame.K_d]:
            dx = 10
            self.current_sprite_list = self.sprites_right
            self.last_direction = 'right'  # Atualize a última direção
        elif key[pygame.K_w] and self.can_jump:  # Check if the player can jump
            self.vel_y = -20  # Change this to the desired jump velocity
            jump.play()
            self.can_jump = False  # Set can_jump to False after jumping
            self.jumping = True
            self.land_sound = False
            score += 1 
        else:
            # Se o jogador não estiver se movendo, use a última direção para determinar para qual direção olhar
            if self.last_direction == 'left':
                self.current_sprite_list = [pygame.transform.flip(self.sprite_stand[0], True, False)]
            else:
                self.current_sprite_list = self.sprite_stand

        # If player is jumping
        if self.jumping:
            if self.last_direction == 'right':
                self.current_sprite_list = self.sprites_jump_start_right
            if self.last_direction == 'left':
                self.current_sprite_list = self.sprites_jump_start_left
            if self.vel_y < 0 and self.last_direction == 'right':
                self.current_sprite_list = self.sprites_jump_air_right
            elif self.vel_y < 0 and self.last_direction == 'left':
                self.current_sprite_list = self.sprites_jump_air_left
            elif self.vel_y > 0 and self.last_direction == 'right':
                self.falling = True
                self.current_sprite_list = self.sprites_jump_fall_right
            elif self.vel_y > 0 and self.last_direction == 'left':
                self.falling = True
                self.current_sprite_list = self.sprites_jump_fall_left
        # If player is falling
        if self.falling and self.can_jump:
            if self.land_sound == False:
                land.play()
                self.land_sound = True
            if self.last_direction == 'right':
                self.current_sprite_list = self.sprites_jump_land_right
            elif self.last_direction == 'left':
                self.current_sprite_list = self.sprites_jump_land_left
            if self.land_counter >= 30:
                self.jumping = False
                self.falling = False
                self.land_counter = 0
            self.land_counter += 1
            

        self.current_sprite_index += 1
        self.current_sprite_index %= len(self.current_sprite_list)  # Certifique-se de que o índice está sempre dentro do intervalo

        self.image = self.current_sprite_list[self.current_sprite_index]
        
        # gravity
        if not self.can_jump:
            self.vel_y += GRAVITY
        dy += self.vel_y
        
        # check collision with platforms
        for platform in platform_group:
            # collision in the y direction
            if platform.rect.colliderect(
                self.rect.x, self.rect.y + dy, self.width, self.height
            ):
                # check if above the platform
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.can_jump = True  # Set can_jump to True if the player is on a platform
                else:
                    self.can_jump = False  # Set can_jump to False if the player is not on a platform


        # ensure player doesn't go off the edge of the screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        # check if the player has bounced to the top of the screen
        if self.rect.top <= SCROLL_THRESH:
            # if player is jumping
            if self.vel_y < 0:
                scroll = -dy

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy + scroll

        return scroll, score

    
    def draw(self):
        screen.blit(self.image, (self.rect.x - 12, self.rect.y - 5))

# platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):

        # update platform's vertical position
        self.rect.y += scroll

        # check if platform has gone off the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

def draw_score_and_target():
    # render score
    draw_text(f'Score: {score}', font_small, score_color, 10, 20, score_outline_color)
    # render target
    draw_text(f'Objetivo: {target}', font_small, score_color, SCREEN_WIDTH - 10, 20, score_outline_color, right_align=True)


water_scroll = 0
# player instance
jumpy = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

# create sprite groups
platform_group = pygame.sprite.Group()

# create starting platform
platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100)
platform_group.add(platform)

wave = Wave()
s = pygame.Surface(screen.get_size(), pygame.SRCALPHA).convert_alpha()
# game loop
run = True
counter = 0
win = False
played = False
pygame.mixer.init()
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)
tsunami.play(-1)

while run:
    clock.tick(FPS)
    if game_over == False:
        scroll, score_temp = jumpy.move()
        score += score_temp
        water_scroll -= scroll
        # draw background
        draw_bg()

        if random.random() < 0.05:  # 1% chance each frame
            # Generate a random index for the left side of the screen
            left_index = 0
            # Generate a random velocity
            left_vel = random.random() * (-100)
            # Splash on the left side of the screen
            wave.splash(left_index, left_vel)

        if random.random() < 0.05:  # 1% chance each frame
            # Generate a random index for the right side of the screen
            right_index = 40
            # Generate a random velocity
            right_vel = random.random() * (-400)
            # Splash on the right side of the screen
            wave.splash(right_index, right_vel)

        # generate platforms
        if len(platform_group) < MAX_PLATFORMS:
            p_w = random.randint(40, 60)
            p_x = random.randint(0, SCREEN_WIDTH - p_w)
            p_y = platform.rect.y - random.randint(80, 120)
            platform = Platform(p_x, p_y, p_w)
            platform_group.add(platform)
        # update platforms
        platform_group.update(scroll)
        # draw sprites
        platform_group.draw(screen)

        wave.update()

        wave.points = [Point(i.x, i.height - water_scroll) for i in wave.springs]
        wave.points.extend(
            [Point(SCREEN_WIDTH, SCREEN_HEIGHT), Point(0, SCREEN_HEIGHT)]
        )

        s.fill(0)
        wave.draw(s)  # Adicione esta linha
        screen.blit(s, (0, 0))
        wave.draw_line(screen)
        water_rect = pygame.Rect(0, wave.get_target_height() - water_scroll, SCREEN_WIDTH, SCREEN_HEIGHT)

        if jumpy.rect.colliderect(water_rect):
            game_over = True
            splash.play()
        
        if counter == 5:
            wave.add_height(acrescimo)
            counter = 0
        counter += 1

        jumpy.draw()
        
        if score >= target:  # replace 'n' with the number of platforms needed to win
            win=True
            game_over = True  # this will end the game loop
        # check game over
        if jumpy.rect.top > SCREEN_HEIGHT:
            game_over = True
            death.play()
        
        draw_score_and_target()

    elif(win == True):
        if fade_counter < SCREEN_WIDTH:
            fade_counter += 5
            for y in range(0, SCREEN_HEIGHT//100, 2):
                pygame.draw.rect(screen, wait_bg, (0, y * 100, fade_counter, 100))
                pygame.draw.rect(screen, wait_bg, (SCREEN_WIDTH - fade_counter, (y + 1) * 100, fade_counter, 100))
        draw_text("Você Venceu!", font_big, text_color, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100, text_outline_color, center=True)
        draw_text("SCORE: " + str(score), font_small, text_color, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, text_outline_color, center=True)
        draw_text("Pressione ESPAÇO para reiniciar", font_small, text_color, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, text_outline_color, center=True)
        draw_text("Pressione M para retornar ao Menu", font_small, text_color, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, text_outline_color, center=True)
        if played == False:
            won.play()
            played = True

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            # reset variables
            game_over = False
            score = 0
            scroll = 0
            fade_counter = 0
            win = False
            # reposition jumpy
            jumpy.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
            # reset platforms
            platform_group.empty()
            # create starting platform
            platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100)
            platform_group.add(platform)
            wave.set_target_height(SCREEN_HEIGHT + 200)
            water_scroll = 0
            s.fill(0)
            wave.update()
            wave.draw(s)
            screen.blit(s, (0, 0))
            wave.draw_line(screen)
            wave = Wave()
            played = False
            s = pygame.Surface(screen.get_size(), pygame.SRCALPHA).convert_alpha()
    else:
        if fade_counter < SCREEN_WIDTH:
            fade_counter += 5
            for y in range(0, SCREEN_HEIGHT//100, 2):
                pygame.draw.rect(screen, wait_bg, (0, y * 100, fade_counter, 100))
                pygame.draw.rect(screen, wait_bg, (SCREEN_WIDTH - fade_counter, (y + 1) * 100, fade_counter, 100))
            draw_text("GAME OVER!", font_big, text_color, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100, text_outline_color, center=True)
            draw_text("SCORE: " + str(score), font_small, text_color, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, text_outline_color, center=True)
            draw_text("Pressione ESPAÇO para reiniciar", font_small, text_color, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, text_outline_color, center=True)
            draw_text("Pressione M para ir ao Menu", font_small, text_color, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, text_outline_color, center=True)
            if played == False:
                lose.play()
                played = True

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            # reset variables
            game_over = False
            score = 0
            scroll = 0
            win = False
            fade_counter = 0
            # reposition jumpy
            jumpy.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
            # reset platforms
            platform_group.empty()
            # create starting platform
            platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100)
            platform_group.add(platform)
            wave.set_target_height(SCREEN_HEIGHT + 200)
            water_scroll = 0
            s.fill(0)
            wave.update()
            wave.draw(s)
            screen.blit(s, (0, 0))
            wave.draw_line(screen)
            wave = Wave()
            played = False
            s = pygame.Surface(screen.get_size(), pygame.SRCALPHA).convert_alpha()
        if key[pygame.K_m]:
            run = False
            # retorna ao menu
    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update display window
    pygame.display.update()


pygame.quit()
