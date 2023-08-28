import pygame
import numpy as np
import pymunk
import threading
from pymunk.vec2d import Vec2d
from World.WorldObject import WorldObject
import World.WorldCommon as WC
from World.Chars.Character import Character, AnimType

class Player(Character):
    def __init__(self, path, size):
        self.speed = 200.0
        self.mousemove = False
        self.isPlayer = True
        self.moveDir = np.asfarray([1.0, 0])
        self.step = 10
        self.PlayerAlive = True
        self.isThrowing = False
        super().__init__(path, size)
        
        self.walkChannel = self.walkSound.play()
        self.walkChannel.pause()

    def ProcessEvent(self, event):
        
        (x,y) = self.GetCenterPosition()


        #KEYBOARD MOVEMENT
        pygame.key.set_repeat(10,10)
        key_input = pygame.key.get_pressed()   
        if key_input[pygame.K_LEFT]:
            x -= self.step
            self.mouseTarget = (x,y)
            self.moveDir, len = WC.ComputeDir(self.GetCenterPosition(), self.mouseTarget)
            self.mousemove = True if len != 0 else False
        if key_input[pygame.K_UP]:
            y -= self.step
            self.mouseTarget = (x,y)
            self.moveDir, len = WC.ComputeDir(self.GetCenterPosition(),self.mouseTarget)
            self.mousemove = True if len != 0 else False
        if key_input[pygame.K_RIGHT]:
            x += self.step
            self.mouseTarget = (x,y)
            self.moveDir, len = WC.ComputeDir(self.GetCenterPosition(), self.mouseTarget)
            self.mousemove = True if len != 0 else False
        if key_input[pygame.K_DOWN]:
            y += self.step
            self.mouseTarget = (x,y)
            self.moveDir, len = WC.ComputeDir(self.GetCenterPosition(), self.mouseTarget)
            self.mousemove = True if len != 0 else False


        #MOUSEMOVEMENT
        if event.type == pygame.MOUSEBUTTONDOWN:
            left, middle, right = pygame.mouse.get_pressed()

            if left:
                self.mouseTarget = np.asfarray(pygame.mouse.get_pos()) - WC.CameraXY
                self.moveDir, len = WC.ComputeDir(self.GetCenterPosition(), self.mouseTarget)
                self.mousemove = True if len != 0 else False
                return True 
        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            self.isThrowing = True
            rock = WorldObject("TinyAdventurePack/Other/Rock.png", np.array([15,15]), body_type=pymunk.Body.DYNAMIC)
            rock.isRock = True
            rock.shape.friction = 0
            rock.SetCenterPosition(self.GetCollisionBoxCenter() + (self.moveDir * 45))
            dir = Vec2d(self.moveDir[0], self.moveDir[1])
            rock.body.apply_impulse_at_world_point(dir *2500.0, rock.body.position)
            rock.timeToDestruction = 2.0
            
            WC.NewWorldObjects.append(rock)
            return True
        return False
    
    def GetCenterPosition(self):
        return self.pos + (self.size / 2.0)

    def Update(self, deltaTime):

        if self.isThrowing:
            self.animType = AnimType.ATTACK
            threading.Timer(0.2, self.ResetIsThrowing).start()
           
        else:
            if self.mousemove:
                self.mousemove = WC.MoveDir(self, self.moveDir, self.mouseTarget,
                                        self.speed, deltaTime)
                self.animType = AnimType.WALK
                self.walkChannel.unpause()
            else:
                self.animType = AnimType.IDLE
                self.walkChannel.pause()
        super().Update(deltaTime)


    def ResetIsThrowing(self):
        self.isThrowing = False
    def Render(self, screen):
        super().Render(screen)

