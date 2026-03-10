# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 16:42:34 2025

Convert Versions 1.0 to 1.1, 1.1 to 1.0
"""
#import libraries
import copy
#conversion classes
class Zero_To_One():
    '''Convert from version 1.0 to version 1.1'''
    def __init__(self, world):
        self.world = world
        self.new_map = copy.deepcopy(self.world.game_map)
        self.inventory = []
    def get_chunk_keys(self):
        self.chunk_keys = list(self.new_map.keys())
    def run_map_conversion(self, root):
        count = 0
        for key in self.chunk_keys:
            root.after(100 + (10 * count), lambda: self.convert_map(root))
            count += 1
    def convert_map(self, root):
        #get current key
        current_key = self.chunk_keys[0]
        #add interactables. In origional, 1=tree, 2=rock, 0=null, and so on
        #in theroy, rect position gets reset before blitting, so they don't need to be set here. This is confirmed to work.
        rock_dict = {"img_coords": [32, 0, 32, 32], "rect": [32, 0, 32, 32], "health": 15, "non_tool_drops": None, "tool_drops": [[[32, 32, 32, 32], 5]], "num_drops": 1, "chunk": "0:-1", "chunk_location": 1, "type": "stone", "tool_types": [9, 12], "class_type": "interactable"}
        tree_dict = {"img_coords": [0, 0, 32, 64], "rect": [0, 0, 32, 64], "health": 12, "non_tool_drops": [[[64, 32, 32, 32], 2]], "tool_drops": [[[64, 32, 32, 32], 2], [[64, 0, 32, 32], 1]], "num_drops": 2, "chunk": "1:-1", "chunk_location": 54, "type": "wood", "tool_types": [7, 8, 11], "class_type": "interactable"}
        log_dict = {"chunk": "-4:-16", "chunk_location": 13, "img_coords": [64, 0, 32, 32], "rect": [386, 354, 32, 32], "class_type": "collectable", "item_num": 1}
        cobblestone_dict = {"chunk": "-4:-16", "chunk_location": 13, "img_coords": [32, 32, 32, 32], "rect": [386, 354, 32, 32], "class_type": "collectable", "item_num": 5}
        stick_dict = {"chunk": "-4:-16", "chunk_location": 13, "img_coords": [64, 32, 32, 32], "rect": [386, 354, 32, 32], "class_type": "collectable", "item_num": 2}
        sugar_string_dict = {"chunk": "-4:-16", "chunk_location": 13, "img_coords": [160, 0, 32, 32], "rect": [386, 354, 32, 32], "class_type": "collectable", "item_num": 13}
        red_gelatin_dict = {"chunk": "-4:-16", "chunk_location": 13, "img_coords": [128, 0, 32, 32], "rect": [386, 354, 32, 32], "class_type": "collectable", "item_num": 21}
        green_gelatin_dict = {"chunk": "-4:-16", "chunk_location": 13, "img_coords": [96, 32, 32, 32], "rect": [386, 354, 32, 32], "class_type": "collectable", "item_num": 22}
        blue_gelatin_dict = {"chunk": "-4:-16", "chunk_location": 13, "img_coords": [96, 0, 32, 32], "rect": [386, 354, 32, 32], "class_type": "collectable", "item_num": 20}
        yellow_gelatin_dict = {"chunk": "-4:-16", "chunk_location": 13, "img_coords": [128, 32, 32, 32], "rect": [386, 354, 32, 32], "class_type": "collectable", "item_num": 23}
        count = 0
        #add correct dictonaries or none for the current interactable
        #print(len(self.world.game_map_interactables), len(self.new_map))
        for tile in self.world.game_map_interactables[current_key]:
            #error handling. it appears some chunks have more aor less tiles, this prevents an error
            if count >= 64:
                continue
            #convert interactable to proper dictionary
            if tile[1] in [1]:
                current_tree = tree_dict.copy()
                current_tree['chunk_location'] = self.world.game_map_interactables[current_key].index(tile)
                current_tree['chunk'] = current_key
                self.new_map[current_key][count].append(current_tree)
            elif tile[1] in [2]:
                current_rock = rock_dict.copy()
                current_rock['chunk_location'] = self.world.game_map_interactables[current_key].index(tile)
                current_rock['chunk'] = current_key
                self.new_map[current_key][count].append(current_rock)
            elif tile[1] in [3]:
                current_log = log_dict.copy()
                current_log['chunk_location'] = self.world.game_map_interactables[current_key].index(tile)
                current_log['chunk'] = current_key
                self.new_map[current_key][count].append(current_log)
            elif tile[1] in [4]:
                current_cobblestone = cobblestone_dict.copy()
                current_cobblestone['chunk_location'] = self.world.game_map_interactables[current_key].index(tile)
                current_cobblestone['chunk'] = current_key
                self.new_map[current_key][count].append(current_cobblestone)
            elif tile[1] in [5]:
                current_stick = stick_dict.copy()
                current_stick['chunk_location'] = self.world.game_map_interactables[current_key].index(tile)
                current_stick['chunk'] = current_key
                self.new_map[current_key][count].append(current_stick)
            elif tile[1] in [6]:
                current_sugar_string = sugar_string_dict.copy()
                current_sugar_string['chunk_location'] = self.world.game_map_interactables[current_key].index(tile)
                current_sugar_string['chunk'] = current_key
                self.new_map[current_key][count].append(current_sugar_string)
            elif tile[1] in [7]:
                current_red_gelatin = red_gelatin_dict.copy()
                current_red_gelatin['chunk_location'] = self.world.game_map_interactables[current_key].index(tile)
                current_red_gelatin['chunk'] = current_key
                self.new_map[current_key][count].append(current_red_gelatin)
            elif tile[1] in [8]:
                current_green_gelatin = green_gelatin_dict.copy()
                current_green_gelatin['chunk_location'] = self.world.game_map_interactables[current_key].index(tile)
                current_green_gelatin['chunk'] = current_key
                self.new_map[current_key][count].append(current_green_gelatin)
            elif tile[1] in [9]:
                current_blue_gelatin = blue_gelatin_dict.copy()
                current_blue_gelatin['chunk_location'] = self.world.game_map_interactables[current_key].index(tile)
                current_blue_gelatin['chunk'] = current_key
                self.new_map[current_key][count].append(current_blue_gelatin)
            elif tile[1] in [10]:
                current_yellow_gelatin = yellow_gelatin_dict.copy()
                current_yellow_gelatin['chunk_location'] = self.world.game_map_interactables[current_key].index(tile)
                current_yellow_gelatin['chunk'] = current_key
                self.new_map[current_key][count].append(current_yellow_gelatin)
            else:
                self.new_map[current_key][count].append(None)
            count += 1
        #make sure that all tiles have an interactable. See error handling above
        count = 0
        for tile in self.new_map[current_key]:
            if len(tile) == 2:
                self.new_map[current_key][count].append(None)
            count += 1
        #remvoe current chunk so it is not used again
        self.chunk_keys.pop(0)
        #sedn message that conversion is done if all keys are used
        if len(self.chunk_keys) == 0:
            root.event_generate("<<Map_Converted>>")
    def convert_main_items(self):
        #iterate through all of main inventory. Only 20 slots, should be fine
        for item in self.world.inventory:
            #check the item to find out what it is, then convert it to new ids and add it to the inventory
            new_item = self.convert_item(item[0])
            #none stays as none
            if new_item == None:
                self.inventory.append(new_item)
            else:
                self.inventory.append([new_item, item[1]])
    def convert_armour_items(self):
        #iterate through all of main inventory. Only 20 slots, should be fine
        for item in self.world.armour:
            #check the item to find out what it is, then convert it to new ids and add it to the inventory
            new_item = self.convert_item(item[0])
            #none stays as none
            if new_item == None:
                self.inventory.append(new_item)
            else:
                self.inventory.append([new_item, item[1]])
    def convert_hotbar_items(self):
        #iterate through all of main inventory. Only 20 slots, should be fine
        for item in self.world.hotbar:
            #check the item to find out what it is, then convert it to new ids and add it to the inventory
            new_item = self.convert_item(item[0])
            #none stays as none
            if new_item == None:
                self.inventory.append(new_item)
            else:
                self.inventory.append([new_item, item[1]])
    def convert_item(self, item_num):
        '''Input version 1.0 item number, outputs version 1.1 item number'''
        match item_num:
            case 0:
                return None
            case 1:
                return 1
            case 2:
                return 4
            case 3:
                return 2
            case 4:
                return 8
            case 5:
                return 11
            case 6:
                return 9
            case 7:
                return 12
            case 8:
                return 3
            case 9:
                return 5
            case 10:
                return 7
            case 11:
                return 13
            case 12:
                return 14
            case 13:
                return 19
            case 14:
                return 18
            case 15:
                return 17
            case 16:
                return 16
            case 17:
                return 21
            case 18:
                return 22
            case 19:
                return 20
            case 20:
                return 23
    def output_class(self, new_class):
        '''Output to new class'''
        return new_class.create_from_other(entities=[], difficulty=self.world.difficulty, game_map=self.new_map, name=self.world.name, inventory=self.inventory, stats=self.world.stats, seed=self.world.seed)
class One_To_Zero():
    '''Convert from version 1.1 to version 1.0'''
    def __init__(self, world):
        self.world = world
        #only deep copying one, should be all that is required
        self.new_map = copy.deepcopy(self.world.game_map)
        self.new_map_interactables = copy.deepcopy(self.world.game_map)
    def get_chunk_keys(self):
        self.chunk_keys = list(self.new_map.keys())
    def run_map_conversion(self, root):
        count = 0
        for key in self.chunk_keys:
            root.after(100 + (10 * count), lambda: self.convert_map(root))
            count += 1
    def convert_map(self, root):
        #get current key
        current_key = self.chunk_keys[0]
        count = 0
        for tile in self.world.game_map[current_key]:
            #error handling. it appears some chunks have more aor less tiles, this prevents an error
            if count >= 64:
                continue
            #remove current interactable from lists
            self.new_map[current_key][count].pop()
            self.new_map_interactables[current_key][count].pop()
            #convert interactable to 1.0 lists
            if tile[2] != None:
                #check if it is interactable of collectable
                if tile[2]['class_type'] == 'interactable':
                    #check tree or rock
                    if tile[2]['type'] == 'wood':
                        #remove old interactable
                        self.new_map_interactables[current_key][count].pop()
                        #add interactable to game map interactables
                        self.new_map_interactables[current_key][count].append(1)
                        self.new_map_interactables[current_key][count].append(12)
                    elif tile[2]['type'] == 'stone':
                        #remove old interactable
                        self.new_map_interactables[current_key][count].pop()
                        #add interactable to game map interactables
                        self.new_map_interactables[current_key][count].append(2)
                        self.new_map_interactables[current_key][count].append(12)
                elif tile[2]['class_type'] == 'collectable':
                    #log
                    if tile[2]['item_num'] == 1:
                        #remove old interactable
                        self.new_map_interactables[current_key][count].pop()
                        #add interactable to game map interactables
                        self.new_map_interactables[current_key][count].append(3)
                        self.new_map_interactables[current_key][count].append(12)
                    #cobblestone
                    elif tile[2]['item_num'] == 5:
                        #remove old interactable
                        self.new_map_interactables[current_key][count].pop()
                        #add interactable to game map interactables
                        self.new_map_interactables[current_key][count].append(4)
                        self.new_map_interactables[current_key][count].append(12)
                    #stick
                    elif tile[2]['item_num'] == 2:
                        #remove old interactable
                        self.new_map_interactables[current_key][count].pop()
                        #add interactable to game map interactables
                        self.new_map_interactables[current_key][count].append(5)
                        self.new_map_interactables[current_key][count].append(12)
                    #sugar string
                    elif tile[2]['item_num'] == 13:
                        #remove old interactable
                        self.new_map_interactables[current_key][count].pop()
                        #add interactable to game map interactables
                        self.new_map_interactables[current_key][count].append(6)
                        self.new_map_interactables[current_key][count].append(12)
                    #red gelatin
                    elif tile[2]['item_num'] == 21:
                        #remove old interactable
                        self.new_map_interactables[current_key][count].pop()
                        #add interactable to game map interactables
                        self.new_map_interactables[current_key][count].append(7)
                        self.new_map_interactables[current_key][count].append(12)
                    #green gelatin
                    elif tile[2]['item_num'] == 22:
                        #remove old interactable
                        self.new_map_interactables[current_key][count].pop()
                        #add interactable to game map interactables
                        self.new_map_interactables[current_key][count].append(8)
                        self.new_map_interactables[current_key][count].append(12)
                    #blue gelatin
                    elif tile[2]['item_num'] == 20:
                        #remove old interactable
                        self.new_map_interactables[current_key][count].pop()
                        #add interactable to game map interactables
                        self.new_map_interactables[current_key][count].append(9)
                        self.new_map_interactables[current_key][count].append(12)
                    #yellow gelatin
                    elif tile[2]['item_num'] == 23:
                        #remove old interactable
                        self.new_map_interactables[current_key][count].pop()
                        #add interactable to game map interactables
                        self.new_map_interactables[current_key][count].append(10)
                        self.new_map_interactables[current_key][count].append(12)
                    #just in case something wierd happens
                    else:
                        #remove old interactable
                        self.new_map_interactables[current_key][count].pop()
                        #add interactable to game map interactables
                        self.new_map_interactables[current_key][count].append(0)
                        self.new_map_interactables[current_key][count].append(12)
            else:
                #remove old interactable
                self.new_map_interactables[current_key][count].pop()
                #add interactable to game map interactables
                self.new_map_interactables[current_key][count].append(0)
                self.new_map_interactables[current_key][count].append(12)
            count += 1
        #remove current chunk so it is not used again
        self.chunk_keys.pop(0)
        #sedn message that conversion is done if all keys are used
        if len(self.chunk_keys) == 0:
            root.event_generate("<<Map_Converted>>")
    def convert_main_items(self):
        #set up 3 inventorys
        self.main_inventory = []
        self.hotbar = []
        self.armour = []
        #iterate through all of inventory. shouldn't take too long
        count  = 0
        for item in self.world.inventory:
            if count <= 19:
                if item == None:
                    self.main_inventory.append([0, 0])
                else:
                    self.main_inventory.append([self.convert_item(item[0]), item[1]])
            elif count <= 24:
                if item == None:
                    self.hotbar.append([0, 0])
                else:
                    self.hotbar.append([self.convert_item(item[0]), item[1]])
            elif count <= 28:
                if item == None:
                    self.armour.append([0, 0])
                else:
                    self.armour.append([self.convert_item(item[0]), item[1]])
            count += 1
    def convert_item(self, item_num):
        '''Input version 1.0 item number, outputs version 1.1 item number'''
        item_num = int(item_num)
        match item_num:
            case 0:
                return 0
            case 1:
                return 1
            case 4:
                return 2
            case 2:
                return 3
            case 8:
                return 4
            case 11:
                return 4
            case 9:
                return 6
            case 12:
                return 7
            case 3:
                return 8
            case 5:
                return 9
            case 7:
                return 10
            case 13:
                return 11
            case 14:
                return 12
            case 19:
                return 13
            case 18:
                return 14
            case 17:
                return 15
            case 16:
                return 16
            case 21:
                return 17
            case 22:
                return 18
            case 20:
                return 19
            case 23:
                return 20
            case _:
                return 0
    def output_class(self, new_class):
        '''Output to new class'''
        return new_class.create_from_other(difficulty=self.world.difficulty, game_map=self.new_map, game_map_interactables=self.new_map_interactables, name=self.world.name, main_inventory=self.main_inventory, hotbar=self.hotbar, armour=self.armour, stats=self.world.stats, seed=self.world.seed)