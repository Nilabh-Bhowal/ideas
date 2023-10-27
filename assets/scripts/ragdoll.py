import pygame
import json
import math

def load_rag(data):
    with open(f"assets/ragdoll/{data}.json", "r") as f:
        return json.load(f)

def distance(p1, p2):
    return math.sqrt(((p2[0] - p1[0]) ** 2) + ((p2[1] - p1[1]) ** 2))

def angle(p1, p2):
    return math.degrees(math.atan2(p1[1] - p2[1], p1[0] - p2[0]))

class Ragdoll:
    def __init__(self, data):
        data = load_rag(data)
        self.points = [p + p for p in data["points"]]
        self.orig_points = [p + p for p in data["points"]]
        self.sticks = []
        for stick in data["sticks"]:
            self.add_stick(stick)
        self.grounded = data["grounded"]
        self.scale = 15
        self.alive = True
        self.rigs = data["rigs"]
        self.animations = data["animations"]
        self.curr_frame = 0
        self.curr_rig_num = 0
        self.curr_rig = 0
        self.curr_animation = "idle"

    def add_stick(self, points):
        self.sticks.append([points[0], points[1], distance(self.points[points[0]], self.points[points[1]])])

    def set_angle(self, dt, stick, target_angle):
        dx = math.cos(math.radians(-target_angle)) * stick[2]
        dy = math.sin(math.radians(-target_angle)) * stick[2]
        self.points[stick[1]][0] += ((dx + self.points[stick[0]][0]) - self.points[stick[1]][0]) * 0.2
        self.points[stick[1]][1] += ((dy + self.points[stick[0]][1]) - self.points[stick[1]][1]) * 0.2

    def move_grounded(self, offset):
        for i, point in enumerate(self.points):
            if i in self.grounded:
                point[0] = offset[0] / self.scale
                point[1] = offset[1] / self.scale
                point[2] = point[0]
                point[3] = point[1]

    def change_animation(self, animation):
        if self.curr_animation != animation:
            self.curr_animation = animation
            self.curr_frame = 0
            self.curr_rig_num = 0
            self.curr_rig = 0

    def update(self, dt):

        self.update_animation(dt)

        for i, point in enumerate(self.points):
            if i not in self.grounded or not self.alive:
                dx = point[0] - point[2]
                dy = point[1] - point[3]
                point[2] = point[0]
                point[3] = point[1]
                point[0] += dx
                point[1] += dy

        if self.alive:
            for stick in self.sticks:
                dis = distance(self.points[stick[0]][:2], self.points[stick[1]][:2])
                dis_dif = stick[2] - dis
                mv_ratio = dis_dif / dis / 2
                dx = self.points[stick[1]][0] - self.points[stick[0]][0]
                dy = self.points[stick[1]][1] - self.points[stick[0]][1]
                if stick[0] not in self.grounded:
                    self.points[stick[0]][0] -= dx * mv_ratio * 0.85
                    self.points[stick[0]][1] -= dy * mv_ratio * 0.85
                if stick[1] not in self.grounded:
                    self.points[stick[1]][0] += dx * mv_ratio * 0.85
                    self.points[stick[1]][1] += dy * mv_ratio * 0.85

    def update_animation(self, dt):
        if not self.alive:
            return
        self.curr_frame += 1
        for animation in self.animations:
            if animation["name"] == self.curr_animation and self.curr_frame > animation["frames"]:
                self.curr_rig_num += 1
                self.curr_frame = 0
                if self.curr_rig_num + 1 > len(animation["rigs"]):
                    self.curr_rig_num = 0
                rigs = animation["rigs"]
                self.curr_rig = rigs[self.curr_rig_num]
        for stick in self.sticks:
            for rig in self.rigs:
                if self.rigs.index(rig) == self.curr_rig:
                    angle = rig["positions"][self.sticks.index(stick)]
                    self.set_angle(dt, stick, angle)

    def draw(self, screen, scroll):
        render_pts = [[p[0] * self.scale - scroll[0], p[1] * self.scale - scroll[1]] for p in self.points]
        for stick in self.sticks:
            pygame.draw.line(screen, (224, 139, 70), render_pts[stick[0]], render_pts[stick[1]], 5)
