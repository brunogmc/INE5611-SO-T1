import pygame
import random
import math
import threading

# Inicialização do Pygame
pygame.init()

# Configurações da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Jogo: Antiaérias contra os aliens')

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
max_bullets = 10  # Número máximo de balas carregadas
current_bullets = max_bullets  # Balas disponíveis inicialmente

# Configurações das naves alienígenas 
alien_width = 100
alien_height = 50  
aliens = []
alien_lock = threading.Lock()  # Lock para acesso thread-safe à lista de aliens
bullet_lock = threading.Lock()  # Lock para acesso thread-safe à lista de balas

# Parâmetros do jogo
total_aliens = 20  # Quantidade de naves alienígenas
aliens_spawned = 0
aliens_destroyed = 0
aliens_reached_ground = 0

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

# Função para desenhar os tiros
def draw_bullets(bullets):
    for bullet in bullets:
        pygame.draw.circle(screen, white, (int(bullet[0]), int(bullet[1])), 5)

# Função para mover os tiros
def move_bullets(bullets):
    for bullet in bullets:
        bullet[0] += bullet[2]
        bullet[1] += bullet[3]

# Classe para a nave alienígena
class Alien(threading.Thread):
    def __init__(self, x, y):
        threading.Thread.__init__(self)
        self.x = x
        self.y = y
        self.alive = True  # Controle de vida da nave

    def run(self):
        global aliens_reached_ground
        while self.alive and self.y < screen_height:
            self.y += 2  # Move a nave para baixo
            pygame.time.wait(50)  # Espera um pouco para suavizar o movimento

        if self.alive:
            aliens_reached_ground += 1  # Incrementa contador de naves que chegaram ao solo

        # Remover a nave da lista de aliens quando morrer
        with alien_lock:
            if self in aliens:
                aliens.remove(self)

    def draw(self):
        pygame.draw.rect(screen, green, (self.x, self.y, alien_width, alien_height))

    def die(self):
        global aliens_destroyed
        self.alive = False  # Marca a nave como morta
        aliens_destroyed += 1  # Incrementa contador de naves destruídas

# Função para detectar colisões
def check_collision(bullets, aliens):
    for bullet in bullets[:]:  # Usamos [:] para uma cópia da lista, pois estamos removendo itens
        bullet_rect = pygame.Rect(bullet[0] - 5, bullet[1] - 5, 10, 10)  # Cria um retângulo ao redor da bala
        for alien in aliens[:]:  # Usamos [:] para uma cópia da lista, pois estamos removendo itens
            alien_rect = pygame.Rect(alien.x, alien.y, alien_width, alien_height)
            if bullet_rect.colliderect(alien_rect):  # Verifica a colisão
                with bullet_lock:
                    if bullet in bullets:
                        bullets.remove(bullet)
                alien.die()  # Mata a nave (encerra a thread)
                break

# Função para verificar o estado do jogo
def check_game_state():
    if aliens_destroyed >= total_aliens // 2:
        return "win"
    elif aliens_reached_ground >= total_aliens // 2:
        return "lose"
    return "ongoing"

# Função para recarregar balas em uma thread secundária
def reload_bullets_thread():
    global current_bullets
    while current_bullets < max_bullets:
        pygame.time.wait(1000)  # Espera 1 segundo
        with bullet_lock:
            current_bullets = min(current_bullets + 1, max_bullets)

# Iniciar a thread de recarga de balas
reload_thread = None

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
                # Disparo, mas só se houver balas disponíveis
                if current_bullets > 0:
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
                    
                    with bullet_lock:
                        bullets.append([battery_x, battery_y, bullet_dx, bullet_dy])
                    current_bullets -= 1  # Reduzir contagem de balas
            elif event.key == pygame.K_s:
                # Iniciar a thread de recarga de balas se ainda não estiver rodando
                if reload_thread is None or not reload_thread.is_alive():
                    reload_thread = threading.Thread(target=reload_bullets_thread)
                    reload_thread.start()

    # Adicionar novas naves alienígenas
    if aliens_spawned < total_aliens and random.randint(1, 50) == 1:
        alien_x = random.randint(0, screen_width - alien_width)
        new_alien = Alien(alien_x, 0)
        with alien_lock:
            aliens.append(new_alien)
        new_alien.start()
        aliens_spawned += 1
    
    # Mover os tiros
    move_bullets(bullets)

    # Verificar colisões entre tiros e naves
    with alien_lock:
        check_collision(bullets, aliens)

    # Desenhar a bateria, naves alienígenas e tiros
    draw_battery(battery_x, battery_y, battery_angle)

    with alien_lock:
        for alien in aliens:
            alien.draw()

    draw_bullets(bullets)

    # Mostrar balas restantes na tela
    font = pygame.font.SysFont(None, 24)
    ammo_text = font.render(f'Balas: {current_bullets}/{max_bullets}', True, white)
    screen.blit(ammo_text, (10, 10))

    # Verificar estado do jogo
    game_state = check_game_state()
    if game_state != "ongoing":
        running = False
        result_text = "Vitória!" if game_state == "win" else "Derrota!"
        result_display = font.render(result_text, True, white)
        screen.blit(result_display, (screen_width // 2 - 50, screen_height // 2))
        pygame.display.flip()
        pygame.time.wait(3000)  # Espera 3 segundos antes de fechar

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
