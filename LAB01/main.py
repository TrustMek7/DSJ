import pygame
import math
import random
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background_original = pygame.image.load('background.jpg')
background = pygame.transform.scale(background_original, (800, 600))

# Background Sound
mixer.music.load('background.mp3')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerImg = pygame.transform.scale(playerImg, (100, 100))
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# SISTEMA DE VELOCIDAD PROGRESIVA
base_enemy_speed = 0.5  # Velocidad inicial (lenta)
speed_increase_per_point = 0.2  # Cuánto aumenta por cada punto
max_enemy_speed = 4.0  # Velocidad máxima
current_enemy_speed = base_enemy_speed

for i in range(num_of_enemies):
    img = pygame.image.load('enemy.png').convert_alpha()
    img = pygame.transform.scale(img, (200, 120))
    enemyImg.append(img)
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(current_enemy_speed)  # Usar velocidad inicial
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load("bullet.png").convert_alpha()
bulletImg = pygame.transform.scale(bulletImg, (20, 60))
bulletX = 50
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
previous_score = 0  # Para detectar cuando cambia el puntaje
font = pygame.font.Font('freesansbold.ttf', 32)
speed_font = pygame.font.Font('freesansbold.ttf', 20)  # Para mostrar velocidad
textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def update_enemy_speed():
    """
    Actualiza la velocidad de todos los enemigos basándose en el puntaje
    """
    global current_enemy_speed

    # Calcular nueva velocidad
    current_enemy_speed = base_enemy_speed + (score_value * speed_increase_per_point)

    # Aplicar velocidad máxima
    if current_enemy_speed > max_enemy_speed:
        current_enemy_speed = max_enemy_speed

    # Actualizar velocidad de todos los enemigos
    for i in range(len(enemyX_change)):
        # Mantener la dirección (positiva o negativa) pero cambiar la magnitud
        direction = 1 if enemyX_change[i] > 0 else -1
        enemyX_change[i] = current_enemy_speed * direction


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))

    # Mostrar velocidad actual
    speed_text = speed_font.render(f"Speed: {current_enemy_speed:.1f}", True, (255, 255, 0))
    screen.blit(speed_text, (x, y + 35))


def show_difficulty_level():
    """
    Muestra el nivel de dificultad basado en la velocidad
    """
    if current_enemy_speed <= 1.0:
        level = "EASY"
        color = (0, 255, 0)  # Verde
    elif current_enemy_speed <= 2.0:
        level = "MEDIUM"
        color = (255, 255, 0)  # Amarillo
    elif current_enemy_speed <= 3.0:
        level = "HARD"
        color = (255, 165, 0)  # Naranja
    else:
        level = "EXTREME"
        color = (255, 0, 0)  # Rojo

    level_text = speed_font.render(f"Difficulty: {level}", True, color)
    screen.blit(level_text, (10, 70))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 255, 0))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 45, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)  # Controlar FPS para movimiento suave

    # RGB
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5  # Aumenté un poco la velocidad del jugador
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('laser.mp3')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking for boundaries of spaceship
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 700:  # Ajustado para el nuevo tamaño del jugador
        playerX = 700

    # Enemy movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = current_enemy_speed  # Usar velocidad actual
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 600:  # Ajustado para el nuevo tamaño del enemigo
            enemyX_change[i] = -current_enemy_speed  # Usar velocidad actual
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.mp3')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1

            # ACTUALIZAR VELOCIDAD CUANDO AUMENTA EL PUNTAJE
            if score_value != previous_score:
                update_enemy_speed()
                previous_score = score_value
                print(f"Score: {score_value}, New Speed: {current_enemy_speed:.1f}")  # Debug

            enemyX[i] = random.randint(0, 600)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    show_difficulty_level()
    pygame.display.update()

pygame.quit()