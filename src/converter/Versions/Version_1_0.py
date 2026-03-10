# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 17:21:33 2025

"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 16:11:28 2025

@author: zrobi
"""
#import libraries
import json
from os import path
import os
import numpy
#version class
class Version_1_0():
    '''Class for version 1.0 worlds'''
    def __init__(self, folder_path):
        self.path = folder_path
        self.version = '1.0'
        self.error = False
    @classmethod
    def create_from_other(cls, **kwargs):
        obj = cls.__new__(cls)
        obj.difficulty = kwargs['difficulty']
        obj.game_map = kwargs['game_map']
        obj.game_map_interactables = kwargs['game_map_interactables']
        obj.name = kwargs['name']
        obj.inventory = kwargs['main_inventory']
        obj.armour = kwargs['armour']
        obj.hotbar = kwargs['hotbar']
        obj.stats = kwargs['stats']
        obj.seed = kwargs['seed']
        obj.version = '1.0'
        return obj
    def load_files(self, root):
        #load in all files, with calls to refresh screen between them
        root.after(100, lambda: self.load_difficulty())
        root.after(110, lambda: self.load_game_map())
        root.after(120, lambda: self.load_interactable_map())
        root.after(130, lambda: self.load_name())
        root.after(140, lambda: self.load_items())
        root.after(150, lambda: self.load_stats())
        root.after(160, lambda: self.load_seed(root))
    def get_error(self, root):
        if self.error:
            root.event_generate("<<Error_Loading_World>>")
        else:
            root.event_generate("<<World_Loaded>>")
    def load_difficulty(self):
        if path.isfile(self.path + '/difficulty/difficulty.json'):
            with open(self.path + '/difficulty/difficulty.json', 'r') as difficulty:
                self.difficulty = json.load(difficulty)
        else:
            self.error = True
    def load_game_map(self):
        if path.isfile(self.path + '/map_data/game_map.json'):
            with open(self.path + '/map_data/game_map.json', 'r') as game_map:
                self.game_map = json.load(game_map)
        else:
            self.error = True
    def load_interactable_map(self):
        if path.isfile(self.path + '/map_data/game_map_interactables.json'):
            with open(self.path + '/map_data/game_map_interactables.json', 'r') as game_map:
                self.game_map_interactables = json.load(game_map)
        else:
            self.error = True
    def load_name(self):
        if path.isfile(self.path + '/name/world_name.json'):
            with open(self.path + '/name/world_name.json', 'r') as name:
                self.name = json.load(name)
        else:
            self.error = True
    def load_items(self):
        if path.isfile(self.path + '/player_data/armour.json'):
            with open(self.path + '/player_data/armour.json', 'r') as armour:
                self.armour = json.load(armour)
        else:
            self.error = True
        if path.isfile(self.path + '/player_data/hotbar.json'):
            with open(self.path + '/player_data/hotbar.json', 'r') as hotbar:
                self.hotbar = json.load(hotbar)
        else:
            self.error = True
        if path.isfile(self.path + '/player_data/inventory.json'):
            with open(self.path + '/player_data/inventory.json', 'r') as inventory:
                self.inventory = json.load(inventory)
        else:
            self.error = True
    def load_stats(self):
        if path.isfile(self.path + '/player_data/stats.json'):
            with open(self.path + '/player_data/stats.json', 'r') as stats:
                self.stats = json.load(stats)
        else:
            self.error = True
    def load_seed(self, root):
        if path.isfile(self.path + '/seed/seed.json'):
            with open(self.path + '/seed/seed.json', 'r') as seed:
                self.seed = json.load(seed)
        else:
            self.error = True
        #run error getting function since this is last
        self.get_error(root)
    def save_world(self, path, world_num):
        #get path to world folder
        world_name = '/world_' + world_num
        world_path = path + world_name
        #create any non existent folders
        os.makedirs(world_path + '/difficulty', exist_ok=True)
        os.makedirs(world_path + '/map_data', exist_ok=True)
        os.makedirs(world_path + '/name', exist_ok=True)
        os.makedirs(world_path + '/player_data', exist_ok=True)
        os.makedirs(world_path + '/seed', exist_ok=True)
        os.makedirs(world_path + '/generated', exist_ok=True)
        #save to folders 

        with open(world_path + '/difficulty/difficulty.json', "w") as file:
            json.dump(self.difficulty, file)
        with open(world_path + '/map_data/game_map.json', "w") as file:
            json.dump(self.game_map, file)
        with open(world_path + '/map_data/game_map_interactables.json', "w") as file:
            json.dump(self.game_map_interactables, file)
        with open(world_path + '/name/world_name.json', "w") as file:
            json.dump(self.name, file)
        with open(world_path + '/player_data/inventory.json', "w") as file:
            json.dump(self.inventory, file)
        with open(world_path + '/player_data/armour.json', "w") as file:
            json.dump(self.armour, file)
        with open(world_path + '/player_data/hotbar.json', "w") as file:
            json.dump(self.hotbar, file)
        with open(world_path + '/player_data/stats.json', "w") as file:
            json.dump(self.stats, file)
        with open(world_path + '/seed/seed.json', "w") as file:
            json.dump(self.seed, file)
            with open(world_path + '/generated/generated.json', "w") as file:
                json.dump(True, file)
    def build_workspace(self, root):
        #grass = Image.new("RGBA", (16, 16), (69, 123, 71, 255))
        #water = Image.new("RGBA", (16, 16), (94, 151, 254, 255))
        game_map_keys = self.game_map.keys()
        self.order_keys(game_map_keys)
        self.get_map_size()
        #create map image
        #self.map_image = Image.new("RGBA", (self.length, self.height), (0, 0, 0, 0))
        count = 0
        for chunk in self.sorted_keys: 
            #root.after(1 + (1 * count), lambda: self.create_map(grass, water))
            count += 1
        root.after_idle(self.notify_done, root)
    def notify_done(self, root):
        self.map_image.show()
        root.event_generate("<<Workspace_Built>>")
    def order_keys(self, game_map_keys):
        #convert the corrdinents into a numpy array
        coordinates = numpy.array([list(map(int, coord.split(':'))) for coord in game_map_keys])
        #sort the corrdinents using numpy
        sorted_coordinates = coordinates[numpy.lexsort((coordinates[:,1], coordinates[:,0]))]
        #convert strings back to keys using numpy
        sorted_keys = numpy.core.defchararray.add(sorted_coordinates[:,0].astype(str), numpy.core.defchararray.add(':', sorted_coordinates[:,1].astype(str)))
        #convert sroted keys to python list
        self.sorted_keys = sorted_keys.tolist()
    def get_map_size(self):
        #get 1st & last coord
        coord_one = self.sorted_keys[0]
        coord_two = self.sorted_keys[-1]
        #split coords on the ':'
        coord_one = coord_one.split(':')
        coord_two = coord_two.split(':')
        #convert coords to int and find length
        self.length = int(coord_two[0]) * 8 * 16 - int(coord_one[0]) * 8 * 16
        #furthest left is top left
        self.left_x = int(coord_one[0]) * 8 * 16
        #get largest y coordinent for the top
        self.top_y = max(map(lambda coord: int(coord.split(':')[1]), self.sorted_keys )) * 8 * 16
        self.bottom_y = min(map(lambda coord: int(coord.split(':')[1]), self.sorted_keys )) * 8 * 16
        self.height = self.top_y - self.bottom_y
    def create_map(self, grass, water):
        coords = self.sorted_keys[0]
        chunk = self.game_map[coords]
        #create image for the chunk
        #chunk_image = Image.new("RGBA", (8*16, 8*16), (0, 0, 0, 0))
        #get coords on whole map
        int_coords = coords.split(':')
        int_coords[0] = int(int_coords[0])
        int_coords[1] = int(int_coords[1])
        #shift the grid over so (0,0) is in the top left corner
        image_coords = [abs(self.left_x) + int_coords[0] * 8 * 16, abs(self.top_y) + int_coords[1] * 8 * 16]
        #print(coords, image_coords)
        #allow for each chunk begin 8 blocks, and images are 16x16
        #image_coords[0] = image_coords[0] * 8 * 16
        #image_coords[1] = image_coords[1] * 8 * 16
        #iterate through and add images to the map image
        x = 0 
        y = 0
        #add each tile to the hunk
        for tile in chunk:
            #1=water, 2=grass
            if tile[1] == 2:
                #chunk_image.paste(grass, (16 * x, 16 * y))
                pass
            else:
                #chunk_image.paste(water, (16 * x, 16 * y))
                pass
            if x == 7:
                x = 0
                y += 1 
            else:
                x += 1
        #add chunk to whole map
        #self.map_image.paste(chunk_image, (image_coords[0], image_coords[1]))
        #remove key currently being used
        self.sorted_keys.pop(0)