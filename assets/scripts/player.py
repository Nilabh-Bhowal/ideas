import assets.scripts.ragdoll as ragdoll
import pygame

class Player:
    def __init__(self):
        self.ragdoll = ragdoll.Ragdoll("e")
        self.rect = pygame.Rect(300, 0, 30, 70)
        self.movement = [0, 0]
        self.can_jump = False
        self.collisions = {"right": False, "left": False, "top": False, "bottom":False}
        self.y_momentum = 0
        self.air_timer = 0
        self.online = True
        self.in_vehicle = False

    def update(self, dt, rects):
        if not self.in_vehicle:
            self.move(dt, rects)
        if self.movement[0] > 0:
            self.ragdoll.change_animation("right")
        elif self.movement[0] < 0:
            self.ragdoll.change_animation("left")
        else:
            self.ragdoll.change_animation("idle")

        self.ragdoll.move_grounded([self.rect.centerx, self.rect.centery + 10])
        self.ragdoll.update(dt)

    def move(self, dt, rects):
        self.y_momentum += 0.1 * dt
        self.y_momentum = min(self.y_momentum, 1)
        self.movement[1] += self.y_momentum * dt

        self.collisions = {"right": False, "left": False, "top": False, "bottom":False}

        self.rect.y += self.movement[1] * dt
        for rect in rects:
            if self.rect.colliderect(rect):
                if self.movement[1] > 0:
                    self.collisions["bottom"] = True
                    self.rect.bottom = rect.top
                elif self.movement[1] < 0:
                    self.collisions["top"] = True
                    self.rect.top = rect.bottom

        self.rect.x += self.movement[0] * dt
        for rect in rects:
            if self.rect.colliderect(rect):
                if self.movement[0] > 0:
                    self.collisions["right"] = True
                    self.rect.right = rect.left
                elif self.movement[0] < 0:
                    self.collisions["left"] = True
                    self.rect.left = rect.right

        if self.collisions["bottom"]:
            self.air_timer = 0
            self.y_momentum = 0
            self.movement[1] = 0
        else:
            self.air_timer += 1 * dt

    def draw(self, screen, scroll):
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height))
        self.ragdoll.draw(screen, scroll)
