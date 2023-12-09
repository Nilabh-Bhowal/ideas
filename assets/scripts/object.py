import pygame

class Object:
    def __init__(self, x, y, z, width, height, length):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.length = length
        self.define_values()

    def define_values(self):
        self.left = self.x
        self.right = self.x + self.width
        self.top = self.y
        self.bottom = self.y + self.height
        self.front = self.z
        self.back = self.z + self.length
        self.centerx = self.x + self.width / 2
        self.centery = self.y + self.height / 2
        self.centerz = self.z + self.length / 2

    def move(self, vector):
        self.x += vector[0]
        self.y += vector[1]
        self.z += vector[2]
        self.define_values()

    def collideobj(self, obj):
        self.define_values()
        x_lined_up = (self.left < obj.right and self.right > obj.left) or (self.left < obj.left and self.right > obj.right)
        y_lined_up = (self.top < obj.bottom and self.bottom > obj.top) or (self.top < obj.top and self.bottom > obj.bottom)
        z_lined_up = (self.front < obj.back and self.back > obj.front) or (self.front < obj.front and self.back > obj.back)

        return x_lined_up and y_lined_up and z_lined_up

    def draw(self, blit_list, scroll, f=1000):
        vertices = [
            (self.left, self.top, self.front),
            (self.right, self.top, self.front),
            (self.right, self.bottom, self.front),
            (self.left, self.bottom, self.front),
            (self.left, self.top, self.back),
            (self.right, self.top, self.back),
            (self.right, self.bottom, self.back),
            (self.left, self.bottom, self.back)
        ]

        projected_vertices = []
        for vertex in vertices:
            x = vertex[0] - scroll[0]
            y = vertex[1] - scroll[1]
            z = vertex[2] - scroll[2]

            if z != -f:
                scale = f / (f + z)
                x = x * scale
                y = y * scale

            x += 640
            y += 360

            projected_vertices.append((x, y))

        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]
        draw_surf = pygame.Surface((1280, 720))
        for edge in edges:
            pygame.draw.line(draw_surf, (255, 0, 0), projected_vertices[edge[0]], projected_vertices[edge[1]])
        draw_surf.set_colorkey((0, 0, 0))
        blit_list.append({"surf": draw_surf, "pos": (0, 0), "z": self.z})
