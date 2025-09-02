# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 16:11:28 2025

"""

import json
import os
from os import path
class Version_1_1():
    '''Class for version 1.1 worlds'''
    def __init__(self, folder_path):
        self.path = folder_path
        self.version = '1.1'
        self.error = False
    @classmethod
    def create_from_other(cls, **kwargs):
        obj = cls.__new__(cls)
        obj.entities = kwargs['entities']
        obj.difficulty = kwargs['difficulty']
        obj.game_map = kwargs['game_map']
        obj.name = kwargs['name']
        obj.inventory = kwargs['inventory']
        obj.stats = kwargs['stats']
        obj.seed = kwargs['seed'] 
        obj.version = '1.1'
        return obj
    def load_files(self, root):
        #load in all files, with calls to refresh screen between them
        root.after(1, lambda: self.load_entities())
        root.after(110, lambda: self.load_difficulty())
        root.after(120, lambda: self.load_map())
        root.after(130, lambda: self.load_name())
        root.after(140, lambda: self.load_items())
        root.after(150, lambda: self.load_stats())
        root.after(150, lambda: self.load_seed(root))
    def get_error(self, root):
        if self.error:
            root.event_generate("<<Error_Loading_World>>")
        else:
            root.event_generate("<<World_Loaded>>")
    def load_entities(self):
        if path.isfile(self.path + '/entities/entity_data.json'):
            with open(self.path + '/entities/entity_data.json', 'r') as entities:
                self.entities = json.load(entities)
        else:
            self.error = True
    def load_difficulty(self):
        if path.isfile(self.path + '/difficulty/difficulty.json'):
            with open(self.path + '/difficulty/difficulty.json', 'r') as difficulty:
                self.difficulty = json.load(difficulty)
        else:
            self.error = True
    def load_map(self):
        if path.isfile(self.path + '/map_data/game_map.json'):
            with open(self.path + '/map_data/game_map.json', 'r') as game_map:
                self.game_map = json.load(game_map)
        else:
            self.error = True
    def load_name(self):
        if path.isfile(self.path + '/name/world_name.json'):
            with open(self.path + '/name/world_name.json', 'r') as name:
                self.name = json.load(name)
        else:
            self.error = True
    def load_items(self):
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
        os.makedirs(world_path + '/entities', exist_ok=True)
        os.makedirs(world_path + '/difficulty', exist_ok=True)
        os.makedirs(world_path + '/map_data', exist_ok=True)
        os.makedirs(world_path + '/name', exist_ok=True)
        os.makedirs(world_path + '/player_data', exist_ok=True)
        os.makedirs(world_path + '/seed', exist_ok=True)
        os.makedirs(world_path + '/generated', exist_ok=True)
        #save to folders 
        with open(world_path + '/entities/entity_data.json', "w") as file:
            json.dump(self.entities, file)
        with open(world_path + '/difficulty/difficulty.json', "w") as file:
            json.dump(self.difficulty, file)
        with open(world_path + '/map_data/game_map.json', "w") as file:
            json.dump(self.game_map, file)
        with open(world_path + '/name/world_name.json', "w") as file:
            json.dump(self.name, file)
        with open(world_path + '/player_data/inventory.json', "w") as file:
            json.dump(self.inventory, file)
        with open(world_path + '/player_data/stats.json', "w") as file:
            json.dump(self.stats, file)
        with open(world_path + '/seed/seed.json', "w") as file:
            json.dump(self.seed, file)
            with open(world_path + '/generated/generated.json', "w") as file:
                json.dump(True, file)