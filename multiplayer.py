import pygame
from pygame.locals import *
import time
from assets.scripts.network import Network

pygame.init()

def parse_data(data):
    players = data[0]
    cars = data[1]
    main_player = data[2]
    return players, cars, main_player

def run(screen, server):
    n = Network(server)

    try:
        player = n.get_p()
    except Exception:
        return

    keymap = {"up": False, "left": False, "right": False, "car": False, "ride": False}

    players = []

    ground = pygame.Rect(-5000, 400, 10000, 200)

    true_scroll = [0, 0]
    scroll = [0, 0]

    clock = pygame.time.Clock()
    pt = time.time()
    dt = 1

    quitted = False

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quitted = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    keymap["car"] = True
                if event.key == pygame.K_q:
                    keymap["ride"] = True
        print(keymap["car"])

        key_pressed = pygame.key.get_pressed()
        keymap["left"] = key_pressed[pygame.K_LEFT]
        keymap["right"] = key_pressed[pygame.K_RIGHT]
        keymap["up"] = key_pressed[pygame.K_UP]


        data = n.send({"keymap": keymap, "dt": dt})
        players, cars, player = parse_data(data)
        print([c.rect for c in cars])
        keymap["car"] = False
        keymap["ride"] = False

        true_scroll[0] += (player.rect.centerx - scroll[0] - 640) / 30 * dt
        true_scroll[1] += (player.rect.centery - scroll[1] - 360) / 30 * dt
        scroll = [int(true_scroll[0]), int(true_scroll[1])]

        screen.fill((105, 235, 255))
        pygame.draw.rect(screen, (148, 75, 16), (ground.x - scroll[0], ground.y - scroll[1], ground.width, ground.height))
        for p in players:
            p.draw(screen, scroll)
        for car in cars:
            car.draw(screen, scroll)
        pygame.display.update()

        clock.tick()
        now = time.time()
        dt = (now - pt) * 60
        dt = min(dt, 4)
        pt = now

    return quitted
