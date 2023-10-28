import pygame
import time
import assets.scripts.ui as ui
import multiplayer
import singleplayer

pygame.init()

screen = pygame.display.set_mode((1280, 720))

def main_menu():
    clock = pygame.time.Clock()
    pt = time.time()
    dt = 1
    running = True
    play_button = ui.Button("Play", 300, 400, 50, 25, "popup")
    singleplayer_button = ui.Button("Singleplayer", 300, 700, 50, 25, "popup")
    server_prompt = ui.PromptBox("Server:")
    while running:

        for event in pygame.event.get():
            server_prompt.handle_input(event)
            if event.type == pygame.QUIT:
                running = False

        screen.fill((105, 235, 255))
        ui.heading("tittle", 640, 200, screen, (0, 0, 0))

        if play_button.draw(screen, 0, pygame.mouse.get_pos()):
            server_prompt.prompt()

        if singleplayer_button.draw(screen, 0, pygame.mouse.get_pos()) and (singleplayer.run(screen)):
            running = False

        if server := server_prompt.draw(screen):
            if multiplayer.run(screen, server):
                running = False
            server = None

        pygame.display.update()

        clock.tick(60)
        now = time.time()
        dt = (now - pt) * 60
        dt = min(dt, 4)
        pt = now

    pygame.quit()

if __name__ == "__main__":
    main_menu()
