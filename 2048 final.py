import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 400
GRID_SIZE = 4
TILE_SIZE = WIDTH // GRID_SIZE
SCORE_HEIGHT = 50
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)

screen = pygame.display.set_mode((WIDTH, HEIGHT + SCORE_HEIGHT))
pygame.display.set_caption("2048")

font = pygame.font.Font(None, 36)
score_font = pygame.font.Font(None, 48)

TILE_COLORS = {
    2: (252, 245, 238),
    4: (255, 196, 196),
    8: (238, 105, 131),
    16: (133, 14, 53),
    32: (84, 8, 99),
    64: (146, 72, 122),
    128: (228, 155, 166),
    256: (255, 211, 213),
    512: (71, 52, 114),
    1024: (83, 98, 158),
    2048: (135, 186, 195),
    4096: (214, 244, 237)
}

BACKGROUND_COLOR = (169, 169, 169)

grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
score = 0


def draw_tile(x, y, value):
    if value in TILE_COLORS:
        color = TILE_COLORS[value]
    else:
        color = (0, 0, 0)

    pygame.draw.rect(
        screen, color, (x, y, TILE_SIZE, TILE_SIZE))
    text_surface = font.render(
        str(value), True, BLACK)
    text_rect = text_surface.get_rect(
        center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
    screen.blit(text_surface, text_rect)


def generate_new_tile():
    empty_cells = [
        (x, y) for x in range(GRID_SIZE)
        for y in range(GRID_SIZE) if grid[x][y] == 0]
    if empty_cells:
        x, y = random.choice(empty_cells)
        grid[x][y] = 2 if random.random() < 0.9 else 4


def update_screen():
    screen.fill(BACKGROUND_COLOR)

    score_label = score_font.render(
        f'Score: {score}', True, BLACK)
    score_label_rect = score_label.get_rect(
        center=(WIDTH // 2, SCORE_HEIGHT // 2))
    screen.blit(score_label, score_label_rect)

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            draw_tile(x * TILE_SIZE, y * TILE_SIZE, grid[x][y])

    pygame.display.flip()


def game_over():
    game_over_text = font.render('GAME OVER', True, WHITE, BLACK)
    screen.blit(
        game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 25))
    pygame.display.flip()
    pygame.time.delay(2000)


generate_new_tile()
generate_new_tile()
update_screen()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            previous_grid = [row[:] for row in grid]

            if event.key == pygame.K_UP:
                for row in grid:
                    row1 = [
                        val for val in row if val != 0]
                    for i in range(len(row1) - 1):
                        if row1[i] == row1[i + 1]:
                            row1[i] *= 2
                            row1[i + 1] = 0
                            score += row1[i]
                    row1 = [val for val in row1 if val != 0]
                    row1 += [0] * (GRID_SIZE - len(row1))
                    row[:] = row1

            elif event.key == pygame.K_DOWN:
                for row in grid:
                    row1 = [
                        val for val in row if val != 0]
                    for i in range(len(row1) - 1, 0, -1):
                        if row1[i] == row1[i - 1]:
                            row1[i] *= 2
                            row1[i - 1] = 0
                            score += row1[i]
                    row1 = [val for val in row1 if val != 0]
                    row1 += [0] * (GRID_SIZE - len(row1)) + row1
                    row[:] = row1

            elif event.key == pygame.K_LEFT:
                for col in range(GRID_SIZE):
                    column = [grid[row][col] for row in range(GRID_SIZE)]
                    column1 = [val for val in column if val != 0]
                    for i in range(len(column1) - 1):
                        if column1[i] == column1[i + 1]:
                            column1[i] *= 2
                            column1[i + 1] = 0
                            score += column1[i]
                    column1 = [val for val in column1 if val != 0]
                    column1 += [0] * (GRID_SIZE - len(column1))
                    for row in range(GRID_SIZE):
                        grid[row][col] = column1[row]

            elif event.key == pygame.K_RIGHT:
                for col in range(GRID_SIZE):
                    column = [grid[col][row] for row in range(GRID_SIZE)]
                    column1 = [val for val in column if val != 0]
                    for i in range(len(column1) - 1, 0, -1):
                        if column1[i] == column1[i - 1]:
                            column1[i] *= 2
                            column1[i - 1] = 0
                            score += column1[i]
                    column1 = [val for val in column1 if val != 0]
                    column1 += [0] * (GRID_SIZE - len(column1)) + column1
                    for row in range(GRID_SIZE):
                        grid[row][col] = column1[row]

            if grid != previous_grid:
                generate_new_tile()
                update_screen()

                if any(any(cell == 2048 for cell in row)
                       for row in grid):
                    game_over()
                    running = False

                game_over_possible = False
                for x in range(GRID_SIZE):
                    for y in range(GRID_SIZE):
                        if grid[x][y] == 0:
                            game_over_possible = True
                        if x > 0 and (
                                grid[x][y] == grid[x - 1][y]):
                            game_over_possible = True
                        if x < GRID_SIZE - 1 and (
                                grid[x][y] == grid[x + 1][y]):
                            game_over_possible = True
                        if y > 0 and (
                                grid[x][y] == grid[x][y - 1]):
                            game_over_possible = True
                        if y < GRID_SIZE - 1 and (
                                grid[x][y] == grid[x][y + 1]):
                            game_over_possible = True

                if not game_over_possible:
                    game_over()
                    running = False

    for row in grid:
        if 2048 in row:
            running = False

    update_screen()

pygame.quit()

