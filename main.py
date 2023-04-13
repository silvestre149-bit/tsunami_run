import pygame
import random

# Configurações iniciais
width, height = 800, 600
cell_size = 3
grid_width, grid_height = width // cell_size, height // cell_size
max_water_amount = 40
block_size = 50

# Inicializando o Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Criando a grade e preenchendo com água
grid = [[random.randint(0, max_water_amount) for _ in range(grid_width)] for _ in range(grid_height)]

# Adicionando o bloco à simulação
block_x, block_y = grid_width // 2, 0
block_speed = 1

# Função para atualizar a grade e o bloco
def update_grid_and_block(grid, block_x, block_y):
    new_grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

    for y in range(grid_height - 1, -1, -1):
        for x in range(grid_width):
            water_amount = grid[y][x]

            if water_amount > 0:
                # Primeiro, tente mover a água para baixo (gravidade)
                if y < grid_height - 1:
                    remaining_space = max_water_amount - new_grid[y + 1][x]
                    transfer_amount = min(water_amount, remaining_space)
                    new_grid[y + 1][x] += transfer_amount
                    water_amount -= transfer_amount

                # Em seguida, tente mover a água para os lados
                for dx in [-1, 1]:
                    if 0 <= x + dx < grid_width:
                        remaining_space = max_water_amount - new_grid[y][x + dx]
                        transfer_amount = min(water_amount // 2, remaining_space)
                        new_grid[y][x + dx] += transfer_amount
                        water_amount -= transfer_amount

                # Mantenha o restante da água na célula atual
                new_grid[y][x] += water_amount

    # Atualizar a posição do bloco e gerar uma onda na superfície da água
    block_y += block_speed
    if block_y >= grid_height * cell_size - block_size:
        block_y = grid_height * cell_size - block_size
    else:
        grid_y = block_y // cell_size
        for y in range(grid_y - 1, grid_y + 2):
            for x in range(block_x - block_size // cell_size // 2, block_x + block_size // cell_size // 2 + 1):
                if 0 <= y < grid_height and 0 <= x < grid_width:
                    new_grid[y][x] = min(max_water_amount, new_grid[y][x] + 5)

    return new_grid, block_x, block_y

    # Função para desenhar a grade e o bloco na tela
def draw_grid_and_block(grid, block_x, block_y, screen):
    for y in range(grid_height):
        for x in range(grid_width):
            water_amount = grid[y][x]
            color = (0, 0, min(255, 100 + water_amount * 3))
            pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))

    pygame.draw.rect(screen, (150, 75, 0), (block_x * cell_size, block_y, block_size, block_size))

# Loop principal do jogo
running = True
while running:
    # Processando eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualizando a grade e o bloco
    grid, block_x, block_y = update_grid_and_block(grid, block_x, block_y)

    # Desenhando a grade e o bloco na tela
    screen.fill((255, 255, 255))
    draw_grid_and_block(grid, block_x, block_y, screen)
    pygame.display.flip()

    # Limitando a taxa de quadros
    clock.tick(30)

pygame.quit()