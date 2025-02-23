import pygame
import sys

def pacmancode():
    # Inicialización de Pygame
    pygame.init()

    # Dimensiones de la ventana
    WIDTH, HEIGHT = 800, 600
    CELL_SIZE = 20
    STATUS_BAR_HEIGHT = 40  # Altura de la barra de estado inferior

    # Colores
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)

    # Configuración de la ventana
    screen = pygame.display.set_mode((WIDTH, HEIGHT + STATUS_BAR_HEIGHT))  # Altura extendida para la barra de estado
    pygame.display.set_caption("Pac-Man")
    clock = pygame.time.Clock()

    # Fuentes para texto
    font = pygame.font.SysFont(None, 30)

    # Laberinto representado como una matriz
    maze = [
        "1111111111111111111111111111111111111111",
        "1000000000000111111100000000000000000001",
        "1011110111110111111101111101111101111101",
        "1011110111110111111101111101111101111101",
        "1000000000000000000000000000000000000001",
        "1111101111011110111011110111110111011111",
        "1111101111011110111011110111110111011111",
        "1000000000001110111000000000000111000001",
        "1011110111111110111011110111111111011101",
        "1011110111111110111011110111111111011101",
        "1000000000000000000000000000000000000001",
        "1111101111011110111111110111110111011111",
        "1111101111011110111111110111110111011111",
        "1000000000010000000000000000000000000001",
        "1011111111010111111111011111011111111101",
        "1011111111010111111111011111011111111101",
        "1000000000000000000000000000000000000001",
        "1111101111110111111101111101111110111111",
        "1111101111110111111101111101111110111111",
        "1000000000000000000000000000000000000001",
        "1011111111011111110111111110111111111101",
        "1011111111011111110111111110111111111101",
        "1000000000000000000000000000000000000001",
        "1111111111111111111111111111111111111111",
    ]

    ROWS = len(maze)
    COLS = len(maze[0])

    # Posición inicial de Pac-Man (en píxeles)
    pacman_x, pacman_y = CELL_SIZE + CELL_SIZE // 2, CELL_SIZE + CELL_SIZE // 2
    pacman_dx, pacman_dy = 0, 0

    # Tamaño de Pac-Man (más grande)
    pacman_size = CELL_SIZE // 2 - 2

    # Temporizador para controlar el movimiento
    move_delay = 100  # Milisegundos entre movimientos
    last_move_time = pygame.time.get_ticks()  # Tiempo del último movimiento

    # Dibujar el laberinto usando líneas
    def draw_maze():
        for row in range(ROWS):
            for col in range(COLS):
                if maze[row][col] == "1":  # Si es un muro
                    x = col * CELL_SIZE
                    y = row * CELL_SIZE
                    # Dibujar líneas para los bordes del muro
                    if row > 0 and maze[row - 1][col] == "0":  # Borde superior
                        pygame.draw.line(screen, WHITE, (x, y), (x + CELL_SIZE, y), 2)
                    if col > 0 and maze[row][col - 1] == "0":  # Borde izquierdo
                        pygame.draw.line(screen, WHITE, (x, y), (x, y + CELL_SIZE), 2)
                    if row < ROWS - 1 and maze[row + 1][col] == "0":  # Borde inferior
                        pygame.draw.line(screen, WHITE, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)
                    if col < COLS - 1 and maze[row][col + 1] == "0":  # Borde derecho
                        pygame.draw.line(screen, WHITE, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)

    # Dibujar a Pac-Man
    def draw_pacman(x, y):
        pygame.draw.circle(screen, YELLOW, (int(x), int(y)), pacman_size)

    # Dibujar la barra de estado (Score y Nickname)
    def draw_status_bar():
        pygame.draw.rect(screen, BLACK, (0, HEIGHT, WIDTH, STATUS_BAR_HEIGHT))  # Fondo negro para la barra
        score_text = font.render("Score", True, WHITE)
        nickname_text = font.render("Nickname", True, WHITE)
        screen.blit(score_text, (10, HEIGHT + 10))  # "Score" a la izquierda
        screen.blit(nickname_text, (WIDTH - 120, HEIGHT + 10))  # "Nickname" a la derecha

    # Comprobar si Pac-Man puede moverse a una posición (en píxeles)
    def can_move(x, y, dx, dy):
        next_x = x + dx
        next_y = y + dy
        col = int(next_x // CELL_SIZE)
        row = int(next_y // CELL_SIZE)

        # Verificar colisión con muros
        if col < 0 or col >= COLS or row < 0 or row >= ROWS:
            return False
        if maze[row][col] == "1":
            return False

        # Permitir moverse dentro de una celda si no hay muro
        return True

    # Loop principal del juego
    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pacman_dx, pacman_dy = 0, -CELL_SIZE
                elif event.key == pygame.K_DOWN:
                    pacman_dx, pacman_dy = 0, CELL_SIZE
                elif event.key == pygame.K_LEFT:
                    pacman_dx, pacman_dy = -CELL_SIZE, 0
                elif event.key == pygame.K_RIGHT:
                    pacman_dx, pacman_dy = CELL_SIZE, 0

        # Controlar la velocidad del movimiento usando un temporizador
        current_time = pygame.time.get_ticks()
        if current_time - last_move_time > move_delay:
            # Calcular nueva posición de Pac-Man
            if can_move(pacman_x, pacman_y, pacman_dx, 0):
                pacman_x += pacman_dx
            if can_move(pacman_x, pacman_y, 0, pacman_dy):
                pacman_y += pacman_dy

            # Teletransportar si Pac-Man cruza los bordes
            if pacman_x < 0:
                pacman_x = WIDTH
            elif pacman_x > WIDTH:
                pacman_x = 0
            if pacman_y < 0:
                pacman_y = HEIGHT
            elif pacman_y > HEIGHT:
                pacman_y = 0

            last_move_time = current_time  # Actualizar el tiempo del último movimiento

        # Dibujar el laberinto, Pac-Man y barra de estado
        draw_maze()
        draw_pacman(pacman_x, pacman_y)
        draw_status_bar()

        pygame.display.flip()
        clock.tick(60)  # FPS (fluidez del juego)

    pygame.quit()
    sys.exit()
