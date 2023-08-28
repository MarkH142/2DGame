import pygame
pygame.init()

size = width, height = 640, 480
screen = pygame.display.set_mode(size)
pygame.mixer.init(frequency=22050, size=16,channels=2, buffer=4096)
import World.World as World
World.Init(size, screen)

import UI.UI as UI
UI.Init()

def Update(deltaTime):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if UI.ProcessEvent(event) == True:
            continue
        if World.ProcessEvent(event) == True:
            continue


    World.Update(deltaTime)
    UI.Render(screen)
    return True

def Render(screen):
    screen.fill((0,0,0))
    World.Render(screen)
    UI.Render(screen)
    pygame.display.flip()


_gTickLastFrame = pygame.time.get_ticks()
_gDeltaTime = 0,0
while Update(_gDeltaTime):
    Render(screen)
    t = pygame.time.get_ticks()
    _gDeltaTime = (t - _gTickLastFrame) / 1000.0 #converts to seconds
    _gTickLastFrame = t


World.Cleanup()