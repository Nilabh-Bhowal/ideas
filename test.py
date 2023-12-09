import pygame
from pygame.locals import *
from assets.scripts.object import Object
from assets.scripts.player import Player

pygame.init()

screen = pygame.display.set_mode((800, 600))

player = Player()
ground = Object(-50, -50, -50, 100, 100, 100)

true_scroll = [0, 0]
scroll = [0, 0]

f = 300

img = pygame.image.load("assets/images/0.png")

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_EQUALS:
                f += 50
            elif event.key == K_MINUS:
                f -= 50

    key_pressed = pygame.key.get_pressed()

    player.movement[0] = (key_pressed[K_RIGHT] - key_pressed[K_LEFT]) * 5
    player.movement[1] = (key_pressed[K_s] - key_pressed[K_w]) * 5
    if key_pressed[K_SPACE]:
        if jumped == False:
            jumped = True
            player.movement[1] = -15
    else:
        jumped = False

    true_scroll[0] += ((player.obj.centerx * f / (f + player.obj.centerz)) - true_scroll[0]) / 5
    true_scroll[1] += ((player.obj.centery * f / (f + player.obj.centerz)) - true_scroll[1]) / 5
    scroll = [int(true_scroll[0]), int(true_scroll[1])]
    scroll = [int(true_scroll[0]), int(true_scroll[1])]

    player.movement[2] = (key_pressed[K_DOWN] - key_pressed[K_UP]) * 5

    player.update(1, [ground])
    screen.fill((255, 255, 255))

    ground.draw(screen, scroll, img)

    player.obj.draw(screen, scroll, img)


    pygame.display.update()
    clock.tick(60)

pygame.quit()
