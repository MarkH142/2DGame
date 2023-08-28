import World.WorldCommon as WC
import World.World as wo
from World.WorldObject import WorldObject
import pygame
from World.Chars.Character import AnimType
import UI.UI as UI

class Action():
    def __init__(self, element):
        pass
    
    def Enter(self, char):
        pass

    def Exit(self, char):
        pass

    def Act(self, char, deltaTime):
        pass

class IdleAction(Action):
    def Enter(self, char):
        char.animType = AnimType.IDLE
        char.walkChannel.pause()
class ChaseAction(Action):
    def __init__(self, element):
        self.walkSound = WorldObject._LoadSoundEffect("TinyAdventurePack/Data/Footsteps-in-grass-fast.mp3")
        
        self.speed = float(element.get("speed"))
        super().__init__(element)

    def Enter(self, char):
        char.animType = AnimType.WALK
        self.walkChannel = self.walkSound.play()    
        self.walkChannel.unpause()
        self.target = WC.Players[0]
        char.moveDir, len = WC.ComputeDir(char.GetCenterPosition(), 
                                           self.target.GetCenterPosition())
        super().Enter(char)

    def Act(self, char, deltaTime):
        WC.MoveDir(char, char.moveDir, self.target.GetCenterPosition(), 
                                        self.speed, deltaTime)
        char.moveDir, len = WC.ComputeDir(char.GetCenterPosition(), 
                                    self.target.GetCenterPosition())
        super().Act(char, deltaTime)
class ReturnAction(Action):
    pass


def CreateAction(element):
    action = element.find("Action")
    if action == None:
        return None
    atype = action.get("type")
    if atype == "Idle":
        return IdleAction(action)
    if atype == "Chase":
        return ChaseAction(action)
    if atype == "Return":
        return ReturnAction(action)
    return None

class Decision():
    def __init__(self, element, state):
        self.state = state
        self.trueState = element.get("trueState")
        self.falseState = element.get("falseState")
    

class PlayerInRange(Decision):
    def __init__(self, element, state):
        super().__init__(element, state)
        self.dist = int(element.get("distance"))
        self.distSqr = self.dist * self.dist

    def Decide(self, char):
        if hasattr(self.state.action, 'target'):
            target = self.state.action.target
        else:
            target = WC.Players[0]
        playerBox = target.GetCollisionBox()
        aiBox = char.GetCollisionBox()

        xdiff = 0
        ydiff = 0

        # Calculations for xdiff and ydiff used in lectures did not work correctly
        if playerBox.x > aiBox.x:
            xdiff = playerBox.x - aiBox.x - 64
            if xdiff < 0:
                xdiff = 0
        elif playerBox.x < aiBox.x:
            xdiff = aiBox.x - playerBox.x - 44
            if xdiff < 0:
                xdiff = 0
        
        
        if playerBox.y > aiBox.y:
            ydiff = playerBox.y - aiBox.y - 13
            if xdiff < 0:
                xdiff = 0
        elif playerBox.y < aiBox.y:
            ydiff = aiBox.y - playerBox.y -13
            if xdiff < 0:
                xdiff = 0

        ydiff= ydiff+1
        len = xdiff * ydiff + ydiff * ydiff
        totdif = xdiff + ydiff
        global _uiObjects

        #If player is touching enemy player dies
        if totdif < 3:
            if xdiff <= 1:
                for obj in wo._worldObjects:
                    if hasattr(obj, "isPlayer"):
                        print("Player has Died")
                        wo._worldObjects.remove(target)
                        del target
                        pygame.time.delay(1000)
                        print("ending game")
                        pygame.time.delay(1000)
                        pygame.quit()

        
        for obj in wo._worldObjects:
            if hasattr(obj, "isRock"):
                rockBox = obj.GetCollisionBox()
                
                rxdiff = 0
                rydiff = 0
                if rockBox.x < aiBox.x:
                    rxdiff = aiBox.x - rockBox.x
                elif rockBox.x > aiBox.x + aiBox.width:
                    rxdiff = rockBox.x - (aiBox.x + aiBox.width)
                elif rockBox.x + rockBox.width < aiBox.x:
                    rxdiff = aiBox.x - (rockBox.x + rockBox.width)
            
                if rockBox.y > aiBox.y:
                    rydiff = rockBox.y - aiBox.y
                elif rockBox.y < aiBox.y:
                    rydiff = aiBox.y - rockBox.y

                lenr = rxdiff * rydiff + rydiff * rydiff
                if lenr < 1:
                    char.hp = char.hp -1
                    pygame.time.delay(50)
        
        if char.hp == 0:
            print(char)
            wo._worldObjects.remove(char)
            WC.PhysicsEngine.remove(obj.body, obj.shape)
            print("Enemy Defeated!")
        return len < self.distSqr

class HomeInRange(Decision):
    pass

class WasAttacked(Decision):
    pass

class TimeIsUp(Decision):
    pass

def CreateDecision(element, state):
    type = element.get("decide")
    if type == "player_in_range":
        return PlayerInRange(element, state)
    if type == "home_in_range":
        return HomeInRange(element, state)
    if type == "was_attacked":
        return WasAttacked(element, state)
    if type == "time_is_up":
        return TimeIsUp(element, state)
    return None
    
class State():
    def __init__(self, element):
        self.name = element.get("name")
        self.action = CreateAction(element)
        self.decisions = []
        for decision in element.findall("Decision"):
            self.decisions.append(CreateDecision(decision, self))

    def Update(self, char, deltaTime):
        self.action.Act(char, deltaTime)
        for decision in self.decisions:
            result = decision.Decide(char)
            if result:
                if decision.trueState != char.curState:
                    self.action.Exit(char)
                    return decision.trueState
            else:
                if decision.falseState != char.curState:
                    self.action.Exit(char)
                    return decision.falseState
        return None


