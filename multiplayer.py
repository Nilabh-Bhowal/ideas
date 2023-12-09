import pygame
from pygame.locals import *
import time
from assets.scripts.car import Car
from assets.scripts.player import Player
from assets.scripts.building import Building
from assets.scripts.road import Road
from assets.scripts.network import Network
from assets.scripts.object import Object
import assets.scripts.ui as ui

pygame.init()
def run(screen, server):
    n = Network(server)
    player = Player()

    player_img = pygame.transform.scale_by(pygame.image.load("assets/images/player.png").convert(), 16)

    ground = Object(-5000, 0, 0, 10000, 200, 1000)
    building = Building(200, 200, "data")

    road = Road()


    true_scroll = [0, 0, 0]
    scroll = [0, 0, 0]
    player = Player()
    clock = pygame.time.Clock()
    pt = time.time()
    dt = 1

    quitted = False
    if not n.p:
        return quitted

    running = True
    while running:
        if not n.p:
            return quitted
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quitted = True

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[K_r]:
            player.obj.x = 0
            player.obj.y = 0
            player.obj.z = 0
        player.movement[0] = (keys_pressed[K_RIGHT] - keys_pressed[K_LEFT]) * 5
        if keys_pressed[K_SPACE]:
            if jumped == False and player.air_timer < 10:
                jumped = True
                player.movement[1] = -15
        else:
            jumped = False

        player.movement[2] = (keys_pressed[K_UP] - keys_pressed[K_DOWN]) * 5

        player.update(dt, [ground] + building.objs)

        data = n.send({"x": int(player.obj.x), "y": int(player.obj.y), "z": int(player.obj.z)})

        player.obj.define_values()
        true_scroll[0] += ((player.obj.centerx) - true_scroll[0]) / 15 * dt
        true_scroll[1] += ((player.obj.centery - 250) - true_scroll[1]) / 15 * dt
        # true_scroll[2] += ((player.obj.centerz) - true_scroll[2]) / 15 * dt
        scroll = [int(true_scroll[0]), int(true_scroll[1]), int(true_scroll[2])]

        screen.fill((105, 235, 255))
        blit_list = []
        road.draw(blit_list, scroll)
        building.draw(blit_list, scroll, player=player)

        for p in data:
            draw_x = p["x"] - scroll[0]
            draw_y = p["y"] - scroll[1]
            draw_z = p["z"] - scroll[2]

            if p["z"] != -1000:
                scale = 1000 / (1000 + draw_z)
                draw_x = draw_x * scale
                draw_y = draw_y * scale

            draw_x += 640
            draw_y += 360

            blit_list.append({"surf": pygame.transform.scale_by(player_img, scale), "pos": (draw_x, draw_y), "z": p["z"], "a": 255})

        for item in sorted(blit_list, key=lambda surf: surf["z"], reverse=True):
            if item["surf"]:
                if item["a"] != 255:
                    item["surf"].set_alpha(item["a"])
                screen.blit(item["surf"], (item["pos"]))
        ui.heading(f"f: {int(clock.get_fps())}", 640, 50, screen)
        pygame.display.update()


        clock.tick()
        now = time.time()
        dt = (now - pt) * 60
        dt = min(dt, 4)
        pt = now

    return quitted
