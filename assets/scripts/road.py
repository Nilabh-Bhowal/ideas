from assets.scripts.object import Object
import pygame
import itertools

class Road:
    def __init__(self):
        self.obj = Object(-5000, 0, 0, 10000, 200, 1000)
        self.scale = 16
        # self.scale_factors = [1000 / (1000 + z * self.scale - scroll[2]) for z in range(50)]
        self.load_img()

    def load_img(self):
        texture = [pygame.transform.scale(pygame.image.load("assets/images/sprite_stacks/road/0.png").convert(), (256, 16)),
                    pygame.transform.scale(pygame.image.load("assets/images/sprite_stacks/road/1.png").convert(), (256, 16))]

        self.texture = []
        surf0 = pygame.Surface((3072, 16))
        surf1 = pygame.Surface((3072, 16))
        for x in range(12):
            surf0.blit(texture[0], (x * 256, 0))
            surf1.blit(texture[1], (x * 256, 0))
        self.texture.append(surf0)
        self.texture.append(surf1)

    def draw(self, blit_list, scroll):
        scale_factors = [1000 / (1000 + z * self.scale - scroll[2]) for z in range(50)]

        for x, z in itertools.product(range(2), range(50)):
            draw_x = x * 3072 - scroll[0] % 3072 - 1200
            draw_y = -scroll[1]

            scale = scale_factors[z]
            draw_x = draw_x * scale
            draw_y = draw_y * scale

            draw_x += 640
            draw_y += 360

            if draw_y < 720:
                if z % 16 == 8:
                    blit_list.append({"surf": pygame.transform.scale_by(self.texture[1], scale), "pos": (draw_x, draw_y), "z": z * 16, "a": 255})
                else:
                    blit_list.append({"surf": pygame.transform.scale_by(self.texture[0], scale), "pos": (draw_x, draw_y), "z": z * 16, "a": 255})
