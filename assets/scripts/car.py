import pygame

class Car:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 300, 150)
        self.movement = [0, 0]
        self.acceleration = 0
        self.y_momentum = 0
        self.speed = 20
        self.driver = None
        self.collisions = {"right": False, "left": False, "top": False, "bottom":False}

    def update(self, dt, rects):
        self.y_momentum += 0.1 * dt
        self.y_momentum = min(self.y_momentum, 5)
        self.movement[1] += self.y_momentum * dt
        self.movement[0] += self.acceleration * dt
        if self.movement[0] > 0:
            self.movement[0] = min(self.movement[0], self.speed)
        else:
            self.movement[0] = max(self.movement[0], -self.speed)
        self.movement[0] *= 0.99

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
            self.y_momentum = 0
            self.movement[1] = 0

        if self.driver:
            self.driver.rect.x = self.rect.x + 200
            self.driver.rect.y = self.rect.y + 10

    def draw(self, screen, scroll):
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height))
