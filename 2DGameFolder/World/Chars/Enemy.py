import pygame
import numpy as np
from World.Chars.Character import Character
from World.Chars.NPCState import State

class Enemy(Character):
    def __init__(self, path=None, size=None, element=None):
        self.speed = 100
        self.size = (0,0,36,25)
        self.isEnemy = True
        self.moveDir = np.asfarray([1.0,0])
        self.curState = None
        self.stateList = {}
        self.hp = 4
        if element != None:
            ai = element.find("AI")
            if ai != None:
                for state in ai.findall("State"):
                    s = State(state)
                    
                    self.stateList[s.name] = s
                    if self.curState == None:
                        self.curState = s.name

        super().__init__(element=element, path= path, size = size)
        self.walkChannel = self.walkSound.play()
        self.walkChannel.pause()
    def Update(self, deltaTime):
        if self.curState != None:
            result = self.stateList[self.curState].Update(self, deltaTime)
            if result is not None:
                self.curState = result
                self.stateList[self.curState].action.Enter(self)
        super().Update(deltaTime)