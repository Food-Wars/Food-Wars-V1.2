'''All nessecary methods for loading spritesheets'''

from pathlib import Path
import json

import pygame

def loadImgs(dataPath):
    '''Loads images using path to the json data'''

    with open(dataPath, "r") as file:
        data = json.load(file)

        output = {}

        #images should be in the same directory as the json data file
        imgPath = Path(dataPath.parent, data["meta"]["image"])

        output["img"] = pygame.image.load(imgPath)

        for sprite in data["frames"].keys():
            output[sprite] = {}
            output[sprite]["coords"] = data["frames"][sprite]["frame"]
        
        return output