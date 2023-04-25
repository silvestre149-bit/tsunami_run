import pygame
import random

# Configurações iniciais
width, height = 800, 600
cell_size = 4
grid_width, grid_height = width // cell_size, height // cell_size
max_water_amount = 50

# Inicializando o Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Criando a grade e preenchendo com água
grid = [[random.randint(0, max_water_amount) for _ in range(grid_width)] for _ in range(grid_height)]

# Adicionando bloco
block = pygame.Rect(grid_width // 2 * cell_size, 0, cell_size, cell_size)
block_falling = True
block_speed = 100

# Função para atualizar a grade
def update_grid(grid):
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

    return new_grid

# Função para desenhar a grade na tela
def draw_grid(grid, screen):
    for y in range(grid_height):
        for x in range(grid_width):
            water_amount = grid[y][x]
            color = (0, 0, min(255, 100 + water_amount * 3))
            pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))

def check_block_collision(grid, block):
    block_cell_x, block_cell_y = block.x // cell_size, block.y // cell_size
    if block_cell_y < grid_height - 1 and grid[block_cell_y + 1][block_cell_x] > 0:
        return True
    return False

# Loop principal do jogo
running = True
while running:
    # Processando eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualizando a posição do bloco
    if block_falling:
        if check_block_collision(grid, block):
            block_falling = False
            grid[block.y // cell_size][block.x // cell_size] -= 10  # Propagação da energia na superfície da água
        else:
            block.y += block_speed

    # Atualizando a grade
    grid = update_grid(grid)

    # Desenhando a grade e o bloco na tela
    screen.fill((255, 255, 255))
    draw_grid(grid, screen)
    pygame.draw.rect(screen, (255, 0, 0), block)
    pygame.display.flip()

    # Limitando a taxa de quadros
    clock.tick(30)

pygame.quit()
