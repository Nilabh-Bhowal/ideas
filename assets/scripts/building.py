import json
import itertools
import pygame
from assets.scripts.object import Object

class Building:
    def __init__(self, x, z, file):
        print(file)
        with open(f"assets/building/{file}.json") as f:
            data = json.load(f)
        self.objs = [Object(x + d[0], d[1], z + d[2], d[3], d[4], d[5]) for d in data]
        self.x = x
        self.z = z
        self.scale = 16
        self.texture = [pygame.transform.scale_by(pygame.image.load("assets/images/sprite_stacks/building/0.png").convert(), self.scale), pygame.transform.scale_by(pygame.image.load("assets/images/sprite_stacks/building/1.png").convert(), self.scale), pygame.transform.scale_by(pygame.image.load("assets/images/sprite_stacks/building/2.png").convert(), self.scale)]

    def draw(self, blit_list, scroll, player=None):

        for i, o in enumerate(self.objs):
            if i < 2:
                draw_x = o.x - scroll[0]
                draw_y = o.y - scroll[1]
                draw_z = o.centerz
                if draw_z != -1000:
                    scale = 1000 / (1000 + draw_z)
                    draw_x = draw_x * scale
                    draw_y = draw_y * scale

                draw_x += 640
                draw_y += 360

                if draw_x < 1280 and draw_x > -800 * scale:
                    if i == 0:
                        if (player and (player.obj.right <= o.left or player.obj.left >= o.right or player.obj.front < o.back)):
                            blit_list.append({"surf": pygame.transform.scale_by(self.texture[0], scale), "pos": (draw_x, draw_y), "z": o.back, "a": 255})
                        else:
                            blit_list.append({"surf": pygame.transform.scale_by(self.texture[0], scale), "pos": (draw_x, draw_y), "z": o.back, "a": 50})
                    elif i == 1:
                        blit_list.append({"surf": pygame.transform.scale_by(self.texture[0], scale), "pos": (draw_x, draw_y), "z": o.front, "a": 255})
            else:
                for z in range(int(o.length / 16)):
                    draw_x = o.x - scroll[0]
                    draw_y = o.y - scroll[1]
                    draw_z = o.back - z * self.scale
                    if z != -1000:
                        scale = 1000 / (1000 + draw_z)
                        draw_x = draw_x * scale
                        draw_y = draw_y * scale

                    draw_x += 640
                    draw_y += 360

                    if draw_x < 1280 and draw_x > -800 * scale:
                        if i == 2:
                            blit_list.append({"surf": pygame.transform.scale_by(self.texture[1], scale), "pos": (draw_x, draw_y), "z": o.back - z * 16, "a": 255})
                        else:
                            blit_list.append({"surf": pygame.transform.scale_by(self.texture[2], scale), "pos": (draw_x, draw_y), "z": o.back - z * 16, "a": 255})
