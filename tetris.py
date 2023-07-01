import pygame
import random

# Dimensiones de la pantalla
WIDTH = 400
HEIGHT = 400
FPS = 30

# Tamaño de la cuadrícula del juego
GRID_SIZE = 25
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Definición de las piezas del Tetris
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

class TetrisGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.running = True
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.current_piece = self.get_random_piece()
        self.current_piece_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.current_piece_y = 0
        self.fall_time = 0.5  # Intervalo de tiempo inicial entre caídas de las piezas
        self.last_fall_time = pygame.time.get_ticks()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move_piece(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.move_piece(1, 0)
                elif event.key == pygame.K_DOWN:
                    self.move_piece(0, 1)
                elif event.key == pygame.K_SPACE:
                    self.rotate_piece()

    def update(self):
        # Verificar si es el momento de hacer caer la pieza automáticamente
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fall_time >= self.fall_time * 1000:
            self.move_piece(0, 1)
            self.last_fall_time = current_time

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.draw_piece()
        self.draw_score()
        pygame.display.flip()

    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(self.screen, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
                if self.grid[y][x] == 1:
                    pygame.draw.rect(self.screen, GREEN, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def draw_piece(self):
        for y in range(len(self.current_piece)):
            for x in range(len(self.current_piece[y])):
                if self.current_piece[y][x] == 1:
                    pygame.draw.rect(self.screen, RED, ((self.current_piece_x + x) * GRID_SIZE, (self.current_piece_y + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def draw_score(self):
        font = pygame.font.SysFont(None, 36)
        score_text = font.render("Score: " + str(self.score), True, BLUE)
        self.screen.blit(score_text, (10, 10))

    def get_random_piece(self):
        shape = random.choice(SHAPES)
        return shape

    def move_piece(self, dx, dy):
        if self.check_collision(self.current_piece, self.current_piece_x + dx, self.current_piece_y + dy):
            if dy == 1:  # Si el movimiento es hacia abajo y hay colisión, fijar la pieza en la cuadrícula y crear una nueva
                self.fix_piece()
                self.clear_lines()
                self.current_piece = self.get_random_piece()
                self.current_piece_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
                self.current_piece_y = 0
                if self.check_collision(self.current_piece, self.current_piece_x, self.current_piece_y):
                    self.running = False  # Fin del juego si hay colisión al crear una nueva pieza
            return

        self.current_piece_x += dx
        self.current_piece_y += dy

    def rotate_piece(self):
        rotated_piece = list(zip(*reversed(self.current_piece)))
        if not self.check_collision(rotated_piece, self.current_piece_x, self.current_piece_y):
            self.current_piece = rotated_piece

    def check_collision(self, piece, x, y):
        for row in range(len(piece)):
            for col in range(len(piece[row])):
                if (
                    piece[row][col] == 1
                    and (
                        x + col < 0
                        or x + col >= GRID_WIDTH
                        or y + row >= GRID_HEIGHT
                        or self.grid[y + row][x + col] == 1
                    )
                ):
                    return True
        return False

    def fix_piece(self):
        for row in range(len(self.current_piece)):
            for col in range(len(self.current_piece[row])):
                if self.current_piece[row][col] == 1:
                    self.grid[self.current_piece_y + row][self.current_piece_x + col] = 1

    def clear_lines(self):
        lines_cleared = 0
        for row in range(GRID_HEIGHT):
            if all(cell == 1 for cell in self.grid[row]):
                del self.grid[row]
                self.grid.insert(0, [0] * GRID_WIDTH)
                lines_cleared += 1
        self.score += lines_cleared

game = TetrisGame()
game.run()

