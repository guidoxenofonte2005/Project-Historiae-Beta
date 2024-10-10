import pygame

pygame.init()
font = pygame.font.SysFont('Monocraft', 24)
screen = pygame.display.set_mode((800, 500))
timer = pygame.time.Clock()
message = "Uma mensagem muito grande e legal que só serve de teste e nada além disso"
snip = font.render('', True, 'white')
counter = 0
speed = 3
done = False

run = True
while run:
    screen.fill('dark gray')
    pygame.draw.rect(screen, 'black', [0, 300, 800, 200])
    
    if counter < speed * len(message):
        counter += 1
    elif counter >= speed * len(message):
        done = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    snip = font.render(message[0:counter//speed], True, 'white')
    screen.blit(snip, (10, 310))
    
    timer.tick(60)
    pygame.display.update()

pygame.quit()