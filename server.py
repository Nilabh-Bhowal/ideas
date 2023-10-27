import socket
from _thread import *
import pickle
import pygame
import threading
import math
import time
from assets.scripts.player import Player
from assets.scripts.car import Car

server = "localhost"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

players = []
cars = []
player = 0

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

ground = pygame.Rect(-5000, 400, 10000, 200)

def threaded_client(conn, player):  # sourcery skip: do-not-use-bare-except
    conn.sendall(pickle.dumps(players[player]))
    clock = pygame.time.Clock()
    pt = time.time()
    dt = 1
    while True:
        try:
            if data := pickle.loads(conn.recv(4096)):

                if players[player].in_vehicle:
                    for car in cars:
                        if car.driver == players[player]:
                            car.acceleration = (data["keymap"]["right"] - data["keymap"]["left"])
                else:
                    players[player].movement[0] = (data["keymap"]["right"] - data["keymap"]["left"]) * 5
                if data["keymap"]["up"]:
                    if jumped == False and players[player].air_timer < 10:
                        jumped = True
                        players[player].movement[1] = data["keymap"]["up"] * -15
                else:
                    jumped = False
                if data["keymap"]["car"]:
                    cars.append(Car(players[player].rect.x, players[player].rect.y))
                if data["keymap"]["ride"]:
                    for car in cars:
                        if players[player].rect.colliderect(car.rect):
                            car.driver = players[player] if car.driver != players[player] else None
                            players[player].in_vehicle = not players[player].in_vehicle

                players[player].update(dt, [ground])

                reply = [[p for p in players if p.online and math.dist(p.rect.center, players[player].rect.center) < 2000], [c for c in cars if math.dist(c.rect.center, players[player].rect.center) < 2000], players[player]]
                # print("Received: ", data)
                # print("Sending : ", reply)
                clock.tick()
                now = time.time()
                dt = (now - pt) * 60
                dt = min(dt, 4)
                pt = now
            else:
                print("Disconnected")
                break
            conn.sendall(pickle.dumps(reply))
        except Exception:
            break

    print("Lost connection")
    players[player].online = False
    conn.close()

def game_loop():
    clock = pygame.time.Clock()
    pt = time.time()
    dt = 1
    while True:
        print(dt)
        for car in cars:
            car.update(dt, [ground])
        clock.tick()
        now = time.time()
        dt = (now - pt) * 60
        dt = min(dt, 4)
        pt = now


game_thread = threading.Thread(target=game_loop)
game_thread.start()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    players.append(Player())
    start_new_thread(threaded_client, (conn, player))
    player += 1
