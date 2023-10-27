import pygame
import math
import json
import assets.scripts.ui as ui

pygame.init()

screen = pygame.display.set_mode((1280, 720))

mode = "points"
points = []
sticks = []
grounded = []
rigs = []
point_rects = []
pressed = False
selected_point = "none"

rig_name_prompt = ui.PromptBox("Name of rig")

def angle(p1, p2):
    return round(math.degrees(math.atan2(p1[1] - p2[1], p1[0] - p2[0])))

def add_rig(rig_name, sticks):
    rigs.append({"name": f"{rig_name}", "positions": [angle(stick[0], stick[1]) for stick in sticks]})

def save(points, sticks, grounded, rigs):
    data = {"points": [], "sticks": [], "grounded": [], "rigs": [], "animations": []}
    for point in points:
        data["points"].append(point)
    for stick in sticks:
        data["sticks"].append([data["points"].index(stick[0]), data["points"].index(stick[1])])
    for point in grounded:
        data["grounded"].append(data["points"].index(point))
    for rig in rigs:
        data["rigs"].append(rig)

    with open("e.json", "w") as f:
        json.dump(data, f)

def load(file):
    points = []
    point_rects = []
    with open(file, "r") as f:
        data = json.load(f)
    for point in data["points"]:
        points.append(point)
        point_rects.append(pygame.Rect(point[0] * 30, point[1] * 30, 30, 30))
    sticks = [[points[stick[0]], points[stick[1]]] for stick in data["sticks"]]
    grounded = [points[point] for point in data["grounded"]]
    rigs = list(data["rigs"])
    return points, point_rects, sticks, grounded, rigs

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and rig_name_prompt.prompted:
            if event.key == pygame.K_1:
                mode = "points"
            elif event.key == pygame.K_2:
                mode = "sticks"
            elif event.key == pygame.K_r:
                mode = "rig"
                rig_name_prompt.prompt()
            elif event.key == pygame.K_d:
                points = []
                sticks = []
                grounded = []
                rigs = []
                point_rects = []
                selected_point = "none"
            elif event.key == pygame.K_s:
                save(points, sticks, grounded, rigs)
            elif event.key == pygame.K_l:
                points, point_rects, sticks, grounded, rigs = load("e.json")
                selected_point = "none"

        rig_name_prompt.handle_input(event)

    if mode == "points" and rig_name_prompt.prompted:
        selected_point = "none"
        if pygame.mouse.get_pressed()[0]:
            if not pressed:
                points.append([round((pygame.mouse.get_pos()[0] - 15) / 30), round((pygame.mouse.get_pos()[1] - 15) / 30)])
                point_rects.append(pygame.Rect(round((pygame.mouse.get_pos()[0] - 15) / 30) * 30, round((pygame.mouse.get_pos()[1] - 15) / 30) * 30, 30, 30))
            pressed = True
        elif pygame.mouse.get_pressed()[1]:
            if not pressed:
                points.append([round((pygame.mouse.get_pos()[0] - 15) / 30), round((pygame.mouse.get_pos()[1] - 15) / 30)])
                point_rects.append(pygame.Rect(round((pygame.mouse.get_pos()[0] - 15) / 30) * 30, round((pygame.mouse.get_pos()[1] - 15) / 30) * 30, 30, 30))
                grounded.append([round((pygame.mouse.get_pos()[0] - 15) / 30), round((pygame.mouse.get_pos()[1] - 15) / 30)])
            pressed = True
        elif pygame.mouse.get_pressed()[2]:
            for point in point_rects:
                if point.collidepoint(pygame.mouse.get_pos()):
                    points.pop(point_rects.index(point))
                    point_rects.remove(point)
                    break
        else:
            pressed = False
    elif mode == "sticks" and rig_name_prompt.prompted:
        if pygame.mouse.get_pressed()[0]:
            if not pressed:
                if selected_point == "none":
                    for point in point_rects:
                        if point.collidepoint(pygame.mouse.get_pos()):
                            selected_point = point
                else:
                    for point in point_rects:
                        if point.collidepoint(pygame.mouse.get_pos()) and point != selected_point and ([[point.centerx / 30, point.centery / 30], [selected_point.centerx / 30, selected_point.centery / 30]] not in sticks or [[selected_point.centerx / 30, selected_point.centery / 30], [point.centerx / 30, point.centery / 30]] not in sticks):
                            sticks.append([[(int(selected_point.centerx / 30 - 0.5)), (int(selected_point.centery / 30 - 0.5))], [(int(point.centerx / 30 - 0.5)), (int(point.centery / 30 - 0.5))]])
                            selected_point = "none"
            pressed = True
        else:
            pressed = False

    print(rigs)

    screen.fill((105, 235, 255))
    for point in point_rects:
        if [point.centerx * 30, point.centery * 30] in grounded:
            pygame.draw.rect(screen, (0, 0, 0), point)
        else:
            pygame.draw.rect(screen, (148, 75, 16), point)

    for stick in sticks:
        pygame.draw.line(screen, (148, 75, 16), [stick[0][0] * 30, stick[0][1] * 30], [stick[1][0] * 30, stick[1][1] * 30], 5)

    for x in range(43):
        pygame.draw.line(screen, (0, 0, 0), (x * 30, 0), (x * 30, 720))
    for y in range(43):
        pygame.draw.line(screen, (0, 0, 0), (0, y * 30), (1280, y * 30))

    if rig_name := rig_name_prompt.draw(screen):
        add_rig(rig_name, sticks)
        rig_name = None


    pygame.display.update()

pygame.quit()
