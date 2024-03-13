import pygame
import sys
import random

pygame.init()

# Dimensiones
width = 900
height = 700
green = (0, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)

# Colores de selección de jugador
color_options = [(255, 0, 0), (255, 255, 0), (0, 0, 255)]  # Rojo, Amarillo, Azul
selected_color = 0  # Índice del color seleccionado

# Pantalla de selección de color
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Choose your color")


def draw_color_options(selected):
    screen.fill(black)
    for i, color in enumerate(color_options):
        pygame.draw.rect(screen, color, (width // 4, (height // 4) * (i + 1), 100, 100))
        if i == selected:
            pygame.draw.rect(screen, white, (width // 4 - 5, (height // 4) * (i + 1) - 5, 110, 110), 5)
    pygame.display.flip()


def select_color():
    global selected_color
    selected = False
    while not selected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_color = (selected_color - 1) % len(color_options)
                elif event.key == pygame.K_DOWN:
                    selected_color = (selected_color + 1) % len(color_options)
                elif event.key == pygame.K_RETURN:
                    selected = True
        draw_color_options(selected_color)


def draw_pause_menu():
    font = pygame.font.Font(None, 36)
    pause_text = font.render("Pause", True, white)
    screen.blit(pause_text, (width // 2 - pause_text.get_width() // 2, height // 2 - 50))

    resume_text = font.render("Push 'R' to continue", True, white)
    screen.blit(resume_text, (width // 2 - resume_text.get_width() // 2, height // 2))

    quit_text = font.render("push 'Q' to exit", True, white)
    screen.blit(quit_text, (width // 2 - quit_text.get_width() // 2, height // 2 + 50))

    pygame.display.flip()


def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        draw_pause_menu()


select_color()

# Inicialización de la pantalla de juego
screen = pygame.display.set_mode((width, height))

# Propiedades del jugador
diameter = 50
position = [width / 2, height - diameter * 2]

# Propiedades del enemigo
enemy_diameter = 50
enemy_position = [random.randint(0, width - enemy_diameter), 0]

# Estado del juego
finished = False
clock = pygame.time.Clock()



def crash(position, enemy_position):
    playerx = position[0]
    y = position[1]
    enemx = enemy_position[0]
    enemy = enemy_position[1]

    if enemx >= playerx and enemx < (playerx + diameter) or (playerx >= enemx and playerx < (enemx + enemy_diameter)):
        if enemy >= y and enemy < (y + diameter) or (
                y >= enemy and y < (enemy + enemy_diameter)):
            return True
    return False


# Loop principal del juego
while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause_game()

            x = position[0]
            if event.key == pygame.K_LEFT:
                x -= diameter
            if event.key == pygame.K_RIGHT:
                x += diameter
            position[0] = x

    screen.fill(black)

    if enemy_position[1] >= 0 and enemy_position[1] < height:
        enemy_position[1] += 20
    else:
        enemy_position[0] = random.randint(0, width - enemy_diameter)
        enemy_position[1] = 0

    if crash(position, enemy_position):
        finished = True

    pygame.draw.rect(screen, color_options[selected_color], (position[0], position[1],
                                                             diameter, diameter))
    pygame.draw.rect(screen, green, (enemy_position[0], enemy_position[1],
                                     enemy_diameter, enemy_diameter))

    clock.tick(20)
    pygame.display.update()

pygame.quit()
