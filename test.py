import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))

data = {"ee": True}
datas = {"data": data}

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    print(datas["data"]["ee"])

    pygame.display.update()

pygame.quit()
