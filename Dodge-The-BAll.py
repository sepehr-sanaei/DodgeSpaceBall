import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Set up display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Spaceship Dodger")

# Set up assets
player_size = 50
player_color = (0, 128, 255)
player_pos = [width // 2, height - 2 * player_size]

asteroid_size = 50
asteroid_color = (255, 0, 0)
asteroid_pos = [random.randint(0, width - asteroid_size), 0]
asteroid_list = [asteroid_pos]

background_color = (0, 0, 0)
score = 0
clock = pygame.time.Clock()

# Set up fonts
font = pygame.font.SysFont("monospace", 35)

def drop_asteroids(asteroid_list):
    delay = random.random()
    if len(asteroid_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, width - asteroid_size)
        y_pos = 0
        asteroid_list.append([x_pos, y_pos])

def draw_asteroids(asteroid_list):
    for asteroid_pos in asteroid_list:
        pygame.draw.rect(window, asteroid_color, (asteroid_pos[0], asteroid_pos[1], asteroid_size, asteroid_size))

def update_asteroid_positions(asteroid_list, score):
    for idx, asteroid_pos in enumerate(asteroid_list):
        if asteroid_pos[1] >= 0 and asteroid_pos[1] < height:
            asteroid_pos[1] += 10
        else:
            asteroid_list.pop(idx)
            score += 1
    return score

def collision_check(asteroid_list, player_pos):
    for asteroid_pos in asteroid_list:
        if detect_collision(asteroid_pos, player_pos):
            return True
    return False

def detect_collision(asteroid_pos, player_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    a_x = asteroid_pos[0]
    a_y = asteroid_pos[1]

    if (a_x >= p_x and a_x < (p_x + player_size)) or (p_x >= a_x and p_x < (a_x + asteroid_size)):
        if (a_y >= p_y and a_y < (p_y + player_size)) or (p_y >= a_y and p_y < (a_y + asteroid_size)):
            return True
    return False

# Game loop
game_over = False
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= 10
    if keys[pygame.K_RIGHT] and player_pos[0] < width - player_size:
        player_pos[0] += 10

    window.fill(background_color)

    drop_asteroids(asteroid_list)
    score = update_asteroid_positions(asteroid_list, score)
    text = font.render("Score: {}".format(score), True, (255, 255, 255))
    window.blit(text, [10, 10])

    if collision_check(asteroid_list, player_pos):
        game_over = True
        break

    draw_asteroids(asteroid_list)

    pygame.draw.rect(window, player_color, (player_pos[0], player_pos[1], player_size, player_size))

    clock.tick(30)

    pygame.display.update()

# Display game over message
while game_over:
    window.fill(background_color)
    text = font.render("Game Over! Score: {}".format(score), True, (255, 255, 255))
    window.blit(text, [width // 2 - 150, height // 2])
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
