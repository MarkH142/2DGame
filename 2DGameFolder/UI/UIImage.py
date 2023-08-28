import pygame
import numpy as np
import World.WorldCommon as WC

class UIImage():
    def __init__(self, element=None):
        if element != None:
            self.path = element.get("path", None)
            if self.path == None:
                self.surf = None
            else:
                self.surf = pygame.image.load(self.path)
            self.x = int(element.get("x", 0))
            self.y = int(element.get("y", 0))
            self.width = int(element.get("width", 0))
            self.height = int(element.get("height", 0))
            if self.surf != None:
                self.surf = pygame.transform.scale(self.surf,(self.width, self.height))
            self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))
            self.justify = element.get("justify", "left")
            self.vjustify = element.get("vjustify", "top")
            anchor = element.find("Anchor")
            if anchor != None:
                self.anchorX = float(anchor.get("x", 0))
                self.anchorY = float(anchor.get("y", 0)) 
            else:
                self.anchorX = 0
                self.anchorY = 0
            v = element.get("visable", "false")
            self.visable = v = "true"
            self._CalcRect()
    def _CalcRect(self):
        self.rect.left = self.anchorX * WC.ScreenSize[0] + self.x
        if self.justify == "right":
            self.rect.left -= self.width
        elif self.justify == "center":
            self.rect.left -= self.width // 2

        self.rect.top = self.anchorY * WC.ScreenSize[1] + self.y
        if self.vjustify == "bottom":
            self.rect.top -= self.height
        elif self.vjustify == "center":
            self.rect.top -= self.height // 2

        self.rect.width = self.width
        self.rect.height = self.height
    def ProcessEvent(self, event):
        return False

    def Update(self, deltaTime):
        pass

    def Render(self, screen):
        if self.visable and self.surf != None:
            screen.blit(self.surf, self.rect)
        
    