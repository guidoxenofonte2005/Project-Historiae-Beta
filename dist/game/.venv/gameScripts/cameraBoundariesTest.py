import pygame

# Configurações iniciais
WIDTH, HEIGHT = 800, 600  # Tamanho da tela
MAP_WIDTH, MAP_HEIGHT = 2000, 2000  # Tamanho do mapa (área total do jogo)
PLAYER_SPEED = 5  # Velocidade do jogador

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Inicialize o jogador e a câmera
player = pygame.Rect(100, 100, 50, 50)  # Posição e tamanho do jogador
camera = pygame.Rect(0, 0, WIDTH, HEIGHT)  # Inicializa a câmera no canto superior esquerdo

# Função para atualizar a posição da câmera com limites
def update_camera():
    # A câmera deve se centrar no jogador
    camera.x = player.x + player.width // 2 - WIDTH // 2
    camera.y = player.y + player.height // 2 - HEIGHT // 2

    # Limite a câmera dentro da área do mapa
    camera.x = max(0, min(camera.x, MAP_WIDTH - WIDTH))
    camera.y = max(0, min(camera.y, MAP_HEIGHT - HEIGHT))

# Função principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimento do jogador com teclas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player.x += PLAYER_SPEED
    if keys[pygame.K_UP]:
        player.y -= PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        player.y += PLAYER_SPEED

    # Atualize a posição da câmera
    update_camera()

    # Desenhar fundo do mapa
    screen.fill((0, 0, 0))

    # Desenhar jogador com a posição relativa à câmera
    pygame.draw.rect(screen, (255, 0, 0), 
                     (player.x - camera.x, player.y - camera.y, player.width, player.height))

    # Atualize a tela e o relógio
    pygame.display.flip()
    clock.tick(60)

pygame.quit()