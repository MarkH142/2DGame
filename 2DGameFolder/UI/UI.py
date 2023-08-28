import pygame
import xml.etree.ElementTree as ET
from UI.UIImage import UIImage

def Init():
    global _uiObjects
    _uiObjects = []
    tree = ET.parse("TinyAdventurePack/Data/UI.xml")
    root = tree.getroot()
    groups = root.find("Group")
    if groups != None:
        for element in groups.findall("*"):
            if element.tag == "Image":
                img = UIImage(element)
                _uiObjects.append(img)
def ProcessEvent(event):
    global _uiObjects
    for i in reversed(_uiObjects):
        if i.ProcessEvent(event) == True:
            return True
    return False

def Update(deltaTime):
    global _uiObjects
    for i in _uiObjects:
        i.Update(deltaTime)

def Render(screen):
    global _uiObjects
    for i in _uiObjects:
        i.Render(screen)

def Cleanup():
    pass