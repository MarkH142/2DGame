import math
import numpy as np

ObjectSize = np.array([32,32])
ScreenSize = np.array([1,1])
PhysicsEngine = None
Players = [None, None]
MyPlayerIndex = 0
CameraXY = np.array([0,0])
NewWorldObjects = []

def ComputeDir(src, tgt):
    dir = tgt - src
    dir2 = dir * dir
    len = math.sqrt(np.sum(dir2))
    if len != 0:
        dir /= len
    return dir, len

def MoveDir(char, originalDir, target, speed, deltaTime):
    myPos = char.GetCenterPosition()
    dir, len = ComputeDir(myPos, target)

    if len == 0:
        return False
    else:
        prod = dir * originalDir
        dotpr = np.sum(prod)
        if dotpr < 0:
            return False
        else:
            char.SetCenterPosition(myPos + speed * deltaTime * dir)
    return True