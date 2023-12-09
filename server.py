import socket
from _thread import *
import pickle
import pygame
from pygame.locals import *
import time
from assets.scripts.player import Player
from assets.scripts.building import Building
from assets.scripts.road import Road

server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

pygame.init()


running = True

players = []
cars = []
player = 0

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

def threaded_client(conn, player):  # sourcery skip: do-not-use-bare-except
    conn.sendall(pickle.dumps({"x": players[player].obj.x, "y": players[player].obj.y}))
    while running:
        try:
            if data := pickle.loads(conn.recv(4096)):

                players[player].obj.x = data["x"]
                players[player].obj.y = data["y"]
                players[player].obj.z = data["z"]

                reply = [{"x": int(p.obj.x), "y": int(p.obj.y), "z": int(p.obj.z)} for p in players if p.online == True]
                print("Received: ", data)
                print("Sending : ", reply)

            else:
                print("Disconnected")
            conn.sendall(pickle.dumps(reply))
        except Exception as e:
            print(e)
            break

    print("Lost connection")
    players[player].online = False
    conn.close()

def game_loop():
    global running

    screen = pygame.display.set_mode((1280, 720))

    scroll = [0, -100, 0]

    road = Road()
    building = Building(200, 200, "data")
    player_img = pygame.transform.scale_by(pygame.image.load("assets/images/player.png").convert(), 16)
    blit_list = []

    clock = pygame.time.Clock()
    pt = time.time()
    dt = 1
    while running:
        try:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            key_pressed = pygame.key.get_pressed()
            scroll[0] += (key_pressed[K_RIGHT] - key_pressed[K_LEFT]) * 5 * dt
            scroll[1] += (key_pressed[K_DOWN] - key_pressed[K_UP]) * 5 * dt

            screen.fill((105, 235, 255))
            blit_list = []
            road.draw(blit_list, scroll)
            building.draw(blit_list, scroll)

            for p in players:
                if p.online:
                    draw_x = p.obj.x - scroll[0]
                    draw_y = p.obj.y - scroll[1]
                    draw_z = p.obj.z - scroll[2]

                    if p.obj.z != -1000:
                        scale = 1000 / (1000 + draw_z)
                        draw_x = draw_x * scale
                        draw_y = draw_y * scale

                    draw_x += 640
                    draw_y += 360

                    blit_list.append({"surf": pygame.transform.scale_by(player_img, scale), "pos": (draw_x, draw_y), "z": p.obj.z})

            for item in sorted(blit_list, key=lambda surf: surf["z"], reverse=True):
                if item["surf"]:
                    screen.blit(item["surf"], (item["pos"]))

            pygame.display.update()

            clock.tick(300)
            now = time.time()
            dt = (now - pt) * 60
            dt = min(dt, 4)
            pt = now
        except Exception as e:
            print(e)
            break
    pygame.quit()


start_new_thread(game_loop, ())

while running:
    conn, addr = s.accept()
    print("Connected to:", addr)

    players.append(Player())
    start_new_thread(threaded_client, (conn, player))
    player += 1
