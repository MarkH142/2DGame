from glob import glob
import pygame
import pymunk
import pymunk.pygame_util
import numpy as np
import xml.etree.ElementTree as ET

import World.WorldCommon as WC
from World.WorldObject import WorldObject
from World.Chars.Player import Player
from World.Chars.Enemy import Enemy
def Init(screen_size, screen):
    global _grass
    global _objectRect
    global _width
    global _height
    global _worldObjects
    global _draw_options

    WC.PhysicsEngine = pymunk.Space()
    WC.PhysicsEngine.gravity = 0,0
    _draw_options = pymunk.pygame_util.DrawOptions(screen)
    WC.ScreenSize = np.array(screen_size)
    WC.Players[0] = Player("TinyAdventurePack/Character/Char_one", (WC.ObjectSize *4))
    WC.Players[0].SetCenterPosition(WC.ScreenSize / 2, teleport=True)
    _worldObjects = [WC.Players[0]]
    
    tree = ET.parse("TinyAdventurePack/Data/WorldData.xml")
    root = tree.getroot()

    objects = root.find("Objects")
    if objects != None:
        for object in objects.findall("Object"):
            wo = WorldObject(None, None, element=object)
            _worldObjects.append(wo)

    enemies = root.find("Enemies")
    if enemies != None:
        for enemy in enemies.findall("Enemy"):
            wo = Enemy(None, None, element=enemy)
            _worldObjects.append(wo)
    _grass = pygame.image.load("TinyAdventurePack/Other/Grass.png")
    _grass = pygame.transform.scale(_grass, WC.ObjectSize)
    _objectRect = pygame.Rect(0,0,WC.ObjectSize[0], WC.ObjectSize[1])
    _width = 640
    _height = 480

def ProcessEvent(event):
    global _worldObjects

    for i in _worldObjects:
        if i.ProcessEvent(event) == True:
            return True
            
    return False

def _SortWorldObjects(worldObject):
    box = worldObject.GetCollisionBox()
    return box.y + box.height
_timeStep = 1.0/60.0
_timeSinceLastFrame = 0
def Update(deltaTime):
    global _worldObjects
    global _timeStep
    global _timeSinceLastFrame
    if deltaTime != (0,0):
        _timeSinceLastFrame += deltaTime
    
    while (_timeSinceLastFrame >= _timeStep):
        WC.PhysicsEngine.step(_timeStep)
        _timeSinceLastFrame -= _timeStep
    
    WC.CameraXY = (WC.ScreenSize / 2) - WC.Players[0].GetCenterPosition()

    for i in _worldObjects:
        i.Update(deltaTime)

    for i in range(len(_worldObjects)-1, -1, -1):
        if _worldObjects[i].timeToDestruction == 0:
            WC.PhysicsEngine.remove(_worldObjects[i].shape, _worldObjects[i].body)
            del _worldObjects[i]

    for i in _worldObjects: 
        i.DetectCol()

    if len(WC.NewWorldObjects) > 0:
        _worldObjects += WC.NewWorldObjects
        WC.NewWorldObjects.clear()
    
    _worldObjects.sort(key=_SortWorldObjects)

def Render(screen):
    global _grass
    global _objectRect
    global _worldObjects
    global _draw_options

    screen_adjust = ()
    grassimg = makeTiledImage(_grass , _width, _height)
    screen.blit(grassimg, _objectRect,(0,0,640,480))

    for i in _worldObjects:
        i.Render(screen)
    # WC.PhysicsEngine.debug_draw(_draw_options)

def Cleanup():
    pass


def makeTiledImage( _grass, width, height ):
    x_cursor = 0
    y_cursor = 0

    tiled_image = pygame.Surface( ( width, height ) )
    while ( y_cursor < height ):
        while ( x_cursor < width ):
            tiled_image.blit( _grass, ( x_cursor, y_cursor ) )
            x_cursor += _grass.get_width()
        y_cursor += _grass.get_height()
        x_cursor = 0
    return tiled_image


def Cleanup():
    pass

