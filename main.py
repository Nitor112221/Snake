import pygame

from scripts.menu import menu_scene

pygame.init()
screen = pygame.display.set_mode((800, 850))
current_scene = None
def switch_scene(scene):
    global current_scene
    current_scene = scene


switch_scene(menu_scene)
while current_scene is not None:
    if current_scene == "Menu":
        switch_scene(menu_scene)
    current_scene(screen, switch_scene)

pygame.quit()