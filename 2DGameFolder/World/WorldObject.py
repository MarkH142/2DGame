
import pygame 
import numpy as np
import pymunk
import World.WorldCommon as WC
class WorldObject():
    _loadedImages = {}
    _loadedSoundEffects = {}
    
    

    @staticmethod
    def _LoadSurf(path, size= None):
        key = path + str(size)
        if key in WorldObject._loadedImages:
            return WorldObject._loadedImages[key], \
                np.array(WorldObject._loadedImages[key].get_rect().size)
        try:
            surf = pygame.image.load(path)
        except:
            return None, None
        if size is None:
            size = np.array(surf.get_rect().size) * 4
        surf = pygame.transform.scale(surf, size)
        WorldObject._loadedImages[key] = surf
        return surf, size.copy()

    @staticmethod
    def _LoadSoundEffect(path):
        if path in WorldObject._loadedSoundEffects:
            return WorldObject._loadedSoundEffects[path]
        try:
            sound = pygame.mixer.Sound(path)
        except:
            return None
        WorldObject._loadedSoundEffects[path] = sound
        return sound
    def __init__(self, path, size, element=None, body_type=pymunk.Body.STATIC):
        self.body = None
        self.timeToDestruction = -1
        
        self.path = path if path is not None or element is None else element.get("path")
        self.surf, self.size = WorldObject._LoadSurf(self.path, size)

        
        

        self.pos = np.asfarray([0,0])
        if element is not None:
            self.SetCenterPosition(np.asfarray([float(element.get("x")), float(element.get("y"))]))
        

        

        self.rect = pygame.Rect(self.pos, self.size)
        if hasattr(self, "shape"):
            if self.shape == "capsule":
                self.col_type = "capsule"
        else:
            self.col_type = "rect"
      
        
        self.col_rect = pygame.Rect((0,0), self.size)
        if element != None:
            col_elem = element.find("Col")
            if col_elem != None:
                self.col_rect = pygame.Rect((int(col_elem.get("xoff")),
                                            int(col_elem.get("yoff"))),
                                            (int(col_elem.get("w")),
                                            int(col_elem.get("h"))))
                self.col_type = col_elem.get("type")
        
        mass = 10
        moment = 10
        self.body = pymunk.Body(mass, moment, body_type)
        center = self.GetCollisionBoxCenter()
        self.body.position = center[0], center[1]
        WC.PhysicsEngine.reindex_shapes_for_body(self.body)
        
        box = self.GetCollisionBox()
        w = self.col_rect.w
        h = self.col_rect.h
        if hasattr(self, "isChar"):
            w = w / 3
            w = w + 10
            h = h / 3
            w = w / 6
        oval = ((-w/2,-h/4), (0,-h/2), (w/2,-h/4), (w/2,h/4), (0,h/2), (-w/2,h/4))
        capsule =  ((-w/2,-h/2), (-w/4,-h), (0,-h), (w/4,-h), (w/2,-h/2), (w/2,h/2), (w/4,h), (0,h), (-w/4,h), (-w/2,h/2))
        if hasattr(self, "col_type"):
            if self.col_type == "rect":
                self.shape = pymunk.Poly.create_box(self.body, box.size)
            elif self.col_type == "oval":
                self.shape = pymunk.Poly(self.body, oval)
            elif self.col_type == "capsule":
                self.shape = pymunk.Poly(self.body, capsule)

        if hasattr(self, "isChar"):
            WC.PhysicsEngine.add(self.body, self.shape)
        else:
            WC.PhysicsEngine.add(self.body, self.shape)

        

        
    def ProcessEvent(self, event):
        return False

    def SetCenterPosition(self, pos, teleport = False):
        self.pos = pos - (self.size / 2.0)

        if self.body != None:
            center = self.GetCollisionBoxCenter()
            
            self.body.position = center[0],  center[1]
            WC.PhysicsEngine.reindex_shapes_for_body(self.body)

    def GetCollisionBox(self):
        return pygame.Rect(self.pos + np.asfarray(self.col_rect.topleft), self.col_rect.size)
                                    
    def GetCollisionBoxCenter(self):
        box = self.GetCollisionBox()
        return np.asfarray([box.x + (box.w / 2),box.y + (box.h / 2)])

    def GetCenterPosition(self):
        return self.pos + (self.size / 2.0)

    def DetectCol(self):
        pass
    def Update(self,deltaTime):
        if self.body.body_type == pymunk.Body.DYNAMIC:
            center = self.GetCollisionBoxCenter()
            self.pos[0] = self.body.position[0] \
                - (center[0] - self.pos[0])
            self.pos[1] = ( self.body.position[1]) \
                 - (center[1] - self.pos[1])
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        if self.timeToDestruction != -1:
            self.timeToDestruction -= deltaTime
            if self.timeToDestruction < 0:
                self.timeToDestruction = 0
    def Render(self,screen):
        rect = self.rect.copy()
        rect.x += WC.CameraXY[0]
        rect.y += WC.CameraXY[1]
        screen.blit(self.surf, rect)
