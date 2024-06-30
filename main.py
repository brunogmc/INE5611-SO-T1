import pygame
import random
import math

# Inicialização do Pygame
pygame.init()

# Configurações da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Bateria Antiaérea')

# Cores
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Configurações da bateria antiaérea
battery_x = screen_width // 2
battery_y = screen_height - 50
battery_width = 10
battery_height = 50
battery_angle = 90

# Configurações dos tiros
bullets = []
bullet_speed = 7

# Configurações das naves alienígenas (aumentadas)
alien_width = 60  # Aumentado de 40 para 60
alien_height = 30  # Aumentado de 20 para 30
aliens = []

# Função para desenhar a bateria
def draw_battery(x, y, angle):
    if angle == 90:  # Vertical
        pygame.draw.rect(screen, red, (x - battery_width // 2, y - battery_height, battery_width, battery_height))
    elif angle == 45:  # Diagonal para a esquerda
        pygame.draw.line(screen, red, (x, y), (x - 35, y - 35), battery_width)
    elif angle == 135:  # Diagonal para a direita
        pygame.draw.line(screen, red, (x, y), (x + 35, y - 35), battery_width)
    elif angle == 180:  # Horizontal para a esquerda
        pygame.draw.rect(screen, red, (x - battery_height, y - battery_width // 2, battery_height, battery_width))
    elif angle == 0:  # Horizontal para a direita
        pygame.draw.rect(screen, red, (x, y - battery_width // 2, battery_height, battery_width))

# Função para desenhar as naves alienígenas
def draw_aliens(aliens):
    for alien in aliens:
        pygame.draw.rect(screen, green, (alien[0], alien[1], alien_width, alien_height))

# Função para desenhar os tiros
def draw_bullets(bullets):
    for bullet in bullets:
        pygame.draw.circle(screen, white, (int(bullet[0]), int(bullet[1])), 5)

# Função para mover os tiros
def move_bullets(bullets):
    for bullet in bullets:
        bullet[0] += bullet[2]
        bullet[1] += bullet[3]

# Função para detectar colisões
def check_collision(bullets, aliens):
    for bullet in bullets:
        bullet_rect = pygame.Rect(bullet[0] - 5, bullet[1] - 5, 10, 10)  # Cria um retângulo ao redor da bala
        for alien in aliens:
            alien_rect = pygame.Rect(alien[0], alien[1], alien_width, alien_height)
            if bullet_rect.colliderect(alien_rect):  # Verifica a colisão
                bullets.remove(bullet)
                aliens.remove(alien)
                break

# Loop do jogo
running = True
while running:
    screen.fill(black)  # Limpar a tela
    
    # Eventos do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                battery_angle = 90
            elif event.key == pygame.K_a:
                battery_angle = 180
            elif event.key == pygame.K_d:
                battery_angle = 0
            elif event.key == pygame.K_q:
                battery_angle = 45
            elif event.key == pygame.K_e:
                battery_angle = 135
            elif event.key == pygame.K_SPACE:
                # Adicionar um tiro na direção atual
                angle_rad = math.radians(battery_angle)
                if battery_angle == 45:
                    bullet_dx = -bullet_speed * math.cos(math.radians(45))
                    bullet_dy = -bullet_speed * math.sin(math.radians(45))
                elif battery_angle == 135:
                    bullet_dx = bullet_speed * math.cos(math.radians(45))
                    bullet_dy = -bullet_speed * math.sin(math.radians(45))
                else:
                    bullet_dx = bullet_speed * math.cos(angle_rad)
                    bullet_dy = -bullet_speed * math.sin(angle_rad)
                bullets.append([battery_x, battery_y, bullet_dx, bullet_dy])
    
    # Adicionar novas naves alienígenas
    if random.randint(1, 50) == 1:
        alien_x = random.randint(0, screen_width - alien_width)
        aliens.append([alien_x, 0])
    
    # Atualizar posição das naves alienígenas
    for alien in aliens:
        alien[1] += 2
    
    # Remover naves que saíram da tela
    aliens = [alien for alien in aliens if alien[1] < screen_height]

    # Mover os tiros
    move_bullets(bullets)

    # Verificar colisões entre tiros e naves
    check_collision(bullets, aliens)

    # Desenhar a bateria, naves alienígenas e tiros
    draw_battery(battery_x, battery_y, battery_angle)
    draw_aliens(aliens)
    draw_bullets(bullets)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
