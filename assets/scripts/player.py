import assets.scripts.ragdoll as ragdoll
from assets.scripts.object import Object
import pygame

class Player:
    def __init__(self):
        self.obj = Object(300, 0, 0, 30, 100, 30)
        self.layer = 0
        self.movement = [0, 0, 0]
        self.can_jump = False
        self.collisions = {"right": False, "left": False, "top": False, "bottom": False, "front": False, "back": False}
        self.y_momentum = 0
        self.air_timer = 0
        self.online = True
        self.in_vehicle = False

    def update(self, dt, rects):
        if not self.in_vehicle:
            self.move(dt, rects)

    def move(self, dt, objects):
        self.y_momentum += 0.1 * dt
        self.y_momentum = min(self.y_momentum, 1)
        self.movement[1] += self.y_momentum * dt

        self.collisions = {"right": False, "left": False, "top": False, "bottom": False, "front": False, "back": False}

        self.obj.move([self.movement[0] * dt, 0, 0])
        for o in objects:
            if self.obj.collideobj(o):
                o.define_values()
                if self.movement[0] > 0:
                    self.collisions["left"] = True
                    self.obj.x = o.left - self.obj.width
                elif self.movement[0] < 0:
                    self.collisions["right"] = True
                    self.obj.x = o.right

        self.obj.move([0, self.movement[1] * dt, 0])
        for o in objects:
            if self.obj.collideobj(o):
                o.define_values()
                if self.movement[1] > 0:
                    self.collisions["bottom"] = True
                    self.obj.y = o.top - self.obj.height
                elif self.movement[1] < 0:
                    self.collisions["top"] = True
                    self.obj.y = o.bottom

        self.obj.move([0, 0, self.movement[2] * dt])
        self.obj.z = max(0, self.obj.z)
        self.obj.z = min(970, self.obj.z)
        for o in objects:
            if self.obj.collideobj(o):
                o.define_values()
                if self.movement[2] > 0:
                    self.collisions["back"] = True
                    self.obj.z = o.front - self.obj.length
                elif self.movement[2] < 0:
                    self.collisions["front"] = True
                    self.obj.z = o.back


        if self.collisions["bottom"]:
            self.air_timer = 0
            self.y_momentum = 0
            self.movement[1] = 0
        else:
            self.air_timer += 1 * dt
