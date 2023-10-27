import pygame
from pygame.locals import *
import time
from assets.scripts.player import Player
from assets.scripts.car import Car

pygame.init()

def run(screen):

    ground = pygame.Rect(-100, 400, 1000, 200)

    keymap = {"up": False, "left": False, "right": False, "car": False, "ride": False}

    player = Player()
    cars = []

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

        key_pressed = pygame.key.get_pressed()
        keymap["left"] = key_pressed[pygame.K_LEFT]
        keymap["right"] = key_pressed[pygame.K_RIGHT]
        keymap["up"] = key_pressed[pygame.K_UP]

        if player.in_vehicle:
            for car in cars:
                if car.driver == player:
                    car.acceleration = (keymap["right"] - keymap["left"])
        else:
            player.movement[0] = (keymap["right"] - keymap["left"]) * 5
        if keymap["up"]:
            if jumped == False and player.air_timer < 10:
                jumped = True
                player.movement[1] = keymap["up"] * -15
        else:
            jumped = False
        if keymap["car"]:
            cars.append(Car(player.rect.x, player.rect.y))
        if keymap["ride"]:
            for car in cars:
                if player.rect.colliderect(car.rect):
                    car.driver = player if car.driver is None else None
                    player.in_vehicle = not player.in_vehicle

        player.update(dt, [ground])
        for car in cars:
            car.update(dt, [ground])

        keymap["car"] = False
        keymap["ride"] = False

        true_scroll[0] += (player.rect.centerx - scroll[0] - 640) / 30 * dt
        true_scroll[1] += (player.rect.centery - scroll[1] - 360) / 30 * dt
        scroll = [int(true_scroll[0]), int(true_scroll[1])]

        screen.fill((105, 235, 255))
        pygame.draw.rect(screen, (148, 75, 16), (ground.x - scroll[0], ground.y - scroll[1], ground.width, ground.height))
        for car in cars:
            car.draw(screen, scroll)
        player.draw(screen, scroll)
        pygame.display.update()

        clock.tick()
        now = time.time()
        dt = (now - pt) * 60
        dt = min(dt, 4)
        pt = now

    return quitted
