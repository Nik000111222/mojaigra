import pygame
import random

# Nastavitve okna
WIDTH = 800
HEIGHT = 600
FPS = 60

# Barve
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Inicializacija Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

# Ustvarjanje igralcev in žoge
player = pygame.Rect(10, HEIGHT // 2 - 50, 10, 100)
opponent = pygame.Rect(WIDTH - 20, HEIGHT // 2 - 50, 10, 100)
ball = pygame.Rect(WIDTH // 2 - 5, HEIGHT // 2 - 5, 10, 10)
ball_speed_x = 7 * random.choice((-1, 1))
ball_speed_y = 7 * random.choice((-1, 1))

# Glavna zanka igre
running = True
while running:
    # Ohranjanje zanke na pravilni hitrosti
    clock.tick(FPS)

    # Preverjanje vseh dogodkov
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Premikanje igralca
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.y -= 5
    if keys[pygame.K_s]:
        player.y += 5
    player.y = min(max(player.y, 0), HEIGHT - player.height)

    # Premikanje nasprotnika
    ball_y = ball.y
    if opponent.y < ball_y:
        opponent.y += 5
    elif opponent.y > ball_y:
        opponent.y -= 5
    opponent.y = min(max(opponent.y, 0), HEIGHT - opponent.height)

    # Premikanje žoge
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Odboj od robov zaslona
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= WIDTH:
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed_x *= random.choice((-1, 1))
        ball_speed_y *= random.choice((-1, 1))

    # Odboj od igralcev
    if player.colliderect(ball) or opponent.colliderect(ball):
        ball_speed_x *= -1

    # Prikaz ozadja
    screen.fill(BLACK)

    # Risnaje vseh elementov
    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, WHITE, opponent)
    pygame.draw.ellipse(screen, WHITE, ball)

    # Posodabljanje prikaza
    pygame.display.flip()

pygame.quit()