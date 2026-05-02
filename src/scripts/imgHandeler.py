'''All nessecary methods for loading spritesheets'''

import json

import pygame

def loadImgs(dataPath):
    '''Loads images using path to the json data'''

    with open(dataPath, "r") as file:
        data = json.load(file)

        output = {}

        output["img"] = pygame.image.load(data["meta"]["image"])

        for sprite in data["frames"].keys():
            output[sprite] = {}
            output[sprite]["coords"] = data["frames"][sprite]["frame"]
        
        return output

