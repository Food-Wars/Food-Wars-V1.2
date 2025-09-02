# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 19:10:23 2025

"""

# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 08:12:39 2024

@author: zrobi
"""

#import defult libraries
import os
from os import path
import random
import json
import copy
import colorsys
import re
import time
#import 3rd party libraries
#using pygame-ce
import pygame as pygame 
from pygame import mixer
import pygame.freetype
import opensimplex
import pyperclip
from PIL import Image, ImageDraw, ImageFont
import numpy
#import files
import game_engines
#initalise modules
pygame.init()
#initalise mixer
pygame.mixer.pre_init(48000, -16, 2, 4096)
mixer.init()
pygame.mixer.set_num_channels(20)
#create specified channels
entity_1 = pygame.mixer.Channel(0)
entity_2 = pygame.mixer.Channel(1)
entity_3 = pygame.mixer.Channel(2)
entity_4 = pygame.mixer.Channel(3)
player_main_step = pygame.mixer.Channel(4)
player_enhance_step = pygame.mixer.Channel(5)
#reserve specific channels
pygame.mixer.set_reserved(6)
#game variables
tile_size = 16
fps = 30
chunk_size = 8
creation_difficulty = 0
settings_difficulty = 0
save_timer = 0
ingame_settings_state = 1
entities_dict = []
projectiles = []
devtools_keybinds = False
chunk_borders_debug = True

#define screen
screen_height = 600
screen_width = 600
screen = pygame.display.set_mode((screen_width, screen_height))
#create surface for interactables
interactable_surface = pygame.Surface((screen_height, screen_width))
interactable_surface = interactable_surface.convert_alpha()

#load attribution for files
#load images tiles


#load button textures

#load music
#player_walk_sfx = pygame.mixer.Sound('imgs/coin.wav')
'''
pygame.mixer.music.set_endevent ( pygame.USEREVENT ) 
playlist = ['game_files/music/Leaving.wav']
pygame.mixer.music.load(random.choice(playlist))
    '''
def load_audio(path):
    return pygame.mixer.Sound(path)
#load sfx
entity_sfx = {}
entity_sfx['gelatin'] = []
for num in range(1, 6):
    sound = load_audio(f'game_files/sfx/Gelatin/splat_{num}.wav')
    entity_sfx['gelatin'].append(sound)
break_block = {}
break_block['wood'] = []
for num in range(1, 10):
    sound = load_audio(f'game_files/sfx/Player/use_item/wood_chop_{num}.wav')
    break_block['wood'].append(sound)
break_block['stone'] = []
for num in range(1, 8):
    sound = load_audio(f'game_files/sfx/Player/use_item/rock_{num}.wav')
    break_block['stone'].append(sound)
#screen details
pygame.display.set_caption('Food Wars')
pygame.display.set_icon(icon_img)
clock = pygame.time.Clock()


#create dictionaries
game_map = {}
#world data dictionaraies
world_generated = {}
world_names = {}
world_difficulties = {}
world_seeds = {}
#load crafting recipie file
if path.exists('game_files/crafting/crafting_recepies.json'):
    with open('game_files/crafting/crafting_recepies.json', 'r') as recepies:
        crafting_recepies = json.load(recepies)
#load  file with item attributes
if path.exists('game_files/item_data/item_data.json'):
    with open('game_files/item_data/item_data.json', 'r') as data:
        item_data = json.load(data)
#load files to check if each world has been generated
if path.exists('game_files/world_data/world_1/generated/generated.json'):
    with open('game_files/world_data/world_1/generated/generated.json', 'r') as one_gen:
        world_one_generated = json.load(one_gen)
        world_generated[1] = world_one_generated
if path.exists('game_files/world_data/world_2/generated/generated.json'):
    with open('game_files/world_data/world_2/generated/generated.json', 'r') as two_gen:
        world_two_generated = json.load(two_gen)
        world_generated[2] = world_two_generated
if path.exists('game_files/world_data/world_3/generated/generated.json'):
    with open('game_files/world_data/world_3/generated/generated.json', 'r') as three_gen:
        world_three_generated = json.load(three_gen)
        world_generated[3] = world_three_generated
if path.exists('game_files/world_data/world_4/generated/generated.json'):
    with open('game_files/world_data/world_4/generated/generated.json', 'r') as four_gen:
        world_four_generated = json.load(four_gen)
        world_generated[4] = world_four_generated
#load the name of each world
if path.exists('game_files/world_data/world_1/name/world_name.json'):
    with open('game_files/world_data/world_1/name/world_name.json', 'r') as one_name:
        world_one_name = json.load(one_name)
        world_names[1] = world_one_name
if path.exists('game_files/world_data/world_2/name/world_name.json'):
    with open('game_files/world_data/world_2/name/world_name.json', 'r') as two_name:
        world_two_name = json.load(two_name)
        world_names[2] = world_two_name
if path.exists('game_files/world_data/world_3/name/world_name.json'):
    with open('game_files/world_data/world_3/name/world_name.json', 'r') as three_name:
        world_three_name = json.load(three_name)
        world_names[3] = world_three_name
if path.exists('game_files/world_data/world_4/name/world_name.json'):
    with open('game_files/world_data/world_4/name/world_name.json', 'r') as four_name:
        world_four_name = json.load(four_name)
        world_names[4] = world_four_name
#load difficulty of each world
if path.exists('game_files/world_data/world_1/difficulty/difficulty.json'):
    with open('game_files/world_data/world_1/difficulty/difficulty.json', 'r') as one_difficulty:
        world_one_diffuclty = json.load(one_difficulty)
        world_difficulties[1] = world_one_diffuclty
if path.exists('game_files/world_data/world_2/difficulty/difficulty.json'):
    with open('game_files/world_data/world_2/difficulty/difficulty.json', 'r') as two_difficulty:
        world_two_diffuclty = json.load(two_difficulty)
        world_difficulties[2] = world_two_diffuclty
if path.exists('game_files/world_data/world_3/difficulty/difficulty.json'):
    with open('game_files/world_data/world_3/difficulty/difficulty.json', 'r') as three_difficulty:
        world_three_diffuclty = json.load(three_difficulty)
        world_difficulties[3] = world_three_diffuclty
if path.exists('game_files/world_data/world_4/difficulty/difficulty.json'):
    with open('game_files/world_data/world_4/difficulty/difficulty.json', 'r') as four_difficulty:
        world_four_diffuclty = json.load(four_difficulty)
        world_difficulties[4] = world_four_diffuclty
#load seed of each world
if path.exists('game_files/world_data/world_1/seed/seed.json'):
    with open('game_files/world_data/world_1/seed/seed.json', 'r') as one_seed:
        world_one_seed = json.load(one_seed)
        world_seeds[1] = world_one_seed
if path.exists('game_files/world_data/world_2/seed/seed.json'):
    with open('game_files/world_data/world_2/seed/seed.json', 'r') as two_seed:
        world_two_seed = json.load(two_seed)
        world_seeds[2] = world_two_seed
if path.exists('game_files/world_data/world_3/seed/seed.json'):
    with open('game_files/world_data/world_3/seed/seed.json', 'r') as three_seed:
        world_three_seed = json.load(three_seed)
        world_seeds[3] = world_three_seed
if path.exists('game_files/world_data/world_4/seed/seed.json'):
    with open('game_files/world_data/world_4/seed/seed.json', 'r') as four_seed:
        world_four_seed = json.load(four_seed)
        world_seeds[4] = world_four_seed

#load credit TXTs
if path.exists('game_files/fonts/medieval-sharp-font/info.txt'):
    with open('game_files/fonts/medieval-sharp-font/info.txt', 'r') as credits_loaded:
        credits_txt = credits_loaded.read()
#colours
white = (255, 255, 255)
colour_inactive = (43, 45, 70)
colour_active = (75, 77, 108)
settings_bg_colour = (198, 198, 198)
settings_bg_colour_active = (190, 190, 190)

#define fonts 
font =  pygame.font.Font('game_files/fonts/medieval-sharp-font/MedievalSharp-xOZ5.ttf', 24)
font_inventory =  pygame.font.Font('game_files/fonts/medieval-sharp-font/MedievalSharp-xOZ5.ttf', 15)
font_difficulty =  pygame.font.Font('game_files/fonts/medieval-sharp-font/MedievalSharp-xOZ5.ttf', 19)
settings_font =  pygame.freetype.Font('game_files/fonts/medieval-sharp-font/MedievalSharp-xOZ5.ttf', 24)
attribution_font = ImageFont.truetype("game_files/fonts/DM_Serif_Text/DMSerifText-Regular.ttf", 12)
#load/define settings
scroll_sensitivity = 1
#set up music
'''
if music == True:
    pygame.mixer.music.play() 
else:
    pygame.mixer.music.pause()'''
#pygame.mixer.music.play() 
#functions
def handle_music(playlist, event, music):
    '''
    if music == True:
        pygame.mixer.music.unpause()
        if event == pygame.USEREVENT:
            music_load = random.choice(playlist)
            pygame.mixer.music.load(music_load) 
            pygame.mixer.music.play() 
    else:
        pygame.mixer.music.pause()
        '''
#pygame.mixer.music.load('game_files/music/[Insert_Title_Here].wav') 
#pygame.mixer.music.play(loops=-1) 
music = False
#saves settigns to a file. Much more DRY
def save_settings():
    settings = [sfx, music, scroll_sense.ratio, coords_on, select_charachter.current_player]
    with open('game_files/settings/settings.json', "w") as file:
        json.dump(settings, file)
    set_keybinds.save_keybinds()
#generate background map
def generate_chunks(x, y, seed):
    chunk_data = []
    #set up noise generator
    opensimplex.seed(seed)
    #iterate through each tile in the chunk
    for y_pos in range(chunk_size):
        for x_pos in range(chunk_size):
            #find x and y locations
            target_x = x * chunk_size + x_pos
            target_y = y * chunk_size + y_pos
            #defult tile is nothing
            tile_type = 0
            #get "height" from noise generator
            height = opensimplex.noise2(target_x / 30, target_y / 30)
            #use height to determine tile type
            #2 = water
            #1 = grass
            if height <= -0.3:
                tile_type = 2
                #set interactabl;e item to zero because tile is water
                interectable_tile = None
            elif height > -0.3:
                tile_type = 1
                #get interactable tile based on noise patter
                interactable_height = opensimplex.noise2(target_x , target_y)
                if interactable_height < -0.78:
                    interectable_tile = Interactable('wood', (0, 0, 32, 64), (10, 15), [[(64, 32, 32, 32), 2]], [[(64, 0, 32, 32), 1], [(64, 32, 32, 32), 2]], 2, x, y, len(chunk_data))
                elif interactable_height > 0.78:
                    interectable_tile = Interactable('stone', (32, 0, 32, 32), (12, 15), None, [[(32, 32, 32, 32), 5]], 1, x, y, len(chunk_data))
                else: 
                    interectable_tile = None
            if tile_type != 0:
                #if the tile is not nothing, add it to the chunk data
                chunk_data.append([(target_x, target_y), tile_type, interectable_tile])
    return chunk_data

#function to draw text to the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
def draw_text_freetype(text, font, font_size, text_colour, x, y):
    font.render_to(screen, (x, y), text, size=font_size, fgcolor=text_colour)
def string_to_float(string):
    '''Convert string to useable number if it contains non-number charachters'''
    #split string at all number/not number charachters
    output_list = re.findall(r'\d+|\D+', string)
    new_string = '0'
    total = 0
    #iterate through all sections of the output list
    for split_string in output_list:
        #if the string is 0-9 or ., just add it to the output string
        if split_string.isdigit():
            new_string = new_string + split_string
        elif split_string == '.':
            new_string = new_string + split_string
        else:
            #if the output string is anything else, go through it charachter by charachter
            for char in split_string:
                #add unicode number value of the charachter to the current total
                total += ord(char)
    #convert the string of number to a float and add the total
    output_float = float(new_string) + total
    return output_float
class Collectable():
    def __init__(self, img_coords, chunk, chunk_pos, item_num):
        self.chunk = chunk
        self.chunk_location = chunk_pos
        self.img_coords = img_coords
        self.rect = pygame.rect.Rect(img_coords[0], img_coords[1], img_coords[2], img_coords[3])
        self.class_type = 'collectable'
        self.item_num = item_num 
    @classmethod
    def load_from_file(cls, attributes):
        #create new object of this class
        obj = cls.__new__(cls)
        #load variables from attributes
        obj.chunk = attributes['chunk']
        obj.chunk_location = attributes['chunk_location']
        obj.img_coords = attributes['img_coords']
        obj.rect = pygame.rect.Rect(attributes['rect'][0], attributes['rect'][1], attributes['rect'][2], attributes['rect'][3])
        obj.item_num = attributes['item_num']
        obj.class_type = 'collectable'
        return obj
    def save_to_file(self):
        #create dict of all variables in self
        self_dict = vars(self)
        #change rect because it cannot be saved
        self_dict['rect'] = [self.rect.x, self.rect.y, self.rect.width, self.rect.height]
        return self_dict
    def collect(self):
        game_map_interactables[self.chunk][self.chunk_pos][2] = None
    def damage(self, *args):
        #this exists to make it easier to have collectable and itneracatble classes
        return
class Interactable():
    #tool and non tool drops are the image corrdinants to send to the collectable
    def __init__(self, interactable_type, img_coords, health_range, non_tool_drops, tool_drops, num_drops, x, y, chunk_location):
        self.img_coords = img_coords
        self.rect = pygame.rect.Rect(img_coords[0], img_coords[1], img_coords[2], img_coords[3])
        self.health = random.randint(health_range[0], health_range[1])
        self.non_tool_drops = non_tool_drops
        self.tool_drops = tool_drops
        self.num_drops = num_drops
        self.chunk = str(x) + ':' + str(y)
        self.chunk_location = chunk_location
        self.type = interactable_type
        match self.type:
            case 'wood':
                self.tool_types = (7, 8, 11)
            case 'stone':
                self.tool_types = (9, 12)
            case _:
                self.tool_types = ()
    @classmethod
    def load_from_file(cls, attributes):
        #create new object of this class
        obj = cls.__new__(cls)
        #create class variables from attributes
        obj.img_coords = attributes['img_coords']
        obj.rect = pygame.rect.Rect(attributes['rect'][0], attributes['rect'][1], attributes['rect'][2], attributes['rect'][3])
        obj.health = attributes['health']
        obj.non_tool_drops = attributes['non_tool_drops']
        obj.tool_drops = attributes['tool_drops']
        obj.num_drops = attributes['num_drops']
        obj.chunk = attributes['chunk']
        obj.chunk_location = attributes['chunk_location']
        obj.type = attributes['type']
        obj.tool_types = attributes['tool_types']
        return obj
    def save_to_file(self):
        #convert all self variables to string
        self_dict = vars(self)
        #change rect because it cannot be saved to json file
        self_dict['class_type'] = 'interactable'
        self_dict['rect'] = [self.rect.x, self.rect.y, self.rect.width, self.rect.height]
        return self_dict
    def damage(self, amount, damage_addition):
        #play damage sound
        sound = random.choice(break_block[self.type])
        sound.play()
        #check what item is in the player's hand
        if hotbar.hotbar_slots[f'slot_{hotbar.selector_slot + 1}'][0] != None:
            #item num is a string when stroed  in item class as json stores it as a string
            item_num = int(hotbar.hotbar_slots[f'slot_{hotbar.selector_slot + 1}'][3])
        else:
            item_num = None
        if item_num in self.tool_types:
            damage_amount = amount + damage_addition
        else:
            damage_amount = amount
        self.health -= damage_amount
        if self.health <= 0:
            self.destroy()
    def destroy(self):
        #check what item is in the player's hand
        if hotbar.hotbar_slots[f'slot_{hotbar.selector_slot + 1}'][0] != None:
            #item num is a string when stroed  in item class as json stores it as a string
            item_num = int(hotbar.hotbar_slots[f'slot_{hotbar.selector_slot + 1}'][3])
        else:
            item_num = None
        #drops are done differently if the interactable has two drops
        if self.num_drops == 2:
            #check if using correct tool
            if item_num in self.tool_types:
                dropped_item_1 = self.tool_drops[0]
                dropped_item_2 = random.choice(self.tool_drops)
            else:
                if self.non_tool_drops == None:
                    dropped_item_1 = None
                    dropped_item_2 = None
                else:
                    dropped_item_1 = random.choice(self.non_tool_drops)
                    dropped_item_2 = random.choice(self.non_tool_drops)

            #check if interactable is on the top of the chunk
            if self.chunk_location > 7:
                #place dropped item on same tile
                game_map[self.chunk][self.chunk_location][2] = Collectable(dropped_item_1[0], self.chunk, self.chunk_location, dropped_item_1[1])
                #place dropped item 1 tile above
                chunk_pos = self.chunk_location - (chunk_size * 2)
                game_map[self.chunk][chunk_pos][2] = Collectable(dropped_item_2[0], self.chunk, chunk_pos, dropped_item_2[1])
            else:
                #place dropped item on same tile
                game_map[self.chunk][self.chunk_location][2] = Collectable(dropped_item_1[0], self.chunk, self.chunk_location, dropped_item_1[1])
                #place dropped item 1 tile above in above chunk
                chunk_coords = self.chunk.split(':')
                above_chunk_num = chunk_coords[0] + ':' + str(int(chunk_coords[1]) - 1)
                chunk_pos = 63 - (14 - self.chunk_location)
                game_map[above_chunk_num][chunk_pos][2] = Collectable(dropped_item_2[0], above_chunk_num, chunk_pos, dropped_item_2[1])
        else:
            #check if using correct tool
            if item_num in self.tool_types:
                dropped_item = random.choice(self.tool_drops)
                game_map[self.chunk][self.chunk_location][2] = Collectable(dropped_item[0], self.chunk, self.chunk_location, dropped_item[1])
            else:
                if self.non_tool_drops == None:
                    game_map[self.chunk][self.chunk_location][2] = None
                else:
                    dropped_item = random.choice(self.non_tool_drops)
                    game_map[self.chunk][self.chunk_location][2] = Collectable(dropped_item[0], self.chunk, self.chunk_location, dropped_item[1])

#world functions
def generate_world(world_num, world_name, seed, difficulty):
    with open(f'game_files/world_data/world_{world_num}/generated/generated.json', "w") as file:
        json.dump(True, file)
    with open(f'game_files/world_data/world_{world_num}/name/world_name.json', "w") as file:
        json.dump(world_name, file)
    with open(f'game_files/world_data/world_{world_num}/seed/seed.json', "w") as file:
        json.dump(seed, file)
    with open(f'game_files/world_data/world_{world_num}/difficulty/difficulty.json', "w") as file:
        json.dump(difficulty, file)
    world_names[world_num] = world_name
    world_generated[world_num] = True
def save_world(world_num, game_map, inventory, health, scroll, player_x, player_y, player_direction, entities):
    #mak a copy of game map to not alter game when making modifications to save
    map_to_save = copy.deepcopy(game_map)
    temp_inventory = []
    for slot in inventory.values():
        if slot['item_data'] == None:
            temp_inventory.append(slot['item_data'])
        else:
            temp_inventory.append(slot['item_data'].save_to_file())
    #iterate thorugh map to chang chunks
    for chunk in map_to_save:
        for tile in map_to_save[chunk]:
            #if there is a intectable or collectable class, run the save command to convert it
            if tile[2] != None:
                new_tile = tile[2].save_to_file()
                map_to_save[chunk][tile[2].chunk_location][2] = new_tile

    #convert entities to a form that can be saved
    entities_to_save = []
    for entity in entities.values():
        entities_to_save.append(entity.save_to_file())
    #convert individual player stats to list
    stats = [health, scroll, [player_x, player_y], player_direction]
    #save to files
    with open(f'game_files/world_data/world_{world_num}/map_data/game_map.json', "w") as file:
        json.dump(map_to_save, file)
    with open(f'game_files/world_data/world_{world_num}/player_data/inventory.json', "w") as file:
        json.dump(temp_inventory, file)
    with open(f'game_files/world_data/world_{world_num}/player_data/stats.json', "w") as file:
        json.dump(stats, file)
    with open(f'game_files/world_data/world_{world_num}/entities/entity_data.json', "w") as file:
        json.dump(entities_to_save, file)
def load_world(world_num):
    if path.exists(f'game_files/world_data/world_{world_num}/map_data/game_map.json'):
        with open(f'game_files/world_data/world_{world_num}/map_data/game_map.json', 'r') as world_map:
            global game_map
            loaded_map = json.load(world_map)
            #iterate through map
            for chunk in loaded_map:
                for tile in loaded_map[chunk]:
                    #print(tile)
                    #save any non None interactables as class
                    if tile[2] != None:
                        if tile[2]['class_type'] =='interactable':
                            loaded_map[chunk][tile[2]['chunk_location']][2] = Interactable.load_from_file(tile[2])
                        elif tile[2]['class_type'] =='collectable':
                            loaded_map[chunk][tile[2]['chunk_location']][2] = Collectable.load_from_file(tile[2])
                        else:
                            loaded_map[chunk][tile[2]['chunk_location']][2] = None
            game_map = loaded_map
    if path.exists(f'game_files/world_data/world_{world_num}/seed/seed.json'):
        with open(f'game_files/world_data/world_{world_num}/seed/seed.json', 'r') as loaded_seed:
            global world_seed
            world_seed = int(json.load(loaded_seed))
    if path.exists(f'game_files/world_data/world_{world_num}/player_data/inventory.json'):
        with open(f'game_files/world_data/world_{world_num}/player_data/inventory.json', 'r') as loaded_inventory:
            inventory_data = json.load(loaded_inventory)
            slot_num = 0
            for slot in inventory.slots:
                #needed for converted worlds to not error
                if slot_num < len(inventory_data):
                    if inventory_data[slot_num] == None:
                        inventory.slots[slot]['item_data'] = inventory_data[slot_num]
                    else:
                        inventory.slots[slot]['item_data'] = Item.load_from_file(inventory_data[slot_num])
                slot_num += 1
    if path.exists(f'game_files/world_data/world_{world_num}/player_data/stats.json'):
        with open(f'game_files/world_data/world_{world_num}/player_data/stats.json', 'r') as statistics:
            stats = json.load(statistics)
            player.hearts['health_count'] = stats[0]
            global true_scroll
            true_scroll = stats[1]
            player.rect.x = stats[2][0]
            player.rect.y = stats[2][1]
            player.direction = stats[3]
    #load entities
    if path.exists(f'game_files/world_data/world_{world_num}/entities/entity_data.json'):
        with open(f'game_files/world_data/world_{world_num}/entities/entity_data.json', 'r') as entities:
            entity_data = json.load(entities)
            entity_loaded = False
            for entity in entity_data:
                if entity['class_type'] == 'cotten_candy':
                    new_entity = game_engines.enitites.Cotten_Candy.load_from_file(entity)
                    entity_loaded = True
                elif entity['class_type'] == 'gelatin':
                    new_entity = game_engines.enitites.Gelatin.load_from_file(entity)
                    entity_loaded = True
                #error hadnlign after bg where it didn't make a new entity
                if entity_loaded == True:
                    game_engines.enitites.entitie_dict[new_entity.entity_num] = new_entity
                    entity_loaded = False
    #load inventory to hotbar
    hotbar.get_slot_data()
def debug_menu_show(target_chunk):
    #shows coords no matter what if debug is on
    if coords_on == False:
        draw_text(str(scroll), font, white, 10, 10)
    #show what chunk you are in
    draw_text('Target Chunk: ' + target_chunk, font, white, 10, 40)
def get_license_text(library_name):
    '''blits license info to screen, works with scrollbar'''
    #get license text
    license_text = game_engines.library_lisences.licenses[library_name]
    #create  temp image uisng PIL
    temp_image = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
    draw = ImageDraw.Draw(temp_image)
    #get required image height 
    text_size = draw.textbbox((0, 0), license_text, font=attribution_font)
    height = text_size[3] - text_size[1]
    #create new image & draw the text onto it
    image = Image.new('RGBA', (500, height), (255, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.multiline_text((10, 10), license_text, font=attribution_font, fill=(0, 0, 0)) 
    bytes_image = image.tobytes()
    pygame_image = pygame.image.frombytes(bytes_image, image.size, image.mode)
    return pygame_image
def draw_license_text(image, scroll):
    image_height = image.get_height()
    screen.blit(image, (70, 60), (0, image_height - (image_height - scroll), 500, 500))
#entity classes
class Player():
    def __init__(self, x, y):
        self.reset(x, y)
    def reset(self, x, y):
        self.dead = False
        self.counter = 0
        self.index = 0
        self.direction = 2
        self.regen_counter = 0
        self.rect = pygame.rect.Rect(0, 0, 32, 64)
        self.hitbox = self.rect.copy()
        self.rect.x = x
        self.rect.y = y
        self.width = self.rect.width
        self.height = self.rect.height
        #armour stuff
        self.armour_full = pygame.image.load('game_files/imgs/gui/armour_full.png')
        self.armour_half = pygame.image.load('game_files/imgs/gui/armour_half.png')
        self.armour_empty = pygame.image.load('game_files/imgs/gui/armour_empty.png')
        self.armour_bg = pygame.image.load('game_files/imgs/gui/armour_bg.png')
        self.armour_points = {
                    'armour_count': 0,
                    'armour_1': self.armour_empty,
                    'armour_2': self.armour_empty,
                    'armour_3': self.armour_empty,
                    'armour_4': self.armour_empty,
                    'armour_5': self.armour_empty,
                    'armour_6': self.armour_empty,
                    'armour_7': self.armour_empty,
                    'armour_8': self.armour_empty,
                    'armour_9': self.armour_empty,
                    'armour_10': self.armour_empty,
                    }
        helmet_img = pygame.image.load('game_files/imgs/armour/suger_cloth_helmet.png')
        self.helmet_img = pygame.transform.scale(helmet_img, (helmet_img.get_width() * 2, helmet_img.get_height() * 2))
        tunic_img = pygame.image.load('game_files/imgs/armour/suger_cloth_chestplate.png')
        self.tunic_img = pygame.transform.scale(tunic_img, (tunic_img.get_width() * 2, tunic_img.get_height() * 2))
        leggings_img = pygame.image.load('game_files/imgs/armour/sugar_cloth_leggings.png')
        self.leggings_img = pygame.transform.scale(leggings_img, (leggings_img.get_width() * 2, leggings_img.get_height() * 2))
        boots_img = pygame.image.load('game_files/imgs/armour/sugar_cloth_boots.png')
        self.boots_img = pygame.transform.scale(boots_img, (boots_img.get_width() * 2, boots_img.get_height() * 2))
        #health stuff
        self.heart_full = pygame.image.load('game_files/imgs/gui/heart_full.png')
        self.heart_half = pygame.image.load('game_files/imgs/gui/heart_half.png')
        self.heart_empty = pygame.image.load('game_files/imgs/gui/heart_empty.png')
        self.heart_bg= pygame.image.load('game_files/imgs/gui/heart_bg.png')
        self.hearts = {
                    'health_count': 20,
                    'heart_1': self.heart_full,
                    'heart_2': self.heart_full,
                    'heart_3': self.heart_full,
                    'heart_4': self.heart_full,
                    'heart_5': self.heart_full,
                    'heart_6': self.heart_full,
                    'heart_7': self.heart_full,
                    'heart_8': self.heart_full,
                    'heart_9': self.heart_full,
                    'heart_10': self.heart_full,
                    }
        self.speed = 0
        self.run = False
        walk_icon = pygame.image.load('game_files/imgs/gui/walk_icon.png')
        self.walk_icon = pygame.transform.scale(walk_icon, (tile_size * 2, tile_size * 2))
        run_icon = pygame.image.load('game_files/imgs/gui/run_icon.png')
        self.run_icon = pygame.transform.scale(run_icon, (tile_size * 2, tile_size * 2))
        self.run_cooldown = 2
        self.selected_item = hotbar.selected_item
        self.item = 0
        self.chopping = False
        self.chop_timer = 0
        self.broken = False
        self.in_water = False
        self.submerged = False
        self.speed_modifier = 1.5
        self.event = 'this is a required variable that will get replaced by usseful stuff later'
        self.hors_frame = 0
        self.vert_frame = 0
        self.player_walk_frames = [0, 1, 0, 2]
        #load sounds
        self.heartbeats = []
        for num in range(1,5):
            sfx = load_audio(f'game_files/sfx/Player/heartbeat_{num}.wav')
            self.heartbeats.append(sfx)
        self.beat = 16
        self.footstep_enhancers = []
        for num in range(1,10):
            sfx = load_audio(f'game_files/sfx/Player/grass_step_{num}.wav')
            self.footstep_enhancers.append(sfx)
        self.played_step = False

    def get_player_image(self):
        self.player_sprite = select_charachter.player_images[select_charachter.current_player][1]
    def respawn(self):
        self.hearts['health_count'] = 20
        self.dead = False
    def update(self):
        walk_cooldown = 4
        key = pygame.key.get_pressed()
        for tile in water_rects:
            if player.hitbox.colliderect(tile[0]):
                self.in_water = True
                self.speed_modifier = 2.2
                break
            else:
                self.in_water = False
                self.speed_modifier = 1.5
        if self.in_water == True:
            for tile in grass_rects:
                if player.hitbox.colliderect(tile[0]):
                    self.submerged = False
                    break
                else:
                    self.submerged = True
        if key[keybinds['run']]:
            if self.run == False and self.run_cooldown >= 1:
                self.speed = 0.8
                self.run = True
                self.run_cooldown = 0
            elif self.run == True and self.run_cooldown >= 1:
                self.speed = 0.1
                self.run = False
                self.run_cooldown = 0
            self.run_cooldown += 1
        if key[pygame.K_w]:
            self.rect.y -= tile_size // (self.speed_modifier - self.speed)
            self.direction = 2
            self.counter += 1
        if key[pygame.K_s]:
            self.rect.y += tile_size // (self.speed_modifier - self.speed)
            self.direction = 0
            self.counter += 1
        if key[pygame.K_a]:
            self.rect.x -= tile_size // (self.speed_modifier - self.speed)
            self.direction = 3
            self.counter += 1
        if key[pygame.K_d]:
            self.rect.x += tile_size // (self.speed_modifier - self.speed)
            self.direction = 1
            self.counter += 1
        #play walk sfx. only play if sfxs are on
        if sfx == True:
            if self.player_walk_frames[self.index] != 0:
                if self.played_step == False:
                    enhance = random.choice(self.footstep_enhancers)
                    player_enhance_step.stop()
                    player_enhance_step.play(enhance)
                    self.played_step = True
            else:
                self.played_step = False
        #print run icon
        if self.run == False:
            screen.blit(self.walk_icon, (400, 1))
        elif self.run == True:
            screen.blit(self.run_icon, (400, 1))
        #add animation
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= 4:
                self.index = 0
        #can't go just based on index b/c the middle frame is the 1st frame
        self.vert_frame = self.player_walk_frames[self.index]
        #set back to standing if no key is pressed
        if not key[keybinds['forward']] and not key[keybinds['backward']] and not key[keybinds['left']] and not key[keybinds['right']]:
            if self.direction == 0:
                self.counter = 0
                self.index = 0
            if self.direction == 1:
                self.counter = 0
                self.index = 0
            if self.direction == 2:
                self.counter = 0
                self.index = 0
            if self.direction == 3:
                self.counter = 0
                self.index = 0
            if self.chop_timer > 0:
                self.vert_frame = self.chop_timer + 2
        #be swimming if in water
        if self.submerged == True:
            self.vert_frame = 8
        self.hitbox = pygame.rect.Rect(0, 0, 32, 64)
        self.hitbox.x = self.rect.x - true_scroll[0]
        self.hitbox.y = self.rect.y - true_scroll[1]
        #blit player to screen
        screen.blit(self.player_sprite, self.hitbox, (32 * self.direction, 64 * self.vert_frame, 32, 63))
        #mke new rect that locks to img for hitbox
        if debug == True:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
    def armour(self):
        #get protection for each piece of armour
        #25, 26, 27, 28
        if inventory.slots['slot_25']['item_data'] != None:
            helmet_protection = inventory.slots['slot_25']['item_data'].protection
        else:
            helmet_protection = 0
        if inventory.slots['slot_26']['item_data'] != None:
            chestplate_protection = inventory.slots['slot_26']['item_data'].protection
        else:
            chestplate_protection = 0
        if inventory.slots['slot_27']['item_data'] != None:
            legs_protection = inventory.slots['slot_27']['item_data'].protection
        else:
            legs_protection = 0
        if inventory.slots['slot_28']['item_data'] != None:
            boots_protection = inventory.slots['slot_28']['item_data'].protection
        else:
            boots_protection = 0
        #blit armour img onto player
        if inventory.slots['slot_25']['item_data'] != None:
            if inventory.slots['slot_25']['item_data'].item_name == 'Sugar Cloth Helmet':
                screen.blit(self.helmet_img, self.hitbox, (32 * self.direction, 0, 32, 64))
        if inventory.slots['slot_26']['item_data'] != None:
            if inventory.slots['slot_26']['item_data'].item_name == 'Sugar Cloth Tunic':
                screen.blit(self.tunic_img, self.hitbox, (32 * self.direction, 64 * self.vert_frame, 32, 63))
        if inventory.slots['slot_27']['item_data'] != None:
            if inventory.slots['slot_27']['item_data'].item_name == 'Sugar Cloth Pants':
                screen.blit(self.leggings_img, self.hitbox, (32 * self.direction, 64 * self.vert_frame, 32, 63))
        if inventory.slots['slot_28']['item_data'] != None:
            if inventory.slots['slot_28']['item_data'].item_name == 'Sugar Cloth Boots':
                screen.blit(self.boots_img, self.hitbox, (32 * self.direction, 64 * self.vert_frame, 32, 63))
        #create images for armour UI
        self.armour_points['armour_count'] = helmet_protection + chestplate_protection + legs_protection + boots_protection
        if self.armour_points['armour_count'] == 20:
            for num in range(1,11):
                self.armour_points[f'armour_{num}'] = self.armour_full
        elif self.armour_points['armour_count'] == 19:
            for num in range(1,10):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(10,11):
                self.armour_points[f'armour_{num}'] = self.armour_half
        elif self.armour_points['armour_count'] == 18:
            for num in range(1,10):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(10,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 17:
            for num in range(1,9):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(9,10):
                self.armour_points[f'armour_{num}'] = self.armour_half
            for num in range(10,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 16:
            for num in range(1,9):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(9,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 15:
            for num in range(1,8):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(8,9):
                self.armour_points[f'armour_{num}'] = self.armour_half
            for num in range(9,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 14:
            for num in range(1,8):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(8,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 13:
            for num in range(1,7):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(7,8):
                self.armour_points[f'armour_{num}'] = self.armour_half
            for num in range(8,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 12:
            for num in range(1,7):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(7,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 11:
            for num in range(1,6):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(6,7):
                self.armour_points[f'armour_{num}'] = self.armour_half
            for num in range(7,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 10:
            for num in range(1,6):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(6,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 9:
            for num in range(1,5):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(5,6):
                self.armour_points[f'armour_{num}'] = self.armour_half
            for num in range(6,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 8:
            for num in range(1,5):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(5,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 7:
            for num in range(1,4):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(4,5):
                self.armour_points[f'armour_{num}'] = self.armour_half
            for num in range(5,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 6:
            for num in range(1,4):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(4,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 5:
            for num in range(1,3):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(3,4):
                self.armour_points[f'armour_{num}'] = self.armour_half
            for num in range(4,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 4:
            for num in range(1,3):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(3,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 3:
            for num in range(1,2):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(2,3):
                self.armour_points[f'armour_{num}'] = self.armour_half
            for num in range(3,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 2:
            for num in range(1,2):
                self.armour_points[f'armour_{num}'] = self.armour_half
            for num in range(2,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 1:
            for num in range(1,2):
                self.armour_points[f'armour_{num}'] = self.armour_half
            for num in range(2,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 0:
            for num in range(1,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        for num in range(1,11):
            screen.blit(self.armour_bg, (num * 15 + 420, 16))
            screen.blit(self.armour_points[f'armour_{num}'], (num * 15 + 420, 16))
    def health(self):
        if self.hearts['health_count'] <= 20:
            if self.regen_counter == 25:
                self.hearts['health_count'] += 1
                self.regen_counter = 0
            else:
                self.regen_counter += 1
        if self.hearts['health_count'] == 20:
            for num in range(1,11):
                self.hearts[f'heart_{num}'] = self.heart_full
        elif self.hearts['health_count'] == 19:
            for num in range(1,10):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(10,11):
                self.hearts[f'heart_{num}'] = self.heart_half
        elif self.hearts['health_count'] == 18:
            for num in range(1,10):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(10,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 17:
            for num in range(1,9):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(9,10):
                self.hearts[f'heart_{num}'] = self.heart_half
            for num in range(10,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 16:
            for num in range(1,9):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(9,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 15:
            for num in range(1,8):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(8,9):
                self.hearts[f'heart_{num}'] = self.heart_half
            for num in range(9,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 14:
            for num in range(1,8):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(8,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 13:
            for num in range(1,7):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(7,8):
                self.hearts[f'heart_{num}'] = self.heart_half
            for num in range(8,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 12:
            for num in range(1,7):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(7,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 11:
            for num in range(1,6):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(6,7):
                self.hearts[f'heart_{num}'] = self.heart_half
            for num in range(7,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 10:
            for num in range(1,6):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(6,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 9:
            for num in range(1,5):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(5,6):
                self.hearts[f'heart_{num}'] = self.heart_half
            for num in range(6,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 8:
            for num in range(1,5):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(5,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 7:
            for num in range(1,4):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(4,5):
                self.hearts[f'heart_{num}'] = self.heart_half
            for num in range(5,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 6:
            for num in range(1,4):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(4,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 5:
            for num in range(1,3):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(3,4):
                self.hearts[f'heart_{num}'] = self.heart_half
            for num in range(4,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 4:
            for num in range(1,3):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(3,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 3:
            for num in range(1,2):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(2,3):
                self.hearts[f'heart_{num}'] = self.heart_half
            for num in range(3,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 2:
            for num in range(1,2):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(2,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 1:
            for num in range(1,2):
                self.hearts[f'heart_{num}'] = self.heart_half
            for num in range(2,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 0:
            for num in range(1,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        if self.hearts['health_count'] == 0:
            self.dead = True
        #blit heart ui
        for num in range(1,11):
            screen.blit(self.heart_bg, (num * 15 + 420, 0))
            screen.blit(self.hearts[f'heart_{num}'], (num * 15 + 420, 0))
        #play heartbeat if below 3 hearts. only play if sfxs is on
        if sfx == True:
            if self.hearts['health_count'] < 6:
                if self.beat >= 12:
                    sound = random.choices(self.heartbeats, k=1, weights=(0.01, 100, 100, 100))[0]
                    sound.play()
                    self.beat = 0
                else:
                    self.beat += 1
            elif self.hearts['health_count'] < 8:
                if self.beat == 16:
                    sound = random.choices(self.heartbeats, k=1, weights=(0.01, 100, 100, 100))[0]
                    sound.play()
                    self.beat = 0
                else:
                    self.beat += 1
            else:
                self.beat = 16
        return game_state
    def damage(self, damage_amount):
        if self.armour_points['armour_count'] == 0:
            damage_reduce_percent = 1
        else:
            #print(self.armour_points['armour_count'] / 21)
            damage_reduce_percent = 1 - round(self.armour_points['armour_count'] / 21, 1)
        self.hearts['health_count'] -= round(damage_amount * damage_reduce_percent)
    def get_event(self, event):
        self.event = event
    def use_item(self, hotbar_slots, hotbar_selector_slots):
        #get item data from hotbar
        item_info = hotbar_slots[f'slot_{hotbar.selector_slot + 1}']
        if item_info[0] == None:
            item_damage = 0
        else:
            item_damage = item_data[item_info[3]]['damage']
            item_throwability = item_data[item_info[3]]['throwable']
        event = self.event
        #get key presses
        key = pygame.key.get_pressed()
        #move destruction rect based on direction the player is facing
        if self.direction == 2:
            item_rect_top = self.rect.y - scroll[1] - self.height
            item_rect_left = self.rect.x  - scroll[0]
        if self.direction == 3:
            item_rect_left = self.rect.x   - scroll[0] - self.width
            item_rect_top = self.rect.y  - scroll[1]
        if self.direction == 0:
            item_rect_top = self.rect.y  - scroll[1] + self.height
            item_rect_left = self.rect.x  - scroll[0]
        if self.direction == 1:
            item_rect_left = self.rect.x  - scroll[0] + self.width
            item_rect_top = self.rect.y  - scroll[1]
        #create destricuion rect
        item_rect = pygame.Rect(item_rect_left, item_rect_top, self.width, self.height)
        #check if attack key was pressed and not currently attacking
        if key[keybinds['break block/attack']]:
            if self.chopping == False:
                self.chopping = True
        if self.chopping == True:
            if self.chop_timer == 5 and self.broken == False:
                #grass rects contain all interactable items
                global game_map
                #damage interactables
                for tile in grass_rects:
                    if tile[3] != None:
                        #get interactable class
                        game_map_tile = game_map[tile[1]][tile[3].chunk_location][2]
                        #check if your item hittign area collides with the interactable
                        if pygame.Rect.colliderect(item_rect, game_map_tile.rect) and isinstance(game_map_tile, Interactable):
                            #game_map[game_map_tile.chunk][game_map_tile.chunk_location][2].damage(2, item_damage)
                            game_map[tile[1]][tile[3].chunk_location][2].damage(2, item_damage)
                #damage entities
                for entity in game_engines.enitites.entitie_dict:
                    if item_rect.colliderect(game_engines.enitites.entitie_dict[entity].rect):
                        game_engines.enitites.entitie_dict[entity].damage(1 + item_damage)
                self.broken = True
            #wait for the key to be released to prevent holding don the button
            elif self.broken == True:
                if event.type == pygame.KEYUP:
                    if event.key == keybinds['break block/attack']:
                        self.chop_timer = 0
                        self.broken = False
                        self.chopping = False
            else:
                self.chop_timer += 1
        if debug == True:
            pygame.draw.rect(screen, (255, 255, 255), item_rect, 2)
#gui classes
class Hotbar():
    def __init__(self):
        img_selected = pygame.image.load('game_files/imgs/gui/inventory_slot_selected.png')
        self.img_selected = pygame.transform.scale(img_selected, (tile_size * 3, tile_size * 3))
        hotbar_img = pygame.image.load('game_files/imgs/gui/hotbar.png')
        self.hotbar_img = pygame.transform.scale(hotbar_img, (tile_size * 15, tile_size * 3))
        self.hotbar_rect = self.hotbar_img.get_rect()
        hotbar_bg = pygame.image.load('game_files/imgs/gui/hotbar_bg.png')
        self.hotbar_bg = pygame.transform.scale(hotbar_bg, (tile_size * 15, tile_size * 3))
        #first is item ID, second is stack size
        self.selector = [[self.hotbar_rect.x, self.hotbar_rect.y], self.img_selected]
        self.selector_slot = 0
        self.hotbar_slots = {}
        self.get_slot_data()
        self.selected_item = 0
    def update(self):
        key = pygame.key.get_pressed()
        if key[keybinds['hotbar_1']]:
            self.selector_slot = 0
            self.selected_item = self.hotbar_slots['slot_1'][0]
        elif key[keybinds['hotbar_2']]:
            self.selector_slot = 1
            self.selected_item = self.hotbar_slots['slot_2'][0]
        elif key[keybinds['hotbar_3']]:
            self.selector_slot = 2
            self.selected_item = self.hotbar_slots['slot_3'][0]
        elif key[keybinds['hotbar_4']]:
            self.selector_slot = 3
            self.selected_item = self.hotbar_slots['slot_4'][0]
        elif key[keybinds['hotbar_5']]:
            self.selector_slot = 4
            self.selected_item = self.hotbar_slots['slot_5'][0]
        self.hotbar_rect.centerx = 300
        self.hotbar_rect.y = 540
        self.selector = [[self.hotbar_rect.x + (tile_size * self.selector_slot * 3), self.hotbar_rect.y], self.img_selected]
        screen.blit(self.hotbar_bg, self.hotbar_rect)
        screen.blit(self.hotbar_img, self.hotbar_rect)
        for num in range (1, 6):
            if self.hotbar_slots[f'slot_{num}'][0] != None:
                #slots start at 1, so have to go back 1 tile size on blit
                screen.blit(item_imgs, (self.hotbar_rect.x + ((tile_size * 3 * num) - tile_size * 3), self.hotbar_rect.y), self.hotbar_slots[f'slot_{num}'][0])
                text_img = font_inventory.render(str(self.hotbar_slots[f'slot_{num}'][1]), True, (255, 255, 255))
                text_rect = text_img.get_rect()
                text_rect.right = self.hotbar_rect.x + (tile_size * 3 * num) - (tile_size / 3) 
                text_rect.bottom = self.hotbar_rect.bottom
                screen.blit(text_img, text_rect)
        screen.blit(self.selector[1],(self.selector[0][0], self.selector[0][1]))
    def get_slot_data(self):
        #get item data from inventory
        for num in range(1, 6):
            if inventory.slots[f'slot_{num + 19}']['item_data'] == None:
                self.hotbar_slots[f'slot_{num}'] = [None]
            else:
                self.hotbar_slots[f'slot_{num}'] = [inventory.slots[f'slot_{num + 19}']['item_data'].img_coords, inventory.slots[f'slot_{num + 19}']['item_data'].amount, f'slot_{num + 19}', inventory.slots[f'slot_{num + 19}']['item_data'].data_num]
class Inventory():
    def __init__(self):
        inventory_img = pygame.image.load('game_files/imgs/gui/inventory.png')
        self.inventory_img = pygame.transform.scale(inventory_img, (tile_size * 15, tile_size * 12))
        self.inventory_rect = self.inventory_img.get_rect()
        self.inventory_rect.centerx = 300
        self.inventory_rect.centery = 300
        
        self.page_left = inventory_page_left
        self.left_rect = self.page_left.get_rect()
        self.left_rect.centerx = 300 - 125
        self.left_rect.centery = 300
        self.page_right = inventory_page_right
        self.right_rect = self.page_right.get_rect()
        self.right_rect.centerx = 300 + 125
        self.right_rect.centery = 300

        hotbar_img = pygame.image.load('game_files/imgs/gui/inventory_hotbar.png')
        self.hotbar_img = pygame.transform.scale(hotbar_img, (tile_size * 15, tile_size * 3))
        self.hotbar_rect = self.hotbar_img.get_rect()
        self.hotbar_rect.centerx = self.inventory_rect.centerx
        self.hotbar_rect.y = 540
        
        armour_img = pygame.image.load('game_files/imgs/gui/armour_slots.png')
        self.armour_img = pygame.transform.scale(armour_img, (tile_size * 3, tile_size * 12))
        self.armour_rect = self.armour_img.get_rect()
        self.armour_rect.centerx = 200 - (tile_size * 3)
        self.armour_rect.y = self.inventory_rect.y
        
        delete_img = pygame.image.load('game_files/imgs/gui/armour_slots.png')
        self.delete_img = pygame.transform.scale(delete_img, (tile_size * 3, tile_size * 12))
        self.delete_rect = self.armour_img.get_rect()
        self.delete_rect.centerx = 495 - (tile_size * 3)
        self.delete_rect.y = self.inventory_rect.y

        arrow = pygame.image.load('game_files/imgs/gui/crafting_arrow.png')
        self.arrow = pygame.transform.scale(arrow, (tile_size * 1.8, tile_size * 2))
        
        ribbon_1 = pygame.image.load('game_files/imgs/gui/ribbon_1.png')
        self.ribbon_1 = pygame.transform.scale(ribbon_1, (tile_size * 2, tile_size * 3))
        self.ribbon_1_rect = self.ribbon_1.get_rect()
        self.ribbon_1_rect.x = self.left_rect.x + 40
        self.ribbon_1_rect.y = self.left_rect.bottom - 7
        ribbon_2 = pygame.image.load('game_files/imgs/gui/ribbon_2.png')
        self.ribbon_2 = pygame.transform.scale(ribbon_2, (tile_size * 2, tile_size * 3))
        self.ribbon_2_rect = self.ribbon_2.get_rect()
        self.ribbon_2_rect.x = self.left_rect.x + 80
        self.ribbon_2_rect.y = self.left_rect.bottom - 5
        self.page_break = pygame.image.load('game_files/imgs/menu/page_break.png')
        self.page_break_1_rect = self.page_break.get_rect()
        self.page_break_1_rect.centerx = self.right_rect.centerx
        self.page_break_1_rect.centery = self.right_rect.centery + (tile_size * 8)
        self.page_break_2_rect = self.page_break.get_rect()
        self.page_break_2_rect.centerx = self.left_rect.centerx
        self.page_break_2_rect.centery = self.left_rect.y + (tile_size * 13)
        self.page_break_3_rect = self.page_break.get_rect()
        self.page_break_3_rect.centerx = self.left_rect.centerx
        self.page_break_3_rect.centery = self.left_rect.y + (tile_size * 16.5)
        self.slots = {}
        img_rect = pygame.rect.Rect(0, 0, tile_size * 3, tile_size * 3)
        coord = 0
        #1st 20 are main inventory, next 5 are hotbar, next 4 are armour, next 9 are crafting grid, last 1 is crafting output
        for num in range(0, 39):
            #set up main inventory
            if 0 <= num <= 3:
                rect = img_rect.copy()
                rect.centerx = self.right_rect.x + (tile_size * 3 * coord) + 50
                rect.y =  self.right_rect.y + 50
                self.slots[f'slot_{num}'] = {
                                            'img_coords': (0, 0, tile_size * 3, tile_size * 3),
                                            'rect': rect,
                                            'item_data': None
                                            }
            elif 4 <= num <= 7:
                rect = img_rect.copy()
                rect.centerx = self.right_rect.x + (tile_size * 3 * coord) + 50
                rect.y =  self.right_rect.y + (tile_size * 3) + 50
                self.slots[f'slot_{num}'] = {
                                            'img_coords': (0, 0, tile_size * 3, tile_size * 3),
                                            'rect': rect,
                                            'item_data': None
                                            }
            elif 8 <= num <= 11:
                rect = img_rect.copy()
                
                rect.centerx = self.right_rect.x + (tile_size * 3 * coord) + 50
                rect.y =  self.right_rect.y  + (tile_size * 3 * 2) + 50
                self.slots[f'slot_{num}'] = {
                                            'img_coords': (0, 0, tile_size * 3, tile_size * 3),
                                            'rect': rect,
                                            'item_data': None
                                            }
            elif 12 <= num <= 15:
                rect = img_rect.copy()
                rect.centerx = self.right_rect.x + (tile_size * 3 * coord) + 50
                rect.y =  self.right_rect.y  + (tile_size * 3 * 3) + 50
                self.slots[f'slot_{num}'] = {
                                            'img_coords': (0, 0, tile_size * 3, tile_size * 3),
                                            'rect': rect,
                                            'item_data': None
                                            }
            elif 16 <= num <= 19:
                rect = img_rect.copy()
                rect.centerx = self.right_rect.x + (tile_size * 3 * coord) + 50
                rect.y =  self.right_rect.y  + (tile_size * 3 * 4) + 50
                self.slots[f'slot_{num}'] = {
                                            'img_coords': (0, 0, tile_size * 3, tile_size * 3),
                                            'rect': rect,
                                            'item_data': None
                                            }
            #set up hotbar
            elif 20 <= num <= 24:
                rect = img_rect.copy()
                rect.x = self.hotbar_rect.x + (tile_size * 3 * coord)
                rect.y =  self.hotbar_rect.y
                self.slots[f'slot_{num}'] = {
                                                    'img_coords': (0, 0, tile_size * 3, tile_size * 3),
                                                    'rect': rect,
                                                    'item_data': None
                                                    }
            #set up armour
            elif 25 <= num <= 28:
                #head
                if num == 25:
                   rect = img_rect.copy()
                   rect.x = self.left_rect.x + (tile_size * 3 * 0) + 30
                   rect.y =  self.left_rect.y + 200
                   self.slots[f'slot_{num}'] = {
                                               'img_coords': (tile_size * 3 * 2, 0, tile_size * 3, tile_size * 3),
                                               'item_img_coords':(0, 0, tile_size * 3, tile_size * 3),
                                               'rect': rect,
                                               'item_data': None
                                               }
                #torso
                if num == 26:
                    rect = img_rect.copy()
                    rect.x = self.left_rect.x + (tile_size * 3 * 1) + 30
                    rect.y =  self.left_rect.y + 200
                    self.slots[f'slot_{num}'] = {
                                                'img_coords': (tile_size * 3 * 3, 0, tile_size * 3, tile_size * 3),
                                                'item_img_coords':(0, 0, tile_size * 3, tile_size * 3),
                                                'rect': rect,
                                                'item_data': None
                                                }
                #legs
                if num == 27:
                    rect = img_rect.copy()
                    rect.x = self.left_rect.x  + (tile_size * 3 * 2) + 30
                    rect.y =  self.left_rect.y + 200
                    self.slots[f'slot_{num}'] = {
                                                'img_coords': (tile_size * 4 * 3, 0, tile_size * 3, tile_size * 3),
                                                'item_img_coords':(0, 0, tile_size * 3, tile_size * 3),
                                                'rect': rect,
                                                'item_data': None
                                                }\
                #boots
                if num == 28:
                    rect = img_rect.copy()
                    rect.x = self.left_rect.x + (tile_size * 3 * 3) + 30
                    rect.y =  self.left_rect.y + 200
                    self.slots[f'slot_{num}'] = {
                                                'img_coords': (tile_size * 5 * 3, 0, tile_size * 3, tile_size * 3),
                                                'item_img_coords':(0, 0, tile_size * 3, tile_size * 3),
                                                'rect': rect,
                                                'item_data': None
                                                }
            #set up crafting
            elif 29 <= num <= 31:
                rect = img_rect.copy()
                rect.x = self.left_rect.x + (tile_size * 3 * coord) + 20
                rect.y =  self.left_rect.y + 50
                self.slots[f'slot_{num}'] = {
                                            'img_coords': (0, 0, tile_size * 3, tile_size * 3),
                                            'rect': rect,
                                            'item_data': None
                                            }
            elif 32 <= num <= 34:
                rect = img_rect.copy()
                rect.x = self.left_rect.x + (tile_size * 3 * coord) + 20
                rect.y =  self.left_rect.y + (tile_size * 3 * 1) + 50
                self.slots[f'slot_{num}'] = {
                                            'img_coords': (0, 0, tile_size * 3, tile_size * 3),
                                            'rect': rect,
                                            'item_data': None
                                            }
            elif 35 <= num <= 37:
                rect = img_rect.copy()
                rect.x = self.left_rect.x + (tile_size * 3 * coord) + 20
                rect.y =  self.left_rect.y + (tile_size * 3 * 2) + 50
                self.slots[f'slot_{num}'] = {
                                            'img_coords': (0, 0, tile_size * 3, tile_size * 3),
                                            'rect': rect,
                                            'item_data': None
                                            }
            elif num == 38:
                rect = img_rect.copy()
                rect.x = self.left_rect.x + (tile_size * 3 * 4)
                rect.y =  self.left_rect.y + (tile_size * 3) + 50
                self.slots[f'slot_{num}'] = {
                                        'img_coords': (0, 0, tile_size * 3, tile_size * 3),
                                        'rect': rect,
                                        'item_data': None
                                        }
            coord += 1
            if num < 19:
                if coord > 3:
                    coord = 0
            elif num == 19:
                coord = 0
            elif num < 25:
                if coord > 4:
                    coord = 0
            elif num < 28:
                if coord > 3:
                    coord = 0
            else:
                if coord > 2:
                    coord = 0
        self.inventory_sort_btn = combined_inventory_button
        self.inventory_sort_btn_hover = combined_inventory_button_hover
        self.inventory_sort_btn_click = combined_inventory_button_click
        self.inventory_sort_rect = self.inventory_sort_btn.get_rect()
        self.inventory_sort_rect.x = self.slots['slot_16']['rect'].x
        self.inventory_sort_rect.y = self.slots['slot_16']['rect'].y + (tile_size * 3)
        
        self.delete_slot_rect = pygame.rect.Rect(0, 0, tile_size * 3, tile_size * 3)
        self.delete_slot_rect.x = self.slots['slot_19']['rect'].x
        self.delete_slot_rect.y = self.slots['slot_19']['rect'].y + (tile_size * 3)
        self.mouse_holding = False
        self.mouse_down = False
        self.mouse_up = True
        self.can_place = False
        self.pick_time = 0
        self.scroll_up = False
        self.scroll_down = False
        self.combined_stacks_selected = False
        self.got_stack = False
        self.current_page = 'crafting'
        #create recipie book
        recipie_book_button = pygame.image.load('game_files/imgs/menu/recipie_book_button.png')
        self.recipie_book_button = pygame.transform.scale(recipie_book_button, (tile_size * 2, tile_size * 2))
        recipie_book_button_selected = pygame.image.load('game_files/imgs/menu/recipie_book_button_selected.png')
        self.recipie_book_button_selected = pygame.transform.scale(recipie_book_button_selected, (tile_size * 2, tile_size * 2))
        self.recipie_book = {}
        recipie_button_rect = self.recipie_book_button.get_rect()
        x_count = 0
        y_count = 0
        total_count = 0
        self.recipie_book_imgs = pygame.transform.scale(item_imgs, (tile_size * 2 * 7, tile_size * 2 * 4))
        for recipie in crafting_recepies:
            recipie_values = crafting_recepies[recipie]
            rect = recipie_button_rect.copy()
            rect.x = self.left_rect.x + 20 + (35 * x_count)
            rect.y = self.left_rect.y  + 250 + (40 * y_count)
            self.recipie_book[total_count] = {
                                        'recipie_name': recipie,
                                        'slot_data': recipie_values[0],
                                        'output_item': recipie_values[1][0],
                                        'rect': rect,
                                        'output_img_coords':item_data[str(recipie_values[1][0])]['img_coords'],
                                        }
            if x_count > 4:
                x_count = 0
                y_count += 1
            else:
                x_count += 1
            total_count += 1
        self.recipie_book_grid = {}
        for num in range(1, 11):
            self.recipie_book_grid[num] = copy.deepcopy(self.slots[f'slot_{num + 28}'])
            self.recipie_book_grid[num]['rect'].y += 200
        self.selected_recipie = None
        x_icon = pygame.image.load('game_files/imgs/gui/inventory_x_icon.png')
        self.x_icon = pygame.transform.scale(x_icon, (tile_size, tile_size))
        self.x_rect = self.x_icon.get_rect()
        self.x_rect.right = self.recipie_book_grid[10]['rect'].right
        self.x_rect.top = self.recipie_book_grid[1]['rect'].top
        self.player_rect = pygame.rect.Rect(0, 0, 16 * 4, 32 * 4)
        self.player_rect.centerx = self.left_rect.centerx 
        self.player_rect.y = self.left_rect.y + 50
        self.player_frame = 0
        arrow = pygame.image.load('game_files/imgs/gui/charachter_select_arrow.png')
        self.arrow_left = pygame.transform.scale(arrow, (arrow.get_width() * 2, arrow.get_height() * 2))
        self.arrow_right = pygame.transform.flip(self.arrow_left, True, False)
        self.arrow_left_rect = self.arrow_left.get_rect()
        self.arrow_left_rect.centerx = self.player_rect.left - 20
        self.arrow_left_rect.centery = self.player_rect.centery
        self.arrow_right_rect = self.arrow_right.get_rect()
        self.arrow_right_rect.centerx = self.player_rect.right + 20
        self.arrow_right_rect.centery = self.player_rect.centery
        self.time_since_last_press = 0
        #load player armour images
        helmet_img = pygame.image.load('game_files/imgs/armour/suger_cloth_helmet.png')
        self.helmet_img = pygame.transform.scale(helmet_img, (helmet_img.get_width() * 4, helmet_img.get_height() * 4))
        tunic_img = pygame.image.load('game_files/imgs/armour/suger_cloth_chestplate.png')
        self.tunic_img = pygame.transform.scale(tunic_img, (tunic_img.get_width() * 4, tunic_img.get_height() * 4))
        leggings_img = pygame.image.load('game_files/imgs/armour/sugar_cloth_leggings.png')
        self.leggings_img = pygame.transform.scale(leggings_img, (leggings_img.get_width() * 4, leggings_img.get_height() * 4))
        boots_img = pygame.image.load('game_files/imgs/armour/sugar_cloth_boots.png')
        self.boots_img = pygame.transform.scale(boots_img, (boots_img.get_width() * 4, boots_img.get_height() * 4))
    def get_player_image(self):
        self.player_sprite = select_charachter.player_images[select_charachter.current_player][2]
    def get_event(self, event):
        #get if the mouse was clicked
        if event.type == pygame.MOUSEBUTTONUP:
            self.mouse_up = True
        else:
            self.mouse_up = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_down = True
            #get if teh scroll wheel was scrolled
            if event.button == 4:
                self.scroll_up = True
            elif event.button == 5:
                self.scroll_down = True
        else:
            self.mouse_down = False
    def update(self):
        #get mouse pos
        mouse_pos = pygame.mouse.get_pos()
        #print background stuff
        screen.blit(self.page_left, self.left_rect)
        screen.blit(self.page_right, self.right_rect)
        screen.blit(inventory_slots, self.delete_slot_rect, (tile_size * 3 * 6, 0, tile_size * 3, tile_size * 3))
        screen.blit(self.page_break, self.page_break_1_rect)
        draw_text('Inventory:', font, (159, 121, 83), self.right_rect.x + 25, self.right_rect.y + 15)
        #change page if clicked on ribbon
        if self.current_page == 'crafting':
            if self.ribbon_2_rect.collidepoint(mouse_pos):
                if self.mouse_down == True:
                    self.current_page = 'armour'
                    self.ribbon_2_rect.y = self.left_rect.bottom - 7
                    self.ribbon_1_rect.y = self.left_rect.bottom - 5
        elif self.current_page == 'armour':
            if self.ribbon_1_rect.collidepoint(mouse_pos):
                if self.mouse_down == True:
                    self.current_page = 'crafting'
                    self.ribbon_1_rect.y = self.left_rect.bottom - 7
                    self.ribbon_2_rect.y = self.left_rect.bottom - 5
        #blit visuals specific to the current page; this is seperated from above to prevent delay in the imgs dissapearng when switching pages
        if self.current_page == 'crafting':
            draw_text('Crafting:', font, (159, 121, 83), self.left_rect.x + 25, self.left_rect.y + 15)
            screen.blit(self.arrow, (self.left_rect.x + (tile_size * 3 * 3.43), self.left_rect.y + (tile_size * 6)))
            screen.blit(self.page_break, self.page_break_2_rect)
            draw_text('Recipies:', font, (159, 121, 83), self.left_rect.x + 25, self.left_rect.y + 220)
            if self.selected_recipie == None:
                for recipie_key in self.recipie_book:
                    recipie = self.recipie_book[recipie_key]
                    screen.blit(self.recipie_book_button, recipie['rect'])
                    #have to multiply by 2/3 to fit image coords ment for 3x size to 2x size
                    screen.blit(self.recipie_book_imgs, recipie['rect'], (recipie['output_img_coords'][0] * (2/3), recipie['output_img_coords'][1] * (2/3), recipie['output_img_coords'][2] * (2/3), recipie['output_img_coords'][3] * (2/3)))
                    #show recipie if you click on associated button
                    if recipie['rect'].collidepoint(mouse_pos):
                        if self.mouse_down == True:
                            self.selected_recipie = recipie_key
            else:
                for slot_key in self.recipie_book_grid:
                    slot = self.recipie_book_grid[slot_key]
                    #blit grid to screen
                    screen.blit(inventory_slots, slot['rect'], slot['img_coords'])
                    #blit arrow
                    screen.blit(self.arrow, (self.left_rect.x + (tile_size * 3 * 3.43), self.left_rect.y + (tile_size * 6) + 200))
                    #draw item name when hovered over
                    if slot['rect'].collidepoint(mouse_pos):
                        if slot_key < 10:
                            if self.recipie_book[self.selected_recipie]['slot_data'][slot_key - 1] != None:
                                item_name_img = font.render(item_data[str(self.recipie_book[self.selected_recipie]['slot_data'][slot_key - 1])]['item_name'], True, (0, 0, 0))
                                item_name_rect = item_name_img.get_rect()
                                item_name_rect.centerx = self.left_rect.centerx 
                                item_name_rect.y = self.left_rect.bottom - 50
                                screen.blit(item_name_img, item_name_rect)
                        elif slot_key == 10:
                            item_name_img = font.render(item_data[str(self.recipie_book[self.selected_recipie]['output_item'])]['item_name'], True, (0, 0, 0))
                            item_name_rect = item_name_img.get_rect()
                            item_name_rect.centerx = self.left_rect.centerx 
                            item_name_rect.y = self.left_rect.bottom - 50
                            screen.blit(item_name_img, item_name_rect)
                #blit items into slots
                #output slot is in a different section of the list
                for num in range(1, 10):
                    if self.recipie_book[self.selected_recipie]['slot_data'][num - 1] != None:
                        screen.blit(item_imgs, self.recipie_book_grid[num]['rect'], item_data[str(self.recipie_book[self.selected_recipie]['slot_data'][num - 1])]['img_coords'])
                screen.blit(item_imgs, self.recipie_book_grid[10]['rect'], self.recipie_book[self.selected_recipie]['output_img_coords'])
                #show x icon and check if it has been clicked
                screen.blit(self.x_icon, self.x_rect)
                if self.x_rect.collidepoint(mouse_pos):
                    if self.mouse_down == True:
                        self.selected_recipie = None
        elif self.current_page == 'armour':
            draw_text('Armour:', font, (159, 121, 83), self.left_rect.x + 25, self.left_rect.y + 15)
            screen.blit(self.page_break, self.page_break_3_rect)
            #draw player
            screen.blit(self.player_sprite, self.player_rect, (16 * self.player_frame * 4, 0, 16 * 4, 32 * 4))
            #draw arrows
            screen.blit(self.arrow_left, self.arrow_left_rect)
            screen.blit(self.arrow_right, self.arrow_right_rect)
            #change player angle if arrow is clicked
            if self.arrow_left_rect.collidepoint(mouse_pos):
                #check if the mouse has been clicked
                if pygame.mouse.get_pressed()[0]:
                    #wait time so there actully is control over the movment
                    if time.time() - self.time_since_last_press > 0.4:
                        if self.player_frame > 0:
                            self.player_frame -= 1
                        else:
                            self.player_frame = 3
                        self.time_since_last_press = time.time()
            elif self.arrow_right_rect.collidepoint(mouse_pos):
                #check if the mouse has been clicked
                if pygame.mouse.get_pressed()[0]:
                    #wait time so there actully is control over the movment
                    if time.time() - self.time_since_last_press > 0.4:
                        if self.player_frame < 3:
                            self.player_frame += 1
                        else:
                            self.player_frame = 0
                        self.time_since_last_press = time.time()
            #blit armour onto player
            if self.slots['slot_25']['item_data'] != None:
                if self.slots['slot_25']['item_data'].item_name == 'Sugar Cloth Helmet':
                    screen.blit(self.helmet_img, self.player_rect, (16 * self.player_frame * 4, 0, 16 * 4, 32 * 4))
            if self.slots['slot_26']['item_data'] != None:
                if self.slots['slot_26']['item_data'].item_name == 'Sugar Cloth Tunic':
                    screen.blit(self.tunic_img, self.player_rect, (16 * self.player_frame * 4, 0, 16 * 4, 32 * 4))
            if self.slots['slot_27']['item_data'] != None:
                if self.slots['slot_27']['item_data'].item_name == 'Sugar Cloth Pants':
                    screen.blit(self.leggings_img, self.player_rect, (16 * self.player_frame * 4, 0, 16 * 4, 32 * 4))
            if self.slots['slot_28']['item_data'] != None:
                if self.slots['slot_28']['item_data'].item_name == 'Sugar Cloth Boots':
                    screen.blit(self.boots_img, self.player_rect, (16 * self.player_frame * 4, 0, 16 * 4, 32 * 4))
        screen.blit(self.ribbon_1, self.ribbon_1_rect)
        screen.blit(self.ribbon_2, self.ribbon_2_rect)
        #check if combined stacks is clicked on, cant turn on if holding an item 
        if self.combined_stacks_selected and self.mouse_holding == False:
            screen.blit(self.inventory_sort_btn_click, self.inventory_sort_rect)
            if self.inventory_sort_rect.collidepoint(mouse_pos):
                #change button state if clicked
                if self.mouse_down == True:
                    self.combined_stacks_selected = False
        else:
            #do hover image if hover over the button
            if self.inventory_sort_rect.collidepoint(mouse_pos):
                screen.blit(self.inventory_sort_btn_hover, self.inventory_sort_rect)
                #change button state if clicked
                if self.mouse_down == True:
                    self.combined_stacks_selected = True
            else:
                screen.blit(self.inventory_sort_btn, self.inventory_sort_rect)
        #iterate through every slot
        for slot_key in self.slots:
            #skip the slots that shouldn't be shown depending on what page you are on
            if self.current_page == 'crafting':
                if slot_key in ['slot_25', 'slot_26', 'slot_27', 'slot_28']:
                    continue
            elif self.current_page == 'armour':
                if slot_key in ['slot_29', 'slot_30', 'slot_31', 'slot_32', 'slot_33', 'slot_34', 'slot_35', 'slot_36', 'slot_37', 'slot_38']:
                    continue
            slot = self.slots[slot_key]
            #if there is nothing in the slot set remvoe the item
            if slot['item_data'] != None:
                if slot['item_data'].amount <= 0:
                    self.slots[slot_key]['item_data'] = None
            #blit slots with special coords if there is or isnt an item
            if slot['item_data'] != None and 'item_img_coords' in slot:
                if slot['item_data'].moving == False:
                    screen.blit(inventory_slots, slot['rect'], slot['item_img_coords'])
                    slot['item_data'].blit_item(slot['rect'], 0)
                elif self.mouse_holding == True and slot_key == self.mouse_items['slot_num']:
                    if self.mouse_items['amount'] != slot['item_data'].amount: 
                        screen.blit(inventory_slots, slot['rect'], slot['item_img_coords'])
                    else:
                        screen.blit(inventory_slots, slot['rect'], slot['img_coords'])
                    slot['item_data'].blit_item(slot['rect'], self.mouse_items['amount'])
                else:
                    slot['item_data'].blit_item(slot['rect'], 0)
            #blit item if there is an item
            elif slot['item_data'] != None:
                screen.blit(inventory_slots, slot['rect'], slot['img_coords'])
                if self.mouse_holding == True and slot_key == self.mouse_items['slot_num']:
                    slot['item_data'].blit_item(slot['rect'], self.mouse_items['amount'])
                else:
                    slot['item_data'].blit_item(slot['rect'], 0)
            #just blit slot if there is no item
            else:
                screen.blit(inventory_slots, slot['rect'], slot['img_coords'])
            #print item name if hovering over it
            if slot['rect'].collidepoint(mouse_pos) and slot['item_data'] != None:
                #don't draw name if you hover over something you are moving
                if slot['item_data'].moving == False:
                    item_name_img = font.render(slot['item_data'].item_name, True, (0, 0, 0))
                    item_name_rect = item_name_img.get_rect()
                    #show armour items seperetly
                    if slot_key in ['slot_25', 'slot_26', 'slot_27', 'slot_28']:
                        item_name_rect.centerx = self.left_rect.centerx 
                        item_name_rect.y = self.left_rect.centery + 50
                        screen.blit(item_name_img, item_name_rect)
                        #draw protection amount
                        item_prot_img = font_difficulty.render('Protection: ' + str(slot['item_data'].protection), True, (0, 0, 0))
                        item_prot_rect = item_prot_img.get_rect()
                        item_prot_rect.centerx = self.left_rect.centerx 
                        item_prot_rect.y = self.left_rect.centery + 100
                        screen.blit(item_prot_img, item_prot_rect)
                    else:
                        item_name_rect.centerx = self.right_rect.centerx 
                        item_name_rect.y = self.right_rect.bottom - 80
                        screen.blit(item_name_img, item_name_rect)
            #check if mouse collided and was clicked
            if self.mouse_holding == False:
                #if combined stack button is on, moving item normally will not happen
                if self.combined_stacks_selected:
                    #check if you have clicked on a slot
                    if self.mouse_down == True:
                        #only select slot if you clicked on a slot with an item. 0.1 second delay so that you don't just pick up the item from the slot you put the item into
                        if slot['rect'].collidepoint(mouse_pos) and slot['item_data'] != None and (time.time() - self.pick_time) >= 0.1:
                            #can only combined items if the item is stackable
                            if slot['item_data'].stackable:
                                selected_item = slot['item_data'].data_num
                                selected_slot = slot_key
                                self.got_stack = True
                                #set timer to give time to put down the item
                                self.grab_time = time.time()
                            else:
                                self.combined_stacks_selected = False
                else:
                    if self.mouse_down == True:
                        #only move item if you clicked on a slot with an item. 0.1 second delay so that you don't just pick up the item from the slot you put the item into
                        if slot['rect'].collidepoint(mouse_pos) and slot['item_data'] != None and (time.time() - self.pick_time) >= 0.1:
                            self.mouse_holding = True
                            self.mouse_items = {
                                            'data_num': slot['item_data'].data_num,
                                            'amount': slot['item_data'].amount,
                                            'img_coords': slot['item_data'].img_coords,
                                            'slot_num': slot_key,
                                            'img_rect': slot['rect'].copy()
                                            }
                            #set timer to give time to put down the item
                            self.grab_time = time.time()
                            #set slot item moving to true
                            self.slots[slot_key]['item_data'].moving = True
            elif self.mouse_holding == True:
                #allow changing amount holding using scroll wheel
                if self.mouse_items['slot_num'] != 38:
                    if self.scroll_up == True:
                        if self.mouse_items['amount'] < self.slots[self.mouse_items['slot_num']]['item_data'].amount:
                            self.mouse_items['amount'] += 1
                    elif self.scroll_down == True:
                        if self.mouse_items['amount'] > 1:
                            self.mouse_items['amount'] -= 1
                self.scroll_up = False
                self.scroll_down = False
                #0.1 second delay so that the game dosent atuomatically detect picking up and placing down an item
                if self.can_place == False:
                    if (time.time() - self.grab_time) >= 0.2:
                        self.can_place = True
                if self.mouse_down == True and self.can_place == True:
                    #only can place an item if you cliked on a slot that is not the crafting output
                    if slot['rect'].collidepoint(mouse_pos) and slot_key != 'slot_38':
                        #get key pressed
                        key = pygame.key.get_pressed()
                        #move if comign from crafting output
                        if self.mouse_items['slot_num'] == 'slot_38':
                            if slot_key == self.mouse_items['slot_num']:
                                self.mouse_holding = False
                                self.can_place = False
                                #set timer so that you don't imediatly place down than pick back up the item,
                                self.pick_time = time.time()
                                self.slots[self.mouse_items['slot_num']]['item_data'].moving = False
                                for num in range(29, 38):
                                    if self.slots[f'slot_{num}']['item_data'] != None:
                                        self.slots[f'slot_{num}']['item_data'].amount -= 1
                            #if new slot is empty
                            elif slot['item_data'] == None:
                                self.mouse_holding = False
                                self.can_place = False
                                #set timer so that you don't imediatly palce down than pick back up the item,
                                self.pick_time = time.time()
                                #set new slot to item and old slot to nothing
                                self.slots[slot_key]['item_data'] = Item(self.mouse_items['data_num'], self.mouse_items['amount'])
                                self.slots[self.mouse_items['slot_num']]['item_data'] = None
                                for num in range(29, 38):
                                    if self.slots[f'slot_{num}']['item_data'] != None:
                                        self.slots[f'slot_{num}']['item_data'].amount -= 1
                            #if slots have the same item
                            elif slot['item_data'].data_num == self.slots[self.mouse_items['slot_num']]['item_data'].data_num:
                                #can only combined items if they can be stacked
                                if slot['item_data'].stackable == True:
                                    self.mouse_holding = False
                                    self.can_place = False
                                    self.pick_time = time.time()
                                    #add 1 to new slot and set old slot to none
                                    self.slots[slot_key]['item_data'].amount += self.mouse_items['amount']
                                    self.slots[self.mouse_items['slot_num']]['item_data'] = None
                                    for num in range(29, 38):
                                        if self.slots[f'slot_{num}']['item_data'] != None:
                                            self.slots[f'slot_{num}']['item_data'].amount -= 1
                        #check if pressing shift to move 1 item
                        elif key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT]:
                            #if you click on the slot the item used to be in, just reset it
                            if slot_key == self.mouse_items['slot_num']:
                                self.can_place = False
                                #set timer so that you don't imediatly palce down than pick back up the ite,
                                self.pick_time = time.time()
                                self.slots[self.mouse_items['slot_num']]['item_data'].moving = False
                            #if new slot is empty
                            elif slot['item_data'] == None:
                                self.can_place = False
                                #set timer so that you don't imediatly palce down than pick back up the ite,
                                self.pick_time = time.time()
                                #set new slot to item
                                self.slots[slot_key]['item_data'] = Item(self.mouse_items['data_num'], 1)
                                #if old slot or mouse item have no items, set them to noting; otherwise remove 1
                                if self.mouse_items['amount'] == 1:
                                    self.mouse_holding = False
                                    self.can_place = False
                                    self.slots[self.mouse_items['slot_num']]['item_data'].moving = False
                                else:
                                    self.mouse_items['amount'] -= 1
                                if self.slots[self.mouse_items['slot_num']]['item_data'].amount == 1:
                                    self.slots[self.mouse_items['slot_num']]['item_data'] = None
                                else:
                                    self.slots[self.mouse_items['slot_num']]['item_data'].amount -= 1
                            #if slots have the same item
                            elif slot['item_data'].data_num == self.slots[self.mouse_items['slot_num']]['item_data'].data_num:
                                self.can_place = False
                                self.pick_time = time.time()
                                #add 1 to new slot 
                                self.slots[slot_key]['item_data'].amount += 1
                                #if old slot or mouse item have no items, set them to noting; otherwise remove 1
                                if self.mouse_items['amount'] == 1:
                                    self.mouse_holding = False
                                    self.can_place = False
                                    self.slots[self.mouse_items['slot_num']]['item_data'].moving = False
                                else:
                                    self.mouse_items['amount'] -= 1
                                if self.slots[self.mouse_items['slot_num']]['item_data'].amount  == 1:
                                    self.slots[self.mouse_items['slot_num']]['item_data'] = None
                                else:
                                    self.slots[self.mouse_items['slot_num']]['item_data'].amount -= 1
                        #if player used scroll wheel to change how many items
                        elif self.mouse_items['amount'] < self.slots[self.mouse_items['slot_num']]['item_data'].amount:
                            #if you click on the slot the item used to be in, just reset it
                            if slot_key == self.mouse_items['slot_num']:
                                self.can_place = False
                                self.mouse_holding = False
                                #set timer so that you don't imediatly palce down than pick back up the ite,
                                self.pick_time = time.time()
                                self.slots[self.mouse_items['slot_num']]['item_data'].moving = False
                            #if new slot is empty
                            elif slot['item_data'] == None:
                                self.can_place = False
                                #set timer so that you don't imediatly place down than pick back up the ite,
                                self.pick_time = time.time()
                                #set new slot to item
                                self.slots[slot_key]['item_data'] = Item(self.mouse_items['data_num'],  self.mouse_items['amount'])
                                #mouse has no items left, slot decreses by amount held by the mouse
                                self.mouse_holding = False
                                self.can_place = False
                                self.slots[self.mouse_items['slot_num']]['item_data'].moving = False
                                self.slots[self.mouse_items['slot_num']]['item_data'].amount -= self.mouse_items['amount']
                            #if slots have the same item
                            elif slot['item_data'].data_num == self.slots[self.mouse_items['slot_num']]['item_data'].data_num:
                                #can only combined items if they can be stacked
                                if slot['item_data'].stackable == True:
                                    self.can_place = False
                                    self.pick_time = time.time()
                                    #add 1 to new slot 
                                    self.slots[slot_key]['item_data'].amount +=  self.mouse_items['amount']
                                    #mouse has no items left, slot decreses by amount held by the mouse
                                    self.mouse_holding = False
                                    self.can_place = False
                                    self.slots[self.mouse_items['slot_num']]['item_data'].moving = False
                                    self.slots[self.mouse_items['slot_num']]['item_data'].amount -= self.mouse_items['amount']
                        
                        #defult move all items
                        else:
                            #if mouse is holding full amount of items from the slot
                            if self.slots[self.mouse_items['slot_num']]['item_data'].amount == self.mouse_items['amount']:
                                #if you click on the slot the item used to be in, just reset it
                                if slot_key == self.mouse_items['slot_num']:
                                    self.mouse_holding = False
                                    self.can_place = False
                                    #set timer so that you don't imediatly palce down than pick back up the ite,
                                    self.pick_time = time.time()
                                    self.slots[self.mouse_items['slot_num']]['item_data'].moving = False
                                #if new slot is empty
                                elif slot['item_data'] == None:
                                    self.mouse_holding = False
                                    self.can_place = False
                                    #set timer so that you don't imediatly palce down than pick back up the ite,
                                    self.pick_time = time.time()
                                    #set new slot to item and old slot to nothing
                                    self.slots[slot_key]['item_data'] = Item(self.mouse_items['data_num'], self.mouse_items['amount'])
                                    self.slots[self.mouse_items['slot_num']]['item_data'] = None
                                #if slots have the same item
                                elif slot['item_data'].data_num == self.slots[self.mouse_items['slot_num']]['item_data'].data_num:
                                    self.mouse_holding = False
                                    self.can_place = False
                                    self.pick_time = time.time()
                                    #add 1 to new slot and set old slot to none
                                    self.slots[slot_key]['item_data'].amount += self.mouse_items['amount']
                                    self.slots[self.mouse_items['slot_num']]['item_data'] = None
                                #if slots have different items
                                else:
                                    self.mouse_holding = False
                                    self.can_place = False
                                    self.pick_time = time.time()
                                    #add 1 to new slot and set old slot to none
                                    class_one =  self.slots[slot_key]['item_data']
                                    class_two = self.slots[self.mouse_items['slot_num']]['item_data']
                                    self.slots[slot_key]['item_data'] = class_two
                                    self.slots[self.mouse_items['slot_num']]['item_data'] = class_one
                    #allow to delete items
                    elif self.delete_slot_rect.collidepoint(mouse_pos):
                        #if used scroll wheel to not hold all items
                        if self.mouse_items['amount'] <= self.slots[self.mouse_items['slot_num']]['item_data'].amount:
                            self.mouse_holding = False
                            self.can_place = False
                            self.pick_time = time.time()
                            #remove items from slot
                            self.slots[self.mouse_items['slot_num']]['item_data'].amount -= self.mouse_items['amount']
                        else:
                            self.mouse_holding = False
                            self.can_place = False
                            self.pick_time = time.time()
                            #remove items from slot
                            self.slots[self.mouse_items['slot_num']]['item_data'] = None
                        
            if self.mouse_holding == True:
                #set area for item img to blit to
                self.mouse_items['img_rect'].x, self.mouse_items['img_rect'].y = mouse_pos[0], mouse_pos[1]
                screen.blit(item_imgs, self.mouse_items['img_rect'], self.mouse_items['img_coords'])
                #blit amount
                text_img = font_inventory.render(str(self.mouse_items['amount']), True, (255, 255, 255))
                text_rect = text_img.get_rect()
                text_rect.right = self.mouse_items['img_rect'].right
                text_rect.bottom = self.mouse_items['img_rect'].bottom
                screen.blit(text_img, text_rect)
        #run combined stacks code if a stack is selected and button is on
        if self.combined_stacks_selected and self.got_stack:
            #usign num in range to only get items in main inventory
            for num in range(0, 39):
                #check if other slot has an item and if that item is the same as the selected slot
                if self.slots[f'slot_{num}']['item_data'] != None and f'slot_{num}' != selected_slot:
                    if self.slots[f'slot_{num}']['item_data'].data_num == selected_item:
                        #add other slot amount to selected slot
                        self.slots[selected_slot]['item_data'].amount += self.slots[f'slot_{num}']['item_data'].amount
                        #set other slot to have no items
                        self.slots[f'slot_{num}']['item_data'] = None
                        #turn off button
                        self.got_stack = False
                        self.combined_stacks_selected = False
        #run crafting function
        self.crafting()
    def crafting(self):
        crafting_grid = []
        #add items from crafting grid to list
        for num in range(29, 38):
            if self.slots[f'slot_{num}']['item_data'] == None:
                crafting_grid.append(self.slots[f'slot_{num}']['item_data'])
            else:
                crafting_grid.append(int(self.slots[f'slot_{num}']['item_data'].data_num))
        #check if pattern is a recipie

        for recipie in crafting_recepies.values():
            if recipie[0] == crafting_grid:
                self.slots['slot_38']['item_data'] = Item(recipie[1][0], recipie[1][1])
                break
            else:
                self.slots['slot_38']['item_data'] = None
    def collect_item(self, item_num):
        #iterate through every slot
        for slot_key in self.slots:
            slot = self.slots[slot_key]
            #check if a slot already contains the item
            if slot['item_data'] != None:
                if slot['item_data'].data_num == str(item_num):
                    self.slots[slot_key]['item_data'].amount += 1
                    #return true so game knows item can be removed from game map
                    return True
        #iterate through every slot
        for slot_key in self.slots:
            slot = self.slots[slot_key]
            if slot['item_data'] == None:
                self.slots[slot_key]['item_data'] = Item(item_num, 1)
                #return true so game knows item can be removed from game map
                return True
        #if there is no avalible slot, return false so game knows item was not collected
        return False
                
class Item():
    def __init__(self, data_num, amount):
        self.data_num = str(data_num)
        self.data = item_data[self.data_num]
        self.amount = amount
        self.load_data()
        self.moving = False
    def load_data(self):
        #function to retrive specifc item data based on item num
        data = item_data[self.data_num]
        self.item_name = data['item_name']
        self.img_coords = data['img_coords']
        self.stackable = data['stackable']
        self.damage = data['damage']
        self.destroy_type = data['destroy_type']
        self.protection = data['protection']
        self.throwable = data['throwable']
        self.moving = False
    def place_item_in_slot(self, data_num, amount):
        self.data_num = str(data_num)
        self.data = item_data[self.data_num]
        self.amount = amount
        self.load_data()
    def save_to_file(self):
        data_to_save = [self.data_num, self.amount]
        return data_to_save
    @classmethod
    def load_from_file(cls, attributes):
        #create new object of this class
        obj = cls.__new__(cls)
        #load variables from attributes
        obj.data_num = str(attributes[0])
        obj.amount = attributes[1]
        #run function to unpack item data
        obj.load_data()
        return obj
    def use(self):
        pass
    def blit_item(self, rect, mouse_amount):
        #blit img only if you are not carying the item
        if self.moving == False:
            screen.blit(item_imgs, rect, self.img_coords)
            #render and blit how many there are
            text_img = font_inventory.render(str(self.amount), True, (255, 255, 255))
            text_rect = text_img.get_rect()
            text_rect.right = rect.right
            text_rect.bottom = rect.bottom
            screen.blit(text_img, text_rect)
        #blit differnet number if carrying some items
        elif self.amount > mouse_amount:
            screen.blit(item_imgs, rect, self.img_coords)
            #render and blit how many there are
            text_img = font_inventory.render(str(self.amount - mouse_amount), True, (255, 255, 255))
            text_rect = text_img.get_rect()
            text_rect.right = rect.right
            text_rect.bottom = rect.bottom
            screen.blit(text_img, text_rect)
class Input_Box():
    def __init__(self, x, y, w, h, active_colour, inactive_colour, resize_type, max_chars=None, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.defult_width = w
        self.x = x
        self.rect.centerx = x
        self.rect.centery = y
        self.defult_y = y
        self.colour_active = active_colour
        self.colour_inactive = inactive_colour
        self.color = colour_inactive
        self.max_chars = max_chars
        self.text_surface = font.render(text, True, self.color)
        self.active = False
        self.resize_type = resize_type
        self.text_pos = 0
        #for typing non-english charachters. IME - input method editor
        self.ime_editing_pos = 0
        self.ime_text_pos = 0
        self.ime_text = text
        self.ime_text_editing = ""
    def update(self, event):
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pos):
                self.active = True
                self.color = self.colour_inactive
            else:
                self.active = False
                self.color = self.colour_active
        if self.active == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    #can't use backspace with no text or at the begining of the text
                    if len(self.ime_text) > 0 and self.ime_text_pos > 0:
                        self.ime_text = self.ime_text[0:self.ime_text_pos - 1] + self.ime_text[self.ime_text_pos:]
                        self.ime_text_pos = max(0, self.ime_text_pos - 1)
                elif event.key == pygame.K_DELETE:
                    self.ime_text = self.ime_text[0:self.ime_text_pos] + self.ime_text[self.ime_text_pos + 1:]
                #move cursor left and right
                elif event.key == pygame.K_LEFT:
                    self.ime_text_pos = max(0, self.ime_text_pos - 1)
                elif event.key == pygame.K_RIGHT:
                    self.ime_text_pos = min(len(self.ime_text), self.ime_text_pos + 1)
                #check for control functions
                elif event.mod & pygame.KMOD_CTRL:
                    #run copy & paste
                    if event.key == pygame.K_v:
                        pasted = pyperclip.paste()
                        self.ime_text = self.ime_text[0:self.ime_text_pos] + str(pasted) + self.ime_text[self.ime_text_pos:]
                    elif event.key == pygame.K_c:
                        pyperclip.copy(self.ime_text)
                    elif event.key == pygame.K_x:
                        pyperclip.copy(self.ime_text)
                        self.ime_text = ''

            elif event.type == pygame.TEXTEDITING:
                if self.max_chars == None or len(self.ime_text) < self.max_chars:
                    #for non english charachters
                    self.ime_editing_text = event.text
                    self.ime_editing_pos = event.start
            elif event.type == pygame.TEXTINPUT:
                if self.max_chars == None or len(self.ime_text) < self.max_chars:
                    #for normal english charachters
                    self.ime_text = self.ime_text[0:self.ime_text_pos] + event.text + self.ime_text[self.ime_text_pos:]
                    self.ime_text_editing = ""
                    self.ime_text_pos += len(event.text)
            
    def draw(self, scroll_amount):
        if self.ime_text_editing:
            #not sure if this works. It is supposed to position intermidate text at the right position, but I can't test it
            combined_text = self.ime_text + self.ime_text_editing
            if self.active == True:
                combined_text = combined_text[0:self.ime_text_pos] + '|' + combined_text[self.ime_text_pos:]
            self.text_surface = font.render(combined_text, True, self.color)
        else:
            #show cursor if clicking on it
            if self.active == True:
                text_to_render = self.ime_text[0:self.ime_text_pos] + '|' + self.ime_text[self.ime_text_pos:]
                self.text_surface = font.render(text_to_render, True, self.color)
            else:
                self.text_surface = font.render(self.ime_text, True, self.color)
        # Resize the box if the text is too long.
        width = max(self.defult_width, self.text_surface.get_width()+10)
        self.rect.y = self.defult_y - scroll_amount
        self.rect.w = width
        if self.resize_type == 'centre':
            self.rect.centerx = self.x
        else:
            self.rect.x = self.x
        # Blit the text.
        screen.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
        return self.ime_text
class Button():
    def __init__(self, x, y, defult_image, hover_image, text, colour):
        self.defult_image = defult_image
        self.hover_image = hover_image

        self.clicked = False
        self.text = text
        self.colour = colour
        self.txt_surface = font.render(self.text, True, self.colour)
        self.text_width = self.txt_surface.get_width()
        
        #resize width to fit text
        if self.txt_surface.get_width() > self.defult_image.get_width():
            self.defult_image = pygame.transform.scale(self.defult_image, (self.txt_surface.get_width() + 20, self.defult_image.get_height()))
            self.hover_image = pygame.transform.scale(self.hover_image, (self.txt_surface.get_width() + 40, self.hover_image.get_height()))
        self.image = self.defult_image
        self.defult_rect = self.defult_image.get_rect()
        self.hover_rect = self.hover_image.get_rect()
        self.rect = self.defult_rect
        self.defult_rect.centerx = x 
        self.defult_rect.centery = y 
        self.hover_rect.centerx = x 
        self.hover_rect.centery = y 
        self.defulty = self.rect.centery
    def draw(self, scroll_amount):
        self.rect.centery = self.defulty - scroll_amount
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        #check mouse over and click conditions
        if self.rect.collidepoint(pos):
            self.image = self.hover_image
            self.rect = self.hover_rect
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        else:
            self.image = self.defult_image
            self.rect = self.defult_rect
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        #draw button
        screen.blit(self.image, self.rect)
        screen.blit(self.txt_surface, (self.rect.centerx - (self.text_width / 2), self.rect.centery - 15))
        return action
    def reset_rect(self):
        self.rect = self.defult_rect

class Select_World():
    def __init__(self):
        self.selector_img = pygame.image.load('game_files/imgs/gui/world_selector_box.png')
        self.selected_img = pygame.image.load('game_files/imgs/gui/world_selected.png')
        self.world_num = 0
        self.world_select_bg = pygame.image.load('game_files/imgs/gui/world_selection_bg.png')
        #self.world_select_bg = pygame.transform.scale(world_select_bg, (tile_size * 29, tile_size * 20))
        self.world_select_bg_rect = self.world_select_bg.get_rect()
        self.world_select_bg_rect.centerx = 300
        self.world_select_bg_rect.centery = 300
        self.world_1_rect = self.selector_img.get_rect()
        self.world_1_rect.centerx = 300
        self.world_1_rect.centery = self.world_select_bg_rect.centery - 128
        self.world_2_rect = self.selector_img.get_rect()
        self.world_2_rect.centerx = 300
        self.world_2_rect.centery = self.world_select_bg_rect.centery - 64
        self.world_3_rect = self.selector_img.get_rect()
        self.world_3_rect.centerx = 300
        self.world_3_rect.centery = self.world_select_bg_rect.centery + 64
        self.world_4_rect = self.selector_img.get_rect()
        self.world_4_rect.centerx = 300
        self.world_4_rect.centery = self.world_select_bg_rect.centery + 128
    def update(self):
        pos = pygame.mouse.get_pos()
        if self.world_1_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            if self.world_num == 1:
                self.world_num = 0
            else:
                self.world_num = 1
        elif self.world_2_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            if self.world_num == 2:
                self.world_num = 0
            else:
                self.world_num = 2
        elif self.world_3_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            if self.world_num == 3:
                self.world_num = 0
            else:
                self.world_num = 3
        elif self.world_4_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            if self.world_num == 4:
                self.world_num = 0
            else:
                self.world_num = 4
        screen.blit(self.world_select_bg, (self.world_select_bg_rect.x, self.world_select_bg_rect.y))
        screen.blit(self.selector_img, (self.world_1_rect.x, self.world_1_rect.y))
        screen.blit(self.selector_img, (self.world_2_rect.x, self.world_2_rect.y))
        screen.blit(self.selector_img, (self.world_3_rect.x, self.world_3_rect.y))
        screen.blit(self.selector_img, (self.world_4_rect.x, self.world_4_rect.y))
        if self.world_num == 1:
            screen.blit(self.selected_img, (self.world_1_rect.x, self.world_1_rect.y))
        elif self.world_num == 2:
            screen.blit(self.selected_img, (self.world_2_rect.x, self.world_2_rect.y))
        elif self.world_num == 3:
            screen.blit(self.selected_img, (self.world_3_rect.x, self.world_3_rect.y))
        elif self.world_num == 4:
            screen.blit(self.selected_img, (self.world_4_rect.x, self.world_4_rect.y))
        return self.world_num

class Scroll_Bar():
    def __init__(self, length, scroll_multiplier):
        image_unpressed = pygame.image.load('game_files/imgs/menu/scroll_bar.png')
        image_pressed = pygame.image.load('game_files/imgs/menu/scroll_bar_pressed.png')
        self.image_unpressed = pygame.transform.scale(image_unpressed, (tile_size * 1, tile_size * length))
        self.image_pressed = pygame.transform.scale(image_pressed, (tile_size * 1, tile_size * length))
        self.image = image_unpressed
        self.rect = self.image_unpressed.get_rect()
        self.rect.x = 600 - self.rect.width
        self.rect.y = 0
        self.scroll_wheel = 0
        self.scroll_count = 0
        self.clicked = False
        self.scroll_distence = 0
        self.scroll_multiplier = scroll_multiplier
    def get_scroll_wheel(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_wheel = event.y
        if event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False
    def update(self):
        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 1 and self.rect.collidepoint(pos):
            self.clicked = True
        if self.clicked == True:
            self.image = self.image_pressed
            self.rect.centery = pos[1]
        else:
            self.image = self.image_unpressed     
        self.rect.centery += (-5 * scroll_sensitivity) * self.scroll_wheel
        if self.scroll_count <= 5:
            self.scroll_count += 1
        else:
            self.scroll_count = 0
            self.scroll_wheel = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600
        elif self.rect.top < 0:
            self.rect.top = 0
        screen.blit(self.image, self.rect)
        self.scroll_distence = self.rect.top
        return self.scroll_distence * self.scroll_multiplier
class Slider():
    def __init__(self, x, y, length, knob_ratio, amount):
        self.length = int(length)
        slider_knob_img = pygame.image.load('game_files/imgs/menu/slider_knob.png')
        self.knob_img = pygame.transform.scale(slider_knob_img, (tile_size *2.5, tile_size * 2.5))
        slider_centre_img = pygame.image.load('game_files/imgs/menu/slider_centre.png')
        self.slider_centre_img = pygame.transform.scale(slider_centre_img, (tile_size *2, tile_size * 2))
        slider_left_img = pygame.image.load('game_files/imgs/menu/slider_end.png')
        self.slider_left_img = pygame.transform.scale(slider_left_img, (tile_size *2, tile_size * 2))
        self.slider_right_img = pygame.transform.flip(self.slider_left_img, 180, 0)
        self.rect = pygame.Rect(x, y, (tile_size * 2 * length), (tile_size * 2))
        self.knob_rect = self.knob_img.get_rect()
        self.knob_rect.centery = self.rect.centery
        self.knob_rect.centerx = self.rect.x + (knob_ratio * self.rect.width)
        self.defulty = self.rect.centery
        self.clicked = False
        self.distance = abs((self.rect.x) - self.knob_rect.centerx) 
        self.slider_amount = 0
        self.amount = amount
        self.ratio = knob_ratio
    def get_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False
    def update(self, scroll_amount):
        pos = pygame.mouse.get_pos()
        self.rect.y = self.defulty - scroll_amount
        self.knob_rect.centery = self.rect.centery
        screen.blit(self.slider_left_img, (self.rect.left, self.rect.y))
        screen.blit(self.slider_right_img, (self.rect.right - (tile_size * 2), self.rect.y))
        for num in range(1, self.length - 1):
            screen.blit(self.slider_centre_img, (self.rect.left + (tile_size * 2 * num), self.rect.y))
        if pygame.mouse.get_pressed()[0] == 1 and self.knob_rect.collidepoint(pos):
            self.clicked = True
        if self.clicked == True:
            self.knob_rect.centerx = pos[0]
        if self.knob_rect.centerx > self.rect.right:
            self.knob_rect.centerx = self.rect.right
        elif self.knob_rect.centerx < self.rect.left:
            self.knob_rect.centerx = self.rect.left
        screen.blit(self.knob_img, (self.knob_rect.x, self.knob_rect.y))
        self.distance = abs((self.rect.x) - self.knob_rect.centerx)
        self.ratio = self.distance / self.rect.width
        self.slider_amount = self.amount * self.ratio
        return self.slider_amount
class Select_Charachter():
    def __init__(self):
        #load player images
        defult_one = pygame.image.load('game_files/imgs/player/defult_one_spritesheet.png')
        self.player_1 = pygame.transform.scale(defult_one, (defult_one.get_width() * 2, defult_one.get_height() * 2))
        with Image.open('game_files/imgs/player/defult_one_spritesheet.png') as image:
            #open not load b/c the defults need to be copied, not edited
            self.pillow_male = image.copy()
        defult_two = pygame.image.load('game_files/imgs/player/defult_two_spritesheet.png')
        self.player_2 = pygame.transform.scale(defult_two, (defult_two.get_width() * 2, defult_two.get_height() * 2))
        with Image.open('game_files/imgs/player/defult_two_spritesheet.png') as image:
            #open not load b/c the defults need to be copied, not edited
            self.pillow_female = image.copy()
        custom_one = pygame.image.load('game_files/imgs/player/custom_one.png')
        self.player_3 = pygame.transform.scale(custom_one, (defult_one.get_width() * 2, defult_one.get_height() * 2))
        with Image.open('game_files/imgs/player/custom_one.png') as image:
            self.pillow_1 = image.copy()
        custom_two = pygame.image.load('game_files/imgs/player/custom_two.png')
        self.player_4 = pygame.transform.scale(defult_two, (custom_two.get_width() * 2, defult_two.get_height() * 2))
        with Image.open('game_files/imgs/player/custom_two.png') as image:
            self.pillow_2 = image.copy()   
        custom_three = pygame.image.load('game_files/imgs/player/custom_three.png')
        self.player_5 = pygame.transform.scale(defult_two, (custom_three.get_width() * 2, defult_two.get_height() * 2))
        with Image.open('game_files/imgs/player/custom_three.png') as image:
            self.pillow_3 = image.copy()
        self.current_player = current_player
        self.player_size = [int(player.rect.width), int(player.rect.height)]
        #open player genders
        with open('game_files/settings/player_genders.json', 'r') as genders_file:
            genders = json.load(genders_file)
        #add player images to dictionary
        self.player_images = {
                            1: {
                                1: pygame.transform.scale(defult_one, (defult_one.get_width() * 2, defult_one.get_height() * 2)),
                                2: pygame.transform.scale(defult_one, (defult_one.get_width() * 4, defult_one.get_height() * 4)),
                                3: pygame.transform.scale(defult_one, (defult_one.get_width() * 6, defult_one.get_height() * 6)),
                                'g': 'm',
                                },
                            2: {
                                1: pygame.transform.scale(defult_two, (defult_two.get_width() * 2, defult_two.get_height() * 2)),
                                2: pygame.transform.scale(defult_two, (defult_two.get_width() * 4, defult_two.get_height() * 4)),
                                3: pygame.transform.scale(defult_two, (defult_two.get_width() * 6, defult_two.get_height() * 6)),
                                'g': 'f',
                                },
                            3: {
                                1: pygame.transform.scale(custom_one, (custom_one.get_width() * 2, custom_one.get_height() * 2)),
                                2: pygame.transform.scale(custom_one, (custom_one.get_width() * 4, custom_one.get_height() * 4)),
                                3: pygame.transform.scale(custom_one, (custom_one.get_width() * 6, custom_one.get_height() * 6)),
                                'g':genders['1'],
                                },
                            4: {
                                1: pygame.transform.scale(custom_two, (custom_two.get_width() * 2, custom_two.get_height() * 2)),
                                2: pygame.transform.scale(custom_two, (custom_two.get_width() * 4, custom_two.get_height() * 4)),
                                3: pygame.transform.scale(custom_two, (custom_two.get_width() * 6, custom_two.get_height() * 6)),
                                'g':genders['2'],
                                },
                            5: {
                                1: pygame.transform.scale(custom_three, (custom_three.get_width() * 2, custom_three.get_height() * 2)),
                                2: pygame.transform.scale(custom_three, (custom_three.get_width() * 4, custom_three.get_height() * 4)),
                                3: pygame.transform.scale(custom_three, (custom_three.get_width() * 6, custom_three.get_height() * 6)),
                                'g':genders['3'],
                                },
                            }
        #load image templates
        with Image.open('game_files/imgs/player/player_template_female.png', 'r') as female_template:
            self.female_data = numpy.array(female_template)
        with Image.open('game_files/imgs/player/player_template_male.png', 'r') as male_template:
            self.male_data = numpy.array(male_template)
        #set up different rects for panel
        self.centre_rect = pygame.rect.Rect(0, 0, self.player_size[0] * 3, self.player_size[1] * 3)
        self.centre_rect.centerx = 300
        self.centre_rect.centery = 300
        self.left_one = pygame.rect.Rect(0, 0, self.player_size[0] * 2, self.player_size[1] * 2)
        self.left_one.centerx = self.centre_rect.centerx - 100
        self.left_one.centery = self.centre_rect.centery
        self.right_one = pygame.rect.Rect(0, 0, self.player_size[0] * 2, self.player_size[1] * 2)
        self.right_one.centerx = self.centre_rect.centerx + 100
        self.right_one.centery = self.centre_rect.centery
        self.left_two = pygame.rect.Rect(0, 0, self.player_size[0] * 1, self.player_size[1] * 1)
        self.left_two.centerx = self.left_one.centerx - 60
        self.left_two.centery = self.left_one.centery
        self.right_two = pygame.rect.Rect(0, 0, self.player_size[0] * 1, self.player_size[1] * 1)
        self.right_two.centerx = self.right_one.centerx + 60
        self.right_two.centery = self.right_one.centery
        self.edit_rect = self.centre_rect.copy()
        self.edit_rect.centerx = 375
        self.edit_rect.centery = 250
        #set up arrows
        arrow = pygame.image.load('game_files/imgs/gui/charachter_select_arrow.png')
        self.arrow_left = pygame.transform.scale(arrow, (arrow.get_width() * 2, arrow.get_height() * 2))
        self.arrow_right = pygame.transform.flip(self.arrow_left, True, False)
        self.arrow_left_rect = self.arrow_left.get_rect()
        self.arrow_left_rect.centerx = 300 - 80
        self.arrow_left_rect.centery = 450
        self.arrow_right_rect = self.arrow_right.get_rect()
        self.arrow_right_rect.centerx = 300 + 80
        self.arrow_right_rect.centery = 450
        self.time_since_last_press = 0
        self.colour_picker = pygame.surface.Surface((120, 120))
        self.colour_picker_rect = self.colour_picker.get_rect()
        self.colour_picker_rect.centerx = 200
        self.colour_picker_rect.centery = 450
        self.hue_gradient_surface = pygame.surface.Surface((self.colour_picker.get_width() / 8, self.colour_picker.get_height()))
        self.hue_rect = self.hue_gradient_surface.get_rect()
        self.hue_rect.x = self.colour_picker_rect.right + 20
        self.hue_rect.y = self.colour_picker_rect.y
        self.make_vert_gradient()
        self.circle_chooser = pygame.rect.Rect(0, 0, 8, 8)
        self.hue_chooser = pygame.rect.Rect(0, 0, self.hue_gradient_surface.get_width() + 16, 10)
        self.hue_chooser.centerx = self.hue_rect.centerx
        self.choosing_hue = False
        arrow = pygame.image.load('game_files/imgs/gui/charachter_select_arrow.png')
        self.edit_arrow_left_rect = self.arrow_left.get_rect()
        self.edit_arrow_left_rect.centerx = self.edit_rect.left - 20
        self.edit_arrow_left_rect.centery = self.edit_rect.centery
        self.edit_arrow_right_rect = self.arrow_right.get_rect()
        self.edit_arrow_right_rect.centerx = self.edit_rect.right + 20
        self.edit_arrow_right_rect.centery = self.edit_rect.centery
        self.hors_frame = 0
        self.editing = None
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        #blit arrows
        screen.blit(self.arrow_right, self.arrow_right_rect)
        screen.blit(self.arrow_left, self.arrow_left_rect)
        #change selected based on arow presses
        if self.arrow_left_rect.collidepoint(mouse_pos):
            #check if the mouse has been clicked
            if pygame.mouse.get_pressed()[0]:
                #wait time so there actully is control over the movment
                if time.time() - self.time_since_last_press > 0.5:
                    if self.current_player == len(self.player_images):
                        self.current_player = 1
                    else:
                        self.current_player += 1
                    self.time_since_last_press = time.time()
        if self.arrow_right_rect.collidepoint(mouse_pos):
            #check if the mouse has been clicked
            if pygame.mouse.get_pressed()[0]:
                #wait time so there actully is control over the movment
                if time.time() - self.time_since_last_press > 0.5:
                    if self.current_player == 1:
                        self.current_player = len(self.player_images)
                    else:
                        self.current_player -= 1
                    self.time_since_last_press = time.time()
        #draw selected player and box
        screen.blit(self.player_images[self.current_player][3], self.centre_rect, (0, 0, self.player_size[0] * 3, self.player_size[1] * 3))
        pygame.draw.rect(screen, (255, 255, 255), self.centre_rect, 4)
        #this allows for less players if I want to in the future. Also I already had refrence code in the Point N' CLick Project to do the carousell like this
        #each number of players plus has its own if statement to blit left or right
        if len(self.player_images) >= 2:
            if self.current_player - 1 <= 0:
                #blit last image if it is one
                screen.blit(self.player_images[list(self.player_images.keys())[-1]][2], self.left_one, (0, 0, self.player_size[0] * 2, self.player_size[1] * 2))
            else:
                screen.blit(self.player_images[self.current_player - 1][2], self.left_one, (0, 0, self.player_size[0] * 2, self.player_size[1] * 2))
            pygame.draw.rect(screen, (50, 50, 50), self.left_one, 3)
        if len(self.player_images) >= 3:
            if self.current_player + 1 > len(self.player_images):
                #blit last image if it is one
                screen.blit(self.player_images[list(self.player_images.keys())[0]][2], self.right_one, (0, 0, self.player_size[0] * 2, self.player_size[1] * 2))
            else:
                screen.blit(self.player_images[self.current_player + 1][2], self.right_one, (0, 0, self.player_size[0] * 2, self.player_size[1] * 2))
            pygame.draw.rect(screen, (50, 50, 50), self.right_one, 3)
        if len(self.player_images) >= 4:
            if self.current_player - 2 <= 0 and self.current_player - 1 <= 0:
                #blit last image if it is one
                screen.blit(self.player_images[list(self.player_images.keys())[-2]][1], self.left_two, (0, 0, self.player_size[0], self.player_size[1]))
            elif self.current_player - 2 <= 0:
                screen.blit(self.player_images[list(self.player_images.keys())[-1]][1], self.left_two, (0, 0, self.player_size[0], self.player_size[1]))
            else:
                screen.blit(self.player_images[self.current_player -2][1], self.left_two, (0, 0, self.player_size[0], self.player_size[1]))
            pygame.draw.rect(screen, (50, 50, 50), self.left_two, 2)
        if len(self.player_images) >= 5:
            if self.current_player + 2 > len(self.player_images) and self.current_player + 1 > len(self.player_images):
                #blit last image if it is one
                screen.blit(self.player_images[list(self.player_images.keys())[1]][1], self.right_two, (0, 0, self.player_size[0], self.player_size[1]))
            elif self.current_player + 2 > len(self.player_images):
                screen.blit(self.player_images[list(self.player_images.keys())[0]][1], self.right_two, (0, 0, self.player_size[0], self.player_size[1]))
            else:
                screen.blit(self.player_images[self.current_player + 2][1], self.right_two, (0, 0, self.player_size[0], self.player_size[1]))
            pygame.draw.rect(screen, (50, 50, 50), self.right_two, 2) 
    def reset_inputs(self):
        h_input.ime_text = str(self.colour_picker_colour['hsv'][0])
        s_input.ime_text = str(self.colour_picker_colour['hsv'][1])
        v_input.ime_text = str(self.colour_picker_colour['hsv'][2])
        r_input.ime_text = str(self.colour_picker_colour['rgb'][0])
        g_input.ime_text = str(self.colour_picker_colour['rgb'][1])
        b_input.ime_text = str(self.colour_picker_colour['rgb'][2])
        hex_input.ime_text = str(self.colour_picker_colour['hex'])
    def save_genders(self):
        gender_data = {
                    '1': self.player_images[3]['g'],
                    '2': self.player_images[4]['g'],
                    '3': self.player_images[5]['g'],
                    }
        #save gender data to a file
        with open('game_files/settings/player_genders.json', "w") as file:
            json.dump(gender_data, file)
    def edit_setup(self):
        '''Get everything prepared to edit charachter'''
        match self.current_player:
            case 3:
                self.editor_img = self.pillow_1
            case 4:
                self.editor_img = self.pillow_2
            case 5:
                self.editor_img = self.pillow_3
        #get current colours
        self.set_attributes()
        #set up colour picker
        self.circle_chooser.right = self.colour_picker_rect.right 
        self.circle_chooser.top = self.colour_picker_rect.top 
        self.moving_circle = False
        self.hue_chooser.centery = self.hue_rect.y
        self.colour_picker_colour = {
                                    'rgb': [255, 0, 0],
                                    'hsv': [0, 1, 1],
                                    'hex': 'ff0000',
                                    }
        self.hors_frame = 0
        h_input.ime_text = str(self.colour_picker_colour['hsv'][0])
        s_input.ime_text = str(self.colour_picker_colour['hsv'][1])
        v_input.ime_text = str(self.colour_picker_colour['hsv'][2])
        r_input.ime_text = str(self.colour_picker_colour['rgb'][0])
        g_input.ime_text = str(self.colour_picker_colour['rgb'][1])
        b_input.ime_text = str(self.colour_picker_colour['rgb'][2])
        hex_input.ime_text = str(self.colour_picker_colour['hex'])
        self.editing = None
    def change_pos_on_input(self, colour_type, value, skip_edits=False):
        '''Changes position of slider & circle on input of colour value'''
        #don't do anything if the field contain nothing
        if value != '':
            #make non hex values bale to be worked with
            if colour_type != 'hex':
                try:
                    value = float(value)
                    value = int(value)
                except:
                    return
            #check what change is being inputted and change all other values accordingly
            match colour_type:
                case 'h':
                    self.colour_picker_colour['hsv'][0] = value
                    rgb = colorsys.hsv_to_rgb(self.colour_picker_colour['hsv'][0] / 360, self.colour_picker_colour['hsv'][1] / 100, self.colour_picker_colour['hsv'][2] / 100)
                    self.colour_picker_colour['rgb'] = [int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)]
                    self.colour_picker_colour['hex'] = "#{:02x}{:02x}{:02x}".format(self.colour_picker_colour['rgb'][0], self.colour_picker_colour['rgb'][1],self.colour_picker_colour['rgb'][2])
                case 's':
                    
                    self.colour_picker_colour['hsv'][1] = value
                    rgb = colorsys.hsv_to_rgb(self.colour_picker_colour['hsv'][0] / 360, self.colour_picker_colour['hsv'][1] / 100, self.colour_picker_colour['hsv'][2] / 100)
                    self.colour_picker_colour['rgb'] = [int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)]
                    self.colour_picker_colour['hex'] = "#{:02x}{:02x}{:02x}".format(self.colour_picker_colour['rgb'][0], self.colour_picker_colour['rgb'][1],self.colour_picker_colour['rgb'][2])
                case 'v':
                    self.colour_picker_colour['hsv'][2] = value
                    rgb = colorsys.hsv_to_rgb(self.colour_picker_colour['hsv'][0] / 360, self.colour_picker_colour['hsv'][1] / 100, self.colour_picker_colour['hsv'][2] / 100)
                    self.colour_picker_colour['rgb'] = [int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)]
                    self.colour_picker_colour['hex'] = "#{:02x}{:02x}{:02x}".format(self.colour_picker_colour['rgb'][0], self.colour_picker_colour['rgb'][1],self.colour_picker_colour['rgb'][2])
                case 'r':
                    self.colour_picker_colour['rgb'][0] = value
                    hsv = colorsys.rgb_to_hsv(self.colour_picker_colour['rgb'][0] / 255, self.colour_picker_colour['rgb'][1] / 255, self.colour_picker_colour['rgb'][2] / 255)
                    self.colour_picker_colour['hsv'] = [int(hsv[0] * 360), int(hsv[1] * 100), int(hsv[2] * 100)]
                    self.colour_picker_colour['hex'] = "#{:02x}{:02x}{:02x}".format(self.colour_picker_colour['rgb'][0], self.colour_picker_colour['rgb'][1],self.colour_picker_colour['rgb'][2])
                case 'g':
                    self.colour_picker_colour['rgb'][1] = value
                    hsv = colorsys.rgb_to_hsv(self.colour_picker_colour['rgb'][0] / 255, self.colour_picker_colour['rgb'][1] / 255, self.colour_picker_colour['rgb'][2] / 255)
                    self.colour_picker_colour['hsv'] = [int(hsv[0] * 360), int(hsv[1] * 100), int(hsv[2] * 100)]
                    self.colour_picker_colour['hex'] = "#{:02x}{:02x}{:02x}".format(self.colour_picker_colour['rgb'][0], self.colour_picker_colour['rgb'][1],self.colour_picker_colour['rgb'][2])
                case 'b':
                    self.colour_picker_colour['rgb'][2] = value
                    hsv = colorsys.rgb_to_hsv(self.colour_picker_colour['rgb'][0] / 255, self.colour_picker_colour['rgb'][1] / 255, self.colour_picker_colour['rgb'][2] / 255)
                    self.colour_picker_colour['hsv'] = [int(hsv[0] * 360), int(hsv[1] * 100), int(hsv[2] * 100)]
                    self.colour_picker_colour['hex'] = "#{:02x}{:02x}{:02x}".format(self.colour_picker_colour['rgb'][0], self.colour_picker_colour['rgb'][1],self.colour_picker_colour['rgb'][2])
                case 'hex':
                    self.colour_picker_colour['hex'] = value
                    #remove # if in before converting to rgb
                    rgb = self.colour_picker_colour['hex'].lstrip('#')
                    self.colour_picker_colour['rgb'] = tuple(int(rgb[i:i+2], 16) for i in (0, 2, 4))
                    hsv = colorsys.rgb_to_hsv(self.colour_picker_colour['rgb'][0] / 255, self.colour_picker_colour['rgb'][1] / 255, self.colour_picker_colour['rgb'][2] / 255)
                    self.colour_picker_colour['hsv'] = [int(hsv[0] * 360), int(hsv[1] * 100), int(hsv[2] * 100)]
            #change position of sliders
            #remember to re-normalise values to solve for position
            self.hue_chooser.centery = self.hue_rect.top + ((self.colour_picker_colour['hsv'][0] / 360) * self.hue_rect.height)
            self.circle_chooser.centerx =  self.colour_picker_rect.left + ((self.colour_picker_colour['hsv'][1] / 100) * (self.colour_picker_rect.width))
            self.circle_chooser.centery =  self.colour_picker_rect.top + ((1 - (self.colour_picker_colour['hsv'][2]) / 100) * (self.colour_picker_rect.height))
            #reset input boxes
            h_input.ime_text = str(self.colour_picker_colour['hsv'][0])
            s_input.ime_text = str(self.colour_picker_colour['hsv'][1])
            v_input.ime_text = str(self.colour_picker_colour['hsv'][2])
            r_input.ime_text = str(self.colour_picker_colour['rgb'][0])
            g_input.ime_text = str(self.colour_picker_colour['rgb'][1])
            b_input.ime_text = str(self.colour_picker_colour['rgb'][2])
            hex_input.ime_text = str(self.colour_picker_colour['hex'])
            #was bugging on changing when selecting a differnt button, this option fixed it. Don't know why
            #but suspect that changing r, then g, then b and ediitng image each time was the problem
            if skip_edits == False:
                #modify actual image
                self.make_edits()
    def edit(self):
        #make edits to actual image - this goes 1st because hue chooser couldn't be moved if it was last
        self.make_edits()
        pos = pygame.mouse.get_pos()
        #blit player image
        screen.blit(self.player_images[self.current_player][3], self.edit_rect, (self.player_size[0] * 3 * self.hors_frame, 0, self.player_size[0] * 3, self.player_size[1] * 3))
        #blit arrows for changing player  angle
        screen.blit(self.arrow_left, self.edit_arrow_left_rect)
        screen.blit(self.arrow_right, self.edit_arrow_right_rect)
        #change player angle if arrow is clicked
        if self.edit_arrow_left_rect.collidepoint(pos):
            #check if the mouse has been clicked
            if pygame.mouse.get_pressed()[0]:
                #wait time so there actully is control over the movment
                if time.time() - self.time_since_last_press > 0.5:
                    if self.hors_frame > 0:
                        self.hors_frame -= 1
                    else:
                        self.hors_frame = 3
                    self.time_since_last_press = time.time()
        elif self.edit_arrow_right_rect.collidepoint(pos):
            #check if the mouse has been clicked
            if pygame.mouse.get_pressed()[0]:
                #wait time so there actully is control over the movment
                if time.time() - self.time_since_last_press > 0.5:
                    if self.hors_frame < 3:
                        self.hors_frame += 1
                    else:
                        self.hors_frame = 0
                    self.time_since_last_press = time.time()
        #blit colour picker
        #convert hue to rgb for gradient
        current_hue = abs(self.hue_rect.top - self.hue_chooser.centery) / (self.hue_rect.height)
        gradient_colour = colorsys.hsv_to_rgb(current_hue, 1, 1)
        gradient_colour = (gradient_colour[0] * 255, gradient_colour[1] * 255, gradient_colour[2] * 255)
        #print(gradient_colour)
        self.colour_picker_gradient = self.gradient(self.colour_picker, gradient_colour)
        screen.blit(self.colour_picker, self.colour_picker_rect)
        pygame.surfarray.blit_array(self.colour_picker, self.colour_picker_gradient)
        screen.blit(self.hue_gradient_surface, self.hue_rect)
        pygame.surfarray.blit_array(self.hue_gradient_surface, self.hue_gradient)
        #draw picker circle
        pygame.draw.circle(screen, (0, 0, 0), (self.circle_chooser.centerx, self.circle_chooser.centery), 4)
        pygame.draw.circle(screen, (255, 255, 255), (self.circle_chooser.centerx, self.circle_chooser.centery), 2)
        #check if clicked on colour picker circle
        if self.circle_chooser.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                self.moving_circle = True
        #move colour picker circle
        if self.moving_circle == True:
            self.circle_chooser.centerx = pos[0]
            self.circle_chooser.centery = pos[1]
            #check if unclicked or moved outside the box
            if not pygame.mouse.get_pressed()[0]:
                self.moving_circle = False
            if not self.colour_picker_rect.colliderect(self.circle_chooser):
                self.moving_circle = False
                if self.circle_chooser.centerx < self.colour_picker_rect.left:
                    self.circle_chooser.centerx = self.colour_picker_rect.left + 3
                elif self.circle_chooser.centerx > self.colour_picker_rect.right:
                    self.circle_chooser.centerx = self.colour_picker_rect.right - 3
                if self.circle_chooser.centery < self.colour_picker_rect.top:
                    self.circle_chooser.centery = self.colour_picker_rect.top + 3
                elif self.circle_chooser.centery > self.colour_picker_rect.bottom:
                    self.circle_chooser.centery = self.colour_picker_rect.bottom - 3
        #draw picker triangles
        pygame.draw.polygon(screen, (255, 255, 255), ((self.hue_chooser.left, self.hue_chooser.top), (self.hue_chooser.left, self.hue_chooser.bottom), (self.hue_chooser.left + 10, self.hue_chooser.centery)))
        pygame.draw.polygon(screen, (255, 255, 255), ((self.hue_chooser.right, self.hue_chooser.top), (self.hue_chooser.right, self.hue_chooser.bottom), (self.hue_chooser.right - 10, self.hue_chooser.centery)))
        if self.hue_chooser.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                self.choosing_hue = True
        #move hue chooser arrows
        if self.choosing_hue == True:
            self.hue_chooser.centery = pos[1]
            #check if unclicked or moved outside the box
            if not pygame.mouse.get_pressed()[0]:
                self.choosing_hue = False
            if not self.hue_rect.colliderect(self.hue_chooser):
                self.choosing_hue = False
                if self.hue_chooser.centery < self.hue_rect.top:
                    self.hue_chooser.centery = self.hue_rect.top
                elif self.hue_chooser.centery > self.hue_rect.bottom:
                    self.hue_chooser.centery = self.hue_rect.bottom  
        #get current colour values
        hsv = (current_hue, (abs(self.colour_picker_rect.left - self.circle_chooser.centerx) / self.colour_picker_rect.width), 1 - abs(self.colour_picker_rect.top - self.circle_chooser.centery) / self.colour_picker_rect.height)
        rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
        rgb = [int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)]
        hsv = [int(hsv[0] * 360), int(hsv[1] * 100), int(hsv[2] * 100)]
        hexcode = "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])
        #perform changes only when required
        if hsv != self.colour_picker_colour['hsv']:
            self.colour_picker_colour['hsv'] = hsv
            self.colour_picker_colour['rgb'] = rgb
            self.colour_picker_colour['hex'] = hexcode
            #set input box numbers
            h_input.ime_text = str(hsv[0])
            s_input.ime_text = str(hsv[1])
            v_input.ime_text = str(hsv[2])
            r_input.ime_text = str(rgb[0])
            g_input.ime_text = str(rgb[1])
            b_input.ime_text = str(rgb[2])
            hex_input.ime_text = str(hexcode)

    def get_editing(self):
        return self.editing
    def set_editing(self, setting):
        #set editing location
        self.editing = setting
        #set sliders & inputs to match current colour
        self.change_pos_on_input('r', self.atributes[setting][0], True)
        self.change_pos_on_input('g', self.atributes[setting][1], True)
        self.change_pos_on_input('b', self.atributes[setting][2], True)
        self.make_edits()
    def set_attributes(self):
        '''I got fed up changing it in 2 places so atribute setting gets its own function'''
        #Note that the top pixel will be 0- all other pixels have to be 1 off
        self.atributes ={
                        'hair': self.editor_img.copy().load()[8, 7],
                        'skin': self.editor_img.copy().load()[8, 10],
                        'eyes': self.editor_img.copy().load()[6, 10],
                        'shirt': self.editor_img.copy().load()[8, 16],
                        'pants': self.editor_img.copy().load()[8, 21],
                        'shoes': self.editor_img.copy().load()[6, 26],
                        }
    def swap_genders(self):
        #check current gender
        if self.player_images[self.current_player]['g'] == 'm':
            #switch gender
            self.player_images[self.current_player]['g'] = 'f'
            #swap imgs
            self.player_images[self.current_player][1] = self.player_images[2][1].copy()
            self.player_images[self.current_player][2] = self.player_images[2][2].copy()
            self.player_images[self.current_player][3] = self.player_images[2][3].copy()
            #swap editing image
            female_image =  self.pillow_female.copy()
            match self.current_player:
                case 3:
                    self.pillow_1 = female_image
                    self.editor_img = self.pillow_1
                case 4:
                    self.pillow_2 = female_image
                    self.editor_img = self.pillow_2
                case 5:
                    self.pillow_3 = female_image
                    self.editor_img = self.pillow_3
        elif self.player_images[self.current_player]['g'] == 'f':
            #switch gender
            self.player_images[self.current_player]['g'] = 'm'
            #swap imgs
            self.player_images[self.current_player][1] = self.player_images[1][1].copy()
            self.player_images[self.current_player][2] = self.player_images[1][2].copy()
            self.player_images[self.current_player][3] = self.player_images[1][3].copy()
            #swap editing image
            male_image =  self.pillow_male.copy()
            match self.current_player:
                case 3:
                    self.pillow_1 = male_image
                    self.editor_img = self.pillow_1
                case 4:
                    self.pillow_2 = male_image
                    self.editor_img = self.pillow_2
                case 5:
                    self.pillow_3 = male_image
                    self.editor_img = self.pillow_3
        #reset editing buttons
        self.editing = None
        #reset attibutes
        self.set_attributes()
    def gradient(self, surf, colour):
        '''Creates Box Gradient'''
        #convert colours to numpy arrays
        top_left_colour = numpy.asarray((255, 255, 255))
        top_right_colour = numpy.asarray(colour)
        bottom_colour = numpy.asarray((0, 0, 0))
        #get width and height of box
        width, height = surf.get_size()
        # Vertical gradient for top and bottom rows
        left_column = numpy.linspace(top_left_colour, bottom_colour, num=width)
        right_column = numpy.linspace(top_right_colour, bottom_colour, num=width)
        # Horizontal gradient between top and bottom rows
        gradient = numpy.linspace(left_column, right_column, num=height).astype("uint8")
        #return surface
        return pygame.surfarray.map_array(surf, gradient)
    def make_vert_gradient(self):
        '''Creates Vertical Hue Gradient. Height must be a multiple of 6'''
        column_height = self.hue_gradient_surface.get_height()
        single_gradient_height = int(column_height / 6)
        #define the colours
        colour_one = numpy.asarray((255, 0, 0))
        colour_two = numpy.asarray((255, 255, 0))
        colour_three = numpy.asarray((0, 255, 0))
        colour_four = numpy.asarray((0, 255, 255))
        colour_five = numpy.asarray((0, 0, 255))
        colour_six = numpy.asarray((255, 0, 255))
        colour_seven = numpy.asarray((255, 0, 0))
        #make gradients
        gradient_one = numpy.linspace(colour_one, colour_two, num=single_gradient_height)
        gradient_two = numpy.linspace(colour_two, colour_three, num=single_gradient_height)
        gradient_three = numpy.linspace(colour_three, colour_four, num=single_gradient_height)
        gradient_four = numpy.linspace(colour_four, colour_five, num=single_gradient_height)
        gradient_five = numpy.linspace(colour_five, colour_six, num=single_gradient_height)
        gradient_six = numpy.linspace(colour_six, colour_seven, num=single_gradient_height)
        #combined all gradients into 1 
        gradient = numpy.vstack((gradient_one, gradient_two, gradient_three, gradient_four, gradient_five, gradient_six)).astype("uint8")[numpy.newaxis, :, :]
        self.hue_gradient = gradient
    def make_edits(self):
        '''This function actully makes the edits to the charachter'''
        #get rgb values for the locations. 1st is regular, 2nd is shading 
        match self.editing:
            case 'hair':
                rgb_values = [(17, 149, 18, 255), (17, 136, 17, 255)]
            case 'skin':
                #rgb_values = [(28, 215, 30, 255), (146, 17, 13, 255)]
                rgb_values = [(201, 25, 20, 255), (146, 17, 13, 255)]
            case 'eyes':
                #rgb_values = [(201, 25, 20, 255), (30, 119, 30, 255)]
                rgb_values = [(28, 215, 30, 255), (30, 119, 30, 255)]
            case 'shirt':
                rgb_values = [(208, 158, 0, 255), (190, 145, 0, 255)]
            case 'pants':
                rgb_values = [(127, 127, 127, 255), (104, 104, 103, 255)]
            case 'shoes':
                rgb_values = [(25, 154, 206, 255), (19, 114, 152, 255)]
            case _:
                #error handling- just stop if no case matches
                return
        #get pixels values depending on male/female
        if self.player_images[self.current_player]['g'] == 'm':
            #find all pixels with main colours. -1 axis rabs last axis, which is the rgb value
            main_pixels = numpy.all(self.male_data == rgb_values[0], axis=-1)
            #find all pixels with shading colours. -1 axis rabs last axis, which is the rgb value
            shading_pixels = numpy.all(self.male_data == rgb_values[1], axis=-1)
        elif self.player_images[self.current_player]['g'] == 'f':
            #find all pixels with main colours. -1 axis rabs last axis, which is the rgb value
            main_pixels = numpy.all(self.female_data == rgb_values[0], axis=-1)
            #find all pixels with shading colours. -1 axis rabs last axis, which is the rgb value
            shading_pixels = numpy.all(self.female_data == rgb_values[1], axis=-1)
        #convert player image to numpy array to make it easier to modify pixels
        pixel_array = numpy.array(self.editor_img)
        #create shadow colour by converting to hsv to only decrease saturation
        shadow_hsv = self.colour_picker_colour['hsv']
        #chack if value is big enough to be subtracted from
        if shadow_hsv[2] > 10:
            shadow_hsv[2] -= 15
        else:
            shadow_hsv[2] = 0
        if shadow_hsv[0] > 4:
            shadow_hsv[0] -= 5
        else:
            shadow_hsv[0] = 0
        #convert shadow hsv to rgb so it can be used
        normalised_rgb_shadow = colorsys.hsv_to_rgb(shadow_hsv[0] / 360, shadow_hsv[1] / 100, shadow_hsv[2] / 100)
        rgb_shadow = (normalised_rgb_shadow[0] * 255, normalised_rgb_shadow[1] * 255, normalised_rgb_shadow[2] * 255, 255)
        #use masks created before to quickly modify image
        pixel_array[main_pixels] = (self.colour_picker_colour['rgb'][0], self.colour_picker_colour['rgb'][1], self.colour_picker_colour['rgb'][2], 255)
        #shading uses darker colour
        pixel_array[shading_pixels] = rgb_shadow
        #convert back to PIl image
        new_image = Image.fromarray(pixel_array)
        self.editor_img = new_image
        #change saved PIl image
        match self.current_player:
            case 3:
                self.pillow_1 = self.editor_img
            case 4:
                self.pillow_2 = self.editor_img
            case 5:
                self.pillow_3 = self.editor_img
        new_img_data = self.editor_img.tobytes()
        new_pygame_img = pygame.image.frombytes(new_img_data, new_image.size, new_image.mode)
        #change all images
        self.player_images[self.current_player][1] = pygame.transform.scale(new_pygame_img, (new_pygame_img.get_width() * 2, new_pygame_img.get_height() * 2))
        self.player_images[self.current_player][2] = pygame.transform.scale(new_pygame_img, (new_pygame_img.get_width() * 4, new_pygame_img.get_height() * 4))
        self.player_images[self.current_player][3] = pygame.transform.scale(new_pygame_img, (new_pygame_img.get_width() * 6, new_pygame_img.get_height() * 6))
        #change saved atributes
        self.set_attributes()
    def save_players(self):
        #save all saveable players
        self.pillow_1.save('game_files/imgs/player/custom_one.png')
        self.pillow_2.save('game_files/imgs/player/custom_two.png')
        self.pillow_3.save('game_files/imgs/player/custom_three.png')
#this class runs setting keybinds
class Keybinds():
    def __init__(self):
        button_img = pygame.image.load('game_files/imgs/menu/keybinds_button.png')
        self.button_image = pygame.transform.scale(button_img, (74, 32))
        self.button_rect = self.button_image.get_rect()
        #define switching buttons
        self.buttons = {
                    'forward': {
                            },
                    'backward': {
                            },
                    'left': {
                            },
                    'right': {
                            },
                    'run': {
                            },
                    'break block/attack': {
                            },
                    'inventory': {
                            },
                    'pause': {
                            },
                    'hotbar_1': {
                            },
                    'hotbar_2': {
                            },
                    'hotbar_3': {
                            },
                    'hotbar_4': {
                            },
                    'hotbar_5': {
                            },
                    }
        self.keybinds = {
                    'forward': '',
                    'backward': '',
                    'left': '',
                    'right': '',
                    'run': '',
                    'break block/attack': '',
                    'inventory': '',
                    'pause': '',
                    'hotbar_1': '',
                    'hotbar_2': '',
                    'hotbar_3': '',
                    'hotbar_4': '',
                    'hotbar_5': '',
                    }
        #load current keybinds
        with open('game_files/settings/keybinds.json', 'r') as keybinds:
            keybinds = json.load(keybinds)
        #load defult keybinds
        with open('game_files/settings/defult_keybinds.json', 'r') as defult_keybinds:
            self.defult_keybinds = json.load(defult_keybinds)
        #set button and reset button rects
        count = 0
        for button in self.buttons:
            self.buttons[button]['text'] = 'None'
            button_rect = self.button_rect.copy()
            button_rect.centery = 60 + (40 * count)
            self.buttons[button]['button'] = button_rect
            button_rect.centerx = 400
            button_rect = self.button_rect.copy()
            button_rect.centery = 60 + (40 * count)
            button_rect.centerx = 500
            self.buttons[button]['reset'] = button_rect
            #set button current key
            self.buttons[button]['text'] = pygame.key.name(keybinds[button]).capitalize()
            self.keybinds[button] = keybinds[button]
            count += 1
        self.mouse_down = False
        self.selected_button = None
    def get_event(self, event):
        #check if mouse was clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_down = True
        #get key press
        if event.type == pygame.KEYDOWN:
            if self.selected_button != None:
                self.buttons[self.selected_button]['text'] = pygame.key.name(event.key).capitalize()
                self.keybinds[self.selected_button] = event.key
    def update(self):
        #get mouse pos
        mouse_pos = pygame.mouse.get_pos()
        #blit button images for  setting and reset
        for button_key in self.buttons:
            #blit buttons
            button = self.buttons[button_key]
            screen.blit(self.button_image, button['button'])
            screen.blit(self.button_image, button['reset'])
            #draw label text
            draw_text_freetype(button_key.capitalize() + ':', settings_font, 20, (0, 0, 0), 150, button['reset'].centery - 6)
            #draw reset button text
            draw_text_freetype('Reset', settings_font, 15, (0, 0, 0), 480, button['reset'].centery - 5)
            #check if button was pressed to select the box
            if self.selected_button != button_key:
                draw_text_freetype(button['text'], settings_font, 15, (0, 0, 0), 380, button['button'].centery - 5)
                if self.mouse_down == True:
                    if button['button'].collidepoint(mouse_pos):
                        self.selected_button = button_key
            else:
                draw_text_freetype('<' + button['text'] + '>', settings_font, 15, (0, 0, 0), 380, button['button'].centery - 5)
                #reset selection if no mouse button was clicked
                if self.mouse_down == True:
                    self.selected_button = None
            #check if reset button was pressed
            if self.mouse_down == True:
                if button['reset'].collidepoint(mouse_pos):
                    self.buttons[button_key]['text'] = pygame.key.name(self.defult_keybinds[button_key]).capitalize()
                    self.keybinds[button_key] = self.defult_keybinds[button_key]
        self.mouse_down = False
    def save_keybinds(self):
        with open('game_files/settings/keybinds.json', "w") as file:
            json.dump(self.keybinds, file)
    def get_keybinds(self):
        return self.keybinds
#this class runs settings selection buttons
class Select_Setting():
    def __init__(self):
        sprites = pygame.image.load('game_files/imgs/menu/settings_ribbons.png')
        self.sprites = pygame.transform.scale(sprites, (sprites.get_width() * 2, sprites.get_height() * 2))
        self.world_rect = pygame.rect.Rect(0, 0, 48 * 2, 25 * 2)
        self.world_rect.x = 10
        self.world_rect.y = 315
        self.controls_rect = self.world_rect.copy()
        self.controls_rect.x = 0
        self.controls_rect.y = 365
        self.audio_rect = self.world_rect.copy()
        self.audio_rect.x = 10
        self.audio_rect.y = 415
        self.graphics_rect = self.world_rect.copy()
        self.graphics_rect.x = 10
        self.graphics_rect.y = 465
        self.credits_rect = self.world_rect.copy()
        self.credits_rect.x = 10
        self.credits_rect.y = 515
        self.selected_setting = 'controls'
        self.back_rect = self.world_rect.copy()
        self.back_rect.x = 10
        self.back_rect.y = 25
        self.selected_setting = 'controls'
    def update(self, ingame):
        #get mouse pos
        mouse_pos = pygame.mouse.get_pos()
        #blit ribbons based on if that option is selected or not
        if ingame:
            if self.selected_setting != 'world':
                screen.blit(self.sprites, self.world_rect, (0, 25 * 5 * 2, 48 * 2, 25 * 2))
            else:
                screen.blit(self.sprites, self.world_rect, (0, 18 * 8 + 25 * 6 * 2, 48 * 2, 18 * 2))
        if self.selected_setting != 'controls':
            screen.blit(self.sprites, self.controls_rect, (0, 25 * 0 * 2, 48 * 2, 25 * 2))
        else:
            screen.blit(self.sprites, self.controls_rect, (0, 18 * 0 + 25 * 6 * 2, 48 * 2, 18 * 2))
        if self.selected_setting != 'audio':
            screen.blit(self.sprites, self.audio_rect, (0, 25 * 1 * 2, 48 * 2, 25 * 2))
        else:
            screen.blit(self.sprites, self.audio_rect, (0, 18 * 2 + 25 * 6 * 2, 48 * 2, 18 * 2))
        if self.selected_setting != 'graphics':
            screen.blit(self.sprites, self.graphics_rect, (0, 25 * 2 * 2, 48 * 2, 25 * 2))
        else:
            screen.blit(self.sprites, self.graphics_rect, (0, 18 * 4 + 25 * 6 * 2, 48 * 2, 18 * 2))
        if self.selected_setting != 'credits':
            screen.blit(self.sprites, self.credits_rect, (0, 25 * 3 * 2, 48 * 2, 25 * 2))
        else:
            screen.blit(self.sprites, self.credits_rect, (0, 18 * 6 + 25 * 6 * 2, 48 * 2, 18 * 2))
        screen.blit(self.sprites, self.back_rect, (0, 25 * 4 * 2, 48 * 2, 25 * 2))
        #draw text to ribbons
        draw_text_freetype('Back', settings_font, 18, (0, 0, 0), self.back_rect.x + 30, self.back_rect.y + 7)
        draw_text_freetype('Controls', settings_font, 18, (0, 0, 0), self.controls_rect.x + 18, self.controls_rect.y + 7)
        draw_text_freetype('Audio', settings_font, 18, (0, 0, 0), self.audio_rect.x + 30, self.audio_rect.y + 7)
        draw_text_freetype('Graphics', settings_font, 18, (0, 0, 0), self.graphics_rect.x + 12, self.graphics_rect.y + 7)
        draw_text_freetype('Credits', settings_font, 18, (0, 0, 0), self.credits_rect.x + 25, self.credits_rect.y + 7)
        if ingame:
            draw_text_freetype('World', settings_font, 18, (0, 0, 0), self.world_rect.x + 25, self.world_rect.y + 7)

        #check if button was pressed
        if pygame.mouse.get_pressed()[0] == 1:
            #check if a ribbon was clicked
            if self.controls_rect.collidepoint(mouse_pos):
                self.selected_setting = 'controls'
                self.reset_rects()
                #set own rect to selected position
                self.controls_rect.x = 0
                self.controls_rect.y += 18
            elif self.audio_rect.collidepoint(mouse_pos):
                self.selected_setting = 'audio'
                self.reset_rects()
                #set own rect to selected position
                self.audio_rect.x = 0
                self.audio_rect.y += 18
            elif self.graphics_rect.collidepoint(mouse_pos):
                self.selected_setting = 'graphics'
                self.reset_rects()
                #set own rect to selected position
                self.graphics_rect.x = 0
                self.graphics_rect.y += 18
            elif self.credits_rect.collidepoint(mouse_pos):
                self.selected_setting = 'credits'
                self.reset_rects()
                #set own rect to selected position
                self.credits_rect.x = 0
                self.credits_rect.y += 18
            elif self.back_rect.collidepoint(mouse_pos):
                #reset to be controls for next opening of settings
                self.selected_setting = 'controls'
                self.reset_rects()
                #set controls rect to selected position
                self.controls_rect.x = 0
                self.controls_rect.y += 18
                return 'back'
            elif ingame:
                if self.world_rect.collidepoint(mouse_pos):
                    self.selected_setting = 'world'
                    self.reset_rects()
                    #set own rect to selected position
                    self.world_rect.x = 0
                    self.world_rect.y += 18
        return self.selected_setting
    def reset_rects(self):
        #reset x coords to 10 
        self.credits_rect.x = 10
        self.graphics_rect.x = 10
        self.controls_rect.x = 10
        self.audio_rect.x = 10
        self.world_rect.x = 10
        #reset y coords based on what the selected ribbon is
        if self.selected_setting == 'controls':
            self.controls_rect.y -= 18
        elif self.selected_setting == 'audio':
            self.audio_rect.y -= 18
        elif self.selected_setting == 'graphics':
            self.graphics_rect.y -= 18
        elif self.selected_setting == 'credits':
            self.credits_rect.y -= 18
        elif self.selected_setting == 'world':
            self.world_rect.y -= 18
class License_Back():
    def __init__(self):
        sprites = pygame.image.load('game_files/imgs/menu/settings_ribbons.png')
        self.sprites = pygame.transform.scale(sprites, (sprites.get_width() * 2, sprites.get_height() * 2))
        self.rect = pygame.rect.Rect(0, 0, 48 * 2, 25 * 2)
        self.rect.x = 10
        self.rect.y = 25
        self.selected_setting = 'controls'
    def update(self):
        '''It was easier jsut make a new small class for this button than to hijack the button class'''
        #get mouse pos
        mouse_pos = pygame.mouse.get_pos()
        # blit and draw text to ribbon
        screen.blit(self.sprites, self.rect, (0, 25 * 4 * 2, 48 * 2, 25 * 2))
        draw_text_freetype('Back', settings_font, 18, (0, 0, 0), self.rect.x + 30, self.rect.y + 7)
        #check if button was pressed
        if pygame.mouse.get_pressed()[0] == 1:
            if self.rect.collidepoint(mouse_pos):
                return True
        return False
class Main():
    def __init__(self):
        self.game_state = 6
        self.world_seed = 482
        self.debug = False
        self.debug_menu = False
        self.settings_state = 1
        self.true_scroll = [0,0]
        self.world_num = 0
        self.delete_state = 0
        #create error image
        error_img = Image.new(mode='RGB', size=(16, 16), color = (0, 0, 0))
        error_img_draw = ImageDraw.Draw(error_img)
        error_img_draw.rectangle([(0, 0), (8, 8)], fill ="#800080", outline ="purple") 
        error_img_draw.rectangle([(8, 8), (8, 8)], fill ="#800080", outline ="purple") 
        error_img_data = error_img.tobytes()
        self.error_img = pygame.image.frombytes(error_img_data, error_img.size, error_img.mode)
    def load_image(self, path):
        '''Helper function to load images or replace with error image'''
        try:
            return pygame.image.load(path)
        except:
            return self.error_img
    def load_button_images(self):
        self.button_img = self.load_image('game_files/imgs/menu/button_img.png')
        self.button_img = self.load_image(self.button_img, (tile_size * 8, tile_size * 4))
        self.button_hover_img = pygame.transform.scale(self.button_img, (tile_size * 9, tile_size * 4.5))
        self.button_selected = self.load_image('game_files/imgs/menu/selected_button.png')
        self.button_selected = pygame.transform.scale(self.button_selected, (tile_size * 8, tile_size * 4))
        self.button_settings = self.load_image('game_files/imgs/menu/settings_button.png')
        self.button_settings = pygame.transform.scale(self.button_settings, (tile_size * 4, tile_size * 4))
        self.button_settings_hover = self.load_image('game_files/imgs/menu/settings_button_hover.png')
        self.button_settings_hover = pygame.transform.scale(self.button_settings_hover, (tile_size * 4, tile_size * 4))
        self.button_settings_game = self.load_image('game_files/imgs/menu/game_settings_button.png')
        self.button_settings_game = pygame.transform.scale(self.button_settings_game, (tile_size * 7.5, tile_size * 4))
        self.button_settings_selected = self.load_image('game_files/imgs/menu/game_settings_button_selected.png')
        self.button_settings_selected = pygame.transform.scale(self.button_settings_selected, (tile_size * 8, tile_size * 4))
        self.combined_inventory_button = self.load_image('game_files/imgs/menu/combined_stack_button.png')
        self.combined_inventory_button = pygame.transform.scale(self.combined_inventory_button, (tile_size * 3, tile_size * 3))
        self.combined_inventory_button_hover = self.load_image('game_files/imgs/menu/combined_stack_button_hover.png')
        self.combined_inventory_button_hover = pygame.transform.scale(self.combined_inventory_button_hover, (tile_size * 3, tile_size * 3))
        self.combined_inventory_button_click = self.load_image('game_files/imgs/menu/combined_stack_button_click.png')
        self.combined_inventory_button_click = pygame.transform.scale(self.combined_inventory_button_click, (tile_size * 3, tile_size * 3))
        self.switch_off = self.load_image('game_files/imgs/menu/switch_off.png')
        self.switch_off = pygame.transform.scale(self.switch_off, (tile_size * 5, tile_size * 2.5))
        self.switch_on = self.load_image('game_files/imgs/menu/switch_on.png')
        self.switch_on = pygame.transform.scale(self.switch_on, (tile_size * 5, tile_size * 2.5))
        self.charachter_button_img = self.load_image('game_files/imgs/menu/charachter_button.png')
        self.charachter_button_img = pygame.transform.scale(self.charachter_button_img, (tile_size * 6, tile_size * 3))
        self.charachter_button_hover = pygame.transform.scale(self.charachter_button_img, (tile_size * 8, tile_size * 4))
    def load_background_images(self):
        self.inventory_bg = self.load_image('game_files/imgs/gui/inventory_background.png')
        inventory_page = self.load_image('game_files/imgs/gui/inventory_page.png')
        self.inventory_page_left = inventory_page
        self.inventory_page_right = pygame.transform.flip(inventory_page, True, False)
        self.respawn_bg = self.load_image('game_files/imgs/gui/respawn_bg.png')
        world_select_bg = self.load_image('game_files/imgs/gui/world_selection_bg.png')
        self.world_select_bg = pygame.transform.scale(world_select_bg, (tile_size * 29, tile_size * 20))
        self.settings_bg = self.load_image('game_files/imgs/menu/settings_bg.png')
        player_select_bg = self.load_image('game_files/imgs/gui/scroll_bg.png')
        self.player_select_bg = pygame.transform.scale(player_select_bg, (600, 600))
    def load_misc_images(self):
        self.ground_tiles_img = self.load_image('game_files/imgs/tiles/tiles_background.png')
        interactable_tiles_img = self.load_image('game_files/imgs/tiles/tiles_interactable.png')
        self.interactable_tiles_img = pygame.transform.scale(interactable_tiles_img, (interactable_tiles_img.get_width() * 2, interactable_tiles_img.get_height() * 2))
        inventory_slots = self.load_image('game_files/imgs/gui/inventory_slots.png')
        self.inventory_slots = pygame.transform.scale(inventory_slots, (tile_size * 3 * 7, tile_size * 3))
        self.icon_img = self.load_image('game_files/imgs/gui/cupcake_icon.png')
        self.keybinds_display = self.load_image('game_files/imgs/menu/keybinds_selector.png')
        logo = self.load_image('game_files/imgs/menu/logo.png')
        self.logo = pygame.transform.scale(logo, (555, 93))
        self.logo_rect = logo.get_rect()
        self.logo_rect.centerx = 300
        self.logo_rect.centery = 100
        #load images items
        item_imgs = pygame.image.load('game_files/imgs/items/item_spritesheet.png')
        self.item_imgs = pygame.transform.scale(item_imgs, (tile_size * 3 * 7, tile_size * 3 * 4))
    def load_settings(self):
        '''Load settings'''
        if path.exists('game_files/settings/settings.json'):
            with open('game_files/settings/settings.json', 'r') as settings_loaded:
                loaded_settings = json.load(settings_loaded)
                self.sfx = loaded_settings[0]
                self.music = loaded_settings[1]
                self.scroll_sense_ratio = loaded_settings[2]
                self.coords_on = loaded_settings[3]
                self.current_player = loaded_settings[4]
    def create_objects(self):
        '''Create all class objects for the game'''
        #set input boxes
        self.world_name_input = Input_Box(300, 180, 100, 30, colour_active, colour_inactive, 'centre')
        self.seed_input = Input_Box(300, 250, 100, 30, colour_active, colour_inactive, 'centre')
        self.world_name_change = Input_Box(300, 200, 100, 30, colour_active, colour_inactive, 'centre') 
        self.devtools_code = Input_Box(350, 1050, 100, 30, settings_bg_colour_active, settings_bg_colour, 'centre')
        self.h_input =  Input_Box(340, 390, 65, 30, colour_inactive, (0, 0, 0), 'centre', 3)
        self.s_input =  Input_Box(407, 390, 65, 30, colour_inactive, (0, 0, 0), 'centre', 3)
        self.v_input =  Input_Box(474, 390, 65, 30, colour_inactive, (0, 0, 0), 'centre', 3)
        self.r_input =  Input_Box(340, 440, 65, 30, colour_inactive, (0, 0, 0), 'centre', 3)
        self.g_input =  Input_Box(407, 440, 65, 30, colour_inactive, (0, 0, 0), 'centre', 3)
        self.b_input =  Input_Box(474, 440, 65, 30, colour_inactive, (0, 0, 0), 'centre', 3)
        self.hex_input =  Input_Box(372.5, 490, 130, 30, colour_inactive, (0, 0, 0), 'centre', 7)
        #set up classes
        self.inventory = Inventory()
        self.hotbar = Hotbar()
        self.player = Player(293, 315)
        self.select_world = Select_World()
        self.select_charachter = Select_Charachter()
        self.player.get_player_image()
        self.inventory.get_player_image()
        self.setting_selector = Select_Setting()
        self.set_keybinds = Keybinds()
        #get keybinds
        self.keybinds = self.set_keybinds.get_keybinds()
        #set buttons
        self.back_to_game = Button(300, 220, self.button_img, self.button_hover_img, "Back to game", white)
        self.ingame_settings_button = Button(300, 300, self.button_img, self.button_hover_img, "Settings", white)
        self.save_and_quit_button = Button(300, 380, self.button_img, self.button_hover_img, "Save and Quit", white)
        self.respawn_button = Button(300, 340, self.button_img, self.button_hover_img, "Respawn", white)
        self.save_and_quit_button_dead = Button(300, 260, self.button_img, self.button_hover_img, "Save and Quit", white)
        self.peaceful_button = Button(400, 350, self.button_img, self.button_hover_img, "Peaceful", white)
        self.hostile_button = Button(200, 350, self.button_img, self.button_hover_img, "Hostile", white)
        self.generate_world_button = Button(300, 450, self.button_img, self.button_hover_img, "Generate", white)
        self.play_button = Button(300, 220, self.button_img, self.button_hover_img, "Play", white)
        self.play_selected_button = Button(150, 550, self.button_img, self.button_hover_img, "Play", white)
        self.create_button = Button(450, 550, self.button_img, self.button_hover_img, "Create", white)
        self.select_back_button = Button(100, 50, self.button_img, self.button_hover_img, "Back", white)
        self.delete_world_button = Button(300, 450, self.button_img, self.button_hover_img, "Delete World", white)
        self.world_one_settings = Button(self.select_world.world_1_rect.right + 32, self.select_world.world_1_rect.centery, self.button_settings, self.button_settings_hover, "", white)
        self.world_two_settings = Button(self.select_world.world_2_rect.right + 32, self.select_world.world_2_rect.centery, self.button_settings, self.button_settings_hover, "", white)
        self.world_three_settings = Button(self.select_world.world_3_rect.right + 32, self.select_world.world_3_rect.centery, self.button_settings, self.button_settings_hover, "", white)
        self.world_four_settings = Button(self.select_world.world_4_rect.right + 32, self.select_world.world_4_rect.centery, self.button_settings, self.button_settings_hover, "", white)
        self.delete_yes_button = Button(400, 300, self.button_img, self.button_hover_img, "Yes", white)
        self.delete_no_button = Button(200, 300, self.button_img, self.button_hover_img, "No", white)
        self.settings_button = Button(300, 320, self.button_img, self.button_hover_img, "Settings", white)
        self.edit_player_button = Button(300, 420, self.button_img, self.button_hover_img, "Player", white)
        self.how_to_play_button = Button(300, 400, self.button_img, self.button_hover_img, "Quit", white)
        self.controls_button = Button(tile_size * 4, tile_size * 6, self.button_settings_game, self.button_settings_game, "Controls", white)
        self.audio_settings_button = Button(tile_size * 4, tile_size * 10, self.button_settings_game, self.button_settings_game, "Audio", white)
        self.back_settings_button = Button(tile_size * 4, tile_size * 2, self.button_settings_game, self.button_settings_game, "Back", white)
        self.graphics_settings_button = Button(tile_size * 4, tile_size * 14, self.button_settings_game, self.button_settings_game, "Graphics", white)
        self.credits_settings_button = Button(tile_size * 4, tile_size * 18, self.button_settings_game, self.button_settings_game, "Credits", white)
        self.sfx_on_button = Button(400, 100,self. switch_on, self.switch_on, "", white)
        self.sfx_off_button = Button(400, 100, self.switch_off, self.switch_off, "", white)
        self.music_on_button = Button(400, 200, self.switch_on, self.switch_on, "", white)
        self.music_off_button = Button(400, 200, self.switch_off, self.switch_off, "", white)
        self.back_settings_button_ingame = Button(tile_size * 4, tile_size * 2, self.button_settings_game, self.button_settings_game, "Back", white)
        self.world_settings_ingame = Button(tile_size * 4, tile_size * 6, self.button_settings_game, self.button_settings_game, "World", white)
        self.controls_button_ingame = Button(tile_size * 4, tile_size * 10, self.button_settings_game, self.button_settings_game, "Controls", white)
        self.audio_settings_button_ingame = Button(tile_size * 4, tile_size * 14, self.button_settings_game, self.button_settings_game, "Audio", white)
        self.hostile_button_ingame = Button(230, 180, self.button_img, self.button_hover_img, "Hostile", white)
        self.peaceful_button_ingame = Button(470, 180, self.button_img, self.button_hover_img, "Peaceful", white)
        self.graphics_settings_button_ingame = Button(tile_size * 4, tile_size * 18, self.button_settings_game, self.button_settings_game, "Graphics", white)
        self.coords_on_button = Button(420, 100, self.switch_on, self.switch_on, "", white)
        self.coords_off_button = Button(420, 100, self.switch_off, self.switch_off, "", white)
        self.done_charachter_button = Button(300, 500, self.charachter_button_img, self.charachter_button_hover, "Done", (0, 0, 0))
        self.edit_charachter_button = Button(300, 450, self.charachter_button_img, self.charachter_button_hover, "Edit", (0, 0, 0))
        self.back_charachter_button = Button(183, 80, self.charachter_button_img, self.charachter_button_hover, "Back", (0, 0, 0))
        self.charachter_hair_button = Button(183, 130, self.charachter_button_img, self.charachter_button_hover, "Hair", (0, 0, 0))
        self.charachter_eyes_button = Button(183, 172, self.charachter_button_img, self.charachter_button_hover, "Eyes", (0, 0, 0))
        self.charachter_skin_button = Button(183, 214, self.charachter_button_img, self.charachter_button_hover, "Skin", (0, 0, 0))
        self.charachter_shirt_button = Button(183, 256, self.charachter_button_img, self.charachter_button_hover, "Shirt", (0, 0, 0))
        self.charachter_pants_button = Button(183, 298, self.charachter_button_img, self.charachter_button_hover, "Pants", (0, 0, 0))
        self.charachter_shoes_button = Button(183, 340, self.charachter_button_img, self.harachter_button_hover, "Shoes", (0, 0, 0))
        self.swap_gender = Button(400, 80, self.charachter_button_img, self.charachter_button_hover, "Swap Gender", (0, 0, 0))
        self.license_back_button = License_Back()
        #view attribution buttons
        self.numpy_button =  Button(400, 160, self.button_img, self.button_hover_img, "View License", white)
        self.open_simplex_button =  Button(400, 220, self.button_img, self.button_hover_img, "View License", white)
        self.pillow_button =  Button(400, 280, self.button_img, self.button_hover_img, "View License", white)
        self.pyperclip_button =  Button(400, 340, self.button_img, self.button_hover_img, "View License", white)
        self.pygame_ce_button =  Button(400, 400, self.button_img, self.button_hover_img, "View License", white)
        self.medieval_sharp_button =  Button(400, 460, self.button_img, self.button_hover_img, "View License", white)
        self.DM_Serif_Text_button =  Button(400, 520, self.button_img, self.button_hover_img, "View License", white)
        #set scroll bars - max length 37
        self.controls_scroll_bar = Scroll_Bar(7, 1)
        self.devtools_controls_scroll_bar = Scroll_Bar(1, 1)
        self.audio_settings_scroll_bar = Scroll_Bar(37, 1)
        self.license_settings_scroll_bar = Scroll_Bar(0.5, 15)
        
        self.ingame = False
        
        #set sliders
        self.scroll_sense = Slider(200, 20, 8, self.scroll_sense_ratio, 2)
    def add_blit_item(self, item):
        '''Adds an item to linked list of all items to be blitted'''
        
    def game_loop(self):
        '''Main game loop function'''
        #start delta time
        dt = time.time()
        save_time = 0
        run = True
        while run == True:
            dt = time.time() - dt
            #fill interactable surface with transparent colour to clear it
            interactable_surface.fill((0, 0, 0, 0))
            #load and blit chunks
            if self.game_state == 1 or self.game_state == 0 or self.game_state == -1 or self.game_state == 2 or self.game_state == 3 or self.game_state == 6 or self.game_state == 7 or self.game_state == 8:
                self.true_scroll[0] += (self.player.rect.x - self.true_scroll[0] + (tile_size // 2) - 300) / 5
                self.true_scroll[1] += (self.player.rect.y - self.true_scroll[1] - (tile_size) - 300) / 5
                scroll = self.true_scroll.copy()
                scroll[0] = int(scroll[0])
                scroll[1] = int(scroll[1])
                #load chunks
                grass_rects = []
                water_rects = []
                current_chunks = []
                for y in range(7):
                    for x in range(7):
                        target_x = x - 1 + int(round(scroll[0] / (chunk_size * 16)))
                        target_y = y - 1 + int(round(scroll[1] / (chunk_size * 16))) 
                        target_chunk = str(target_x) + ':' + str(target_y)
                        if target_chunk not in self.game_map: #check if chunk exists
                            self.game_map[target_chunk] = generate_chunks(target_x, target_y, self.world_seed)
                        #current chunks is used to sagve time for entities droping items
                        current_chunks.append(target_chunk)
                        for tile in self.game_map[target_chunk]:
                            if tile[1] in [1]:
                                grass_rects.append([pygame.Rect(tile[0][0]*16-scroll[0],tile[0][1]*16-scroll[1],16,16), target_chunk, tile, tile[2]])
                                screen.blit(self.ground_tiles_img, (tile[0][0]*16-scroll[0],tile[0][1]*16-scroll[1]), (0, 0, 16, 16))
                            elif tile[1] in [2]:
                                water_rects.append([pygame.Rect(tile[0][0]*16-scroll[0],tile[0][1]*16-scroll[1],16,16), target_chunk, tile, tile[2]])
                                screen.blit(self.ground_tiles_img, (tile[0][0]*16-scroll[0],tile[0][1]*16-scroll[1]), (16, 0, 16, 16))
                            #update debug menu if enabled
                            if self.debug_menu == True and self.game_state == 0:
                                #check if center of self.player collides with tile to figure out what chunk they are in
                                if pygame.Rect(tile[0][0]*16-scroll[0],tile[0][1]*16-scroll[1],16,16).collidepoint((self.player.hitbox.centerx, self.player.hitbox.centery)):
                                   chunk_debug = target_chunk
                            #only run interactable/colelctble stuff if the object is a class
                            if tile[2] != None:
                                #move img rect based on scroll
                                if tile[1] in [1]:
                                    self.game_map[target_chunk][tile[2].chunk_location][2].rect.x = grass_rects[-1][0].x
                                    self.game_map[target_chunk][tile[2].chunk_location][2].rect.y =  grass_rects[-1][0].y
                                elif tile[1] in [2]:
                                    self.game_map[target_chunk][tile[2].chunk_location][2].rect.x = water_rects[-1][0].x
                                    self.game_map[target_chunk][tile[2].chunk_location][2].rect.y =  water_rects[-1][0].y
                                #blit img
                                interactable_surface.blit(self.interactable_tiles_img, tile[2].rect, tile[2].img_coords)
                                if self.debug == True:
                                    pygame.draw.rect(interactable_surface, (255, 255, 255), tile[2].rect, 2)
                                #check if tile is a collectable
                                if isinstance(tile[2], Collectable):
                                    #check if self.player collides with item
                                    if tile[2].rect.colliderect(self.player.hitbox):
                                        if self.inventory.collect_item(tile[2].item_num):
                                            self.game_map[tile[2].chunk][tile[2].chunk_location][2] = None
                                            self.hotbar.get_slot_data()
                        #blit interctables to the screen
                        screen.blit(interactable_surface, (0, 0))
            #show debug menu if enabled; seperated from setting above so it is blit above the interactables
            if self.debug_menu == True and self.game_state == 0:
                #show debug menu
                debug_menu_show(chunk_debug)
            for event in pygame.event.get():
                #handle_music(event, playlist, music)
                if event.type == pygame.QUIT:
                    run = False #if press x, end game loop
                if event.type == pygame.KEYDOWN:
                    if self.game_state == 0:
                        if event.key == self.keybinds['self.inventory']: 
                            self.game_state = 1
                        elif event.key == self.keybinds['pause']:
                            self.game_state = 2
                        if event.key == pygame.K_f:
                            self.debug = not self.debug
                        if event.key == pygame.K_TAB:
                            self.debug_menu = not self.debug_menu
                    elif self.game_state == 1:
                        if event.key == self.keybinds['self.inventory']:
                            self.hotbar.get_slot_data()
                            self.game_state = 0
                        elif event.key == self.keybinds['pause']:
                            self.hotbar.get_slot_data()
                            self.game_state = 2
                    elif self.game_state == 2:
                        if event.key == self.keybinds['pause']:
                            self.game_state = 0 
                if self.game_state == 0:
                    self.player.get_event(event)
                elif self.game_state == 1:
                    self.inventory.get_event(event)
                elif self.game_state == 3:
                    self.world_name_input.update(event)
                    self.seed_input.update(event)
                elif self.game_state == 8:
                    self.world_name_change.update(event)
                elif self.game_state == 9:
                    if self.settings_state == 'controls':
                        self.set_self.keybinds.get_event(event)
                elif self.game_state == 'edit_self.player':
                    self.h_input.update(event)
                    self.s_input.update(event)
                    self.v_input.update(event)
                    self.r_input.update(event)
                    self.g_input.update(event)
                    self.b_input.update(event)
                    self.hex_input.update(event)
                elif self.game_state == 'view_attributions':
                    self.license_settings_scroll_bar.get_scroll_wheel(event)
            #print self.player stuff
            if self.game_state == 0:
                #run entity stuff
                for projectile in game_engines.enitites.projectiles_to_pop:
                    #error handling
                    if projectile in game_engines.enitites.projectiles:
                        del game_engines.enitites.projectiles[projectile]
                game_engines.enitites.projectiles_to_pop = []
                for entity in game_engines.enitites.entitie_dict:
                    self.game_map = game_engines.enitites.entitie_dict[entity].update(self.player, scroll, self.debug, screen, water_rects, grass_rects, Collectable, self.game_map, entity_sfx, self.sfx)
                for projectile in game_engines.enitites.projectiles:
                    game_engines.enitites.projectiles[projectile].update(self.player, scroll, screen, self.debug)
                for entity in game_engines.enitites.entities_to_pop:
                    game_engines.enitites.entitie_dict.pop(entity)
                game_engines.enitites.entities_to_pop = []
                if self.player.dead == True:
                    self.game_state = -1
                self.player.update()
                self.hotbar.update()
                self.player.use_item(self.hotbar.hotbar_slots, self.hotbar.selector_slot)
                self.player.armour()
                self.player.health()
                game_engines.enitites.spawn_entities(world_difficulties, self.world_num, self.player)
                if self.coords_on == True:
                    draw_text(str(scroll), font, white, 10, 10)
                #save evry 5 minutes
                if time.time() - save_time == 5:
                    save_world(self.world_num, self.game_map, self.inventory.slots, self.player.hearts['health_count'], self.true_scroll, self.player.rect.x, self.player.rect.y, self.player.direction, game_engines.enitites.entitie_dict)
                    save_time = time.time()
                else:
                    self.play_selected_button += 1
            elif self.game_state == 1:
                screen.blit(self.inventory_bg, (0,0))
                self.inventory.update()
            elif self.game_state == -1:
                screen.blit(self.respawn_bg, (0,0))
                if self.respawn_button.draw(0):
                    self.player.respawn()
                    self.game_state = 0
                if self.save_and_quit_button_dead.draw(0):
                    save_world(self.world_num, self.game_map, self.inventory.slots, self.inventory.armour_slots, self.inventory.hotbar_slots, self.player.hearts['health_count'], self.true_scroll, self.player.rect.x, self.player.rect.y, self.player.direction, game_engines.enitites.entitie_dict)
                    self.world_seed = 0
                    game_map = {}
                    game_map_interactables = {}
                    true_scroll = [0, 0]
                    self.player.rect.x = 293
                    self.player.rect.y = 315
                    ingame = False
                    self.game_state = 7
            elif self.game_state == 2:
                screen.blit(self.inventory_bg, (0,0))
                if self.save_and_quit_button.draw(0):
                    save_world(self.world_num, game_map, self.inventory.slots, self.player.hearts['health_count'], true_scroll, self.player.rect.x, self.player.rect.y, self.player.direction, game_engines.enitites.entitie_dict)
                    self.world_seed = 37
                    self.game_map = {}
                    true_scroll = [0, 0]
                    self.player.rect.x = 293
                    self.player.rect.y = 315
                    ingame = False
                    self.game_state = 7
                if self.back_to_game.draw(0):
                    self.game_state = 0
                if self.ingame_self.settings_button.draw(0):
                    world_name_settings_ingame = world_names[self.world_num]
                    settings_difficulty_ingame = world_difficulties[self.world_num]
                    self.game_state = 9
            elif self.game_state == 3:
                if self.select_back_button.draw(0):
                    self.game_state = 7
                world_name_generating = self.world_name_input.draw(0)
                draw_text('World Name:', font, white, 210, 140)
                seed_generating = self.seed_input.draw(0)
                draw_text('Seed:', font, white, 210, 210)
                if self.creation_difficulty == 0:
                    screen.blit(self.button_selected, self.peaceful_button.rect)
                    screen.blit(self.peaceful_button.txt_surface, (self.peaceful_button.rect.centerx - (self.peaceful_button.text_width / 2), self.peaceful_button.rect.centery - 15))
                    if self.player.draw(0):
                        self.player.reset_rect()
                        creation_difficulty = 1
                elif creation_difficulty == 1:
                    screen.blit(self.button_selected, self.player.rect)
                    screen.blit(self.player.txt_surface, (self.player.rect.centerx - (self.player.text_width / 2), self.player.rect.centery - 15))
                    if self.peaceful_button.draw(0):
                        self.peaceful_button.reset_rect()
                        creation_difficulty = 0
                if self.generate_world_button.draw(0):
                    generating_world = True
                    self.world_name_input.ime_text = ''
                    self.seed_input.ime_text = ''
                    self.game_state = 4
            elif self.game_state == 4:
                #get random number if no string was inputed, otherwise run it through a fuction to ensure it  is useable
                if len(seed_generating) == 0:
                    seed_generating = random.randint(-10000000, 100000000)
                else:
                    seed_generating = string_to_float(seed_generating)
                generate_world(self.world_num, world_name_generating, seed_generating, creation_difficulty)
                temp_inventory = {}
                for num in range(0, 39):
                    temp_inventory[f'slot_{num}'] = {}
                    temp_inventory[f'slot_{num}']['item_data'] = None
                save_world(self.world_num, {}, temp_inventory, 20, [0,0], 293, 315, 2, game_engines.enitites.entitie_dict)
                self.game_state = 5
            elif self.game_state == 5:
                game_engines.enitites.entitie_dict = {}
                load_world(self.world_num)
                self.game_state = 0
                ingame = True
            elif self.game_state == 6:
                #print title screen
                screen.blit(self.logo, self.logo_rect)
                draw_text('Food Wars V1.2', font, white, 5, 570)
                if self.play_button.draw(0):
                    self.game_state = 7
                if self.settings_button.draw(0):
                    self.game_state = 9
                if self.edit_self.player_button.draw(0):
                    self.game_state = 'select_self.player'
            elif self.game_state == 7:
                self.world_num = self.select_world.update()
                if self.select_back_button.draw(0):
                    self.game_state = 6
                if self.world_num != 0 and world_generated[self.world_num] == True:
                    if self.play_selected_button.draw(0):
                        self.game_state = 5
                else:
                    screen.blit(self.button_selected, self.play_selected_button.rect)
                    draw_text(self.play_selected_button.text, font, white, (self.play_selected_button.rect.centerx - (self.play_selected_button.text_width / 2)), self.play_selected_button.rect.centery - 15)
        
                if self.world_num != 0 and world_generated[self.world_num] == False:
                    if self.create_button.draw(0):
                       self.game_state = 3
                else:
                    screen.blit(self.button_selected, self.create_button.rect)
                    draw_text(self.create_button.text, font, white, (self.create_button.rect.centerx - (self.create_button.text_width / 2)), self.create_button.rect.centery - 15)
                if self.world_one_settings.draw(0):
                    if world_generated[1] == True:
                        world_num = 1
                        self.game_state = 8
                        self.world_name_change.ime_text = world_names[world_num]
                        settings_difficulty = world_difficulties[world_num]
                if self.world_two_settings.draw(0):
                    if world_generated[2] == True:
                        world_num = 2
                        self.game_state = 8
                        self.world_name_change.ime_text = world_names[world_num]
                        settings_difficulty = world_difficulties[world_num]
                if self.world_three_settings.draw(0):
                    if world_generated[3] == True:
                        world_num = 3
                        self.game_state = 8
                        self.world_name_change.ime_text = world_names[world_num]
                        settings_difficulty = world_difficulties[world_num]
                if self.world_four_settings.draw(0):
                    if world_generated[4] == True:
                        world_num = 4
                        self.game_state = 8
                        self.world_name_change.ime_text = world_names[world_num]
                        settings_difficulty = world_difficulties[world_num]
                if world_generated[1] == True:
                    draw_text(world_names[1], font, white, self.select_world.world_1_rect.x + 70, self.select_world.world_1_rect.y)
                    if world_difficulties[1] == 0: 
                        draw_text('Peaceful', font_difficulty, white, self.select_world.world_1_rect.x + 70, self.select_world.world_1_rect.y + 35)
                    if world_difficulties[1] == 1: 
                        draw_text('Hostile', font_difficulty, white, self.select_world.world_1_rect.x + 70, self.select_world.world_1_rect.y + 35)
                else:
                    draw_text('World 1', font, white, self.select_world.world_1_rect.x + 70, self.select_world.world_1_rect.y)
                if world_generated[2] == True:
                    draw_text(world_names[2], font, white, self.select_world.world_2_rect.x + 70, self.select_world.world_2_rect.y)
                    if world_difficulties[2] == 0: 
                        draw_text('Peaceful', font_difficulty, white, self.select_world.world_2_rect.x + 70, self.select_world.world_2_rect.y + 35)
                    if world_difficulties[2] == 1: 
                        draw_text('Hostile', font_difficulty, white, self.select_world.world_2_rect.x + 70, self.select_world.world_2_rect.y + 35)
                else:
                    draw_text('World 2', font, white, self.select_world.world_2_rect.x + 70, self.select_world.world_2_rect.y)
                if world_generated[3] == True:
                    draw_text(world_names[3], font, white, self.select_world.world_3_rect.x + 70, self.select_world.world_3_rect.y)
                    if world_difficulties[3] == 0: 
                        draw_text('Peaceful', font_difficulty, white, self.select_world.world_3_rect.x + 70, self.select_world.world_3_rect.y + 35)
                    if world_difficulties[3] == 1: 
                        draw_text('Hostile', font_difficulty, white, self.select_world.world_3_rect.x + 70, self.select_world.world_3_rect.y + 35)
                else:
                    draw_text('World 3', font, white, self.select_world.world_3_rect.x + 70, self.select_world.world_3_rect.y)
                if world_generated[4] == True:
                    draw_text(world_names[4], font, white, self.select_world.world_4_rect.x + 70, self.select_world.world_4_rect.y)
                    if world_difficulties[4] == 0: 
                        draw_text('Peaceful', font_difficulty, white, self.select_world.world_4_rect.x + 70, self.select_world.world_4_rect.y + 35)
                    if world_difficulties[4] == 1: 
                        draw_text('Hostile', font_difficulty, white, self.select_world.world_4_rect.x + 70, self.select_world.world_4_rect.y + 35)
                else:
                   draw_text('World 4', font, white, self.select_world.world_4_rect.x + 70, self.select_world.world_4_rect.y)     
            elif self.game_state == 8:
                if self.delete_state == 0:
                    draw_text('Seed: '+ str(self.world_seeds[world_num]), font, white, 200, 250)     
                    world_name_settings = self.world_name_change.draw(0)
                    draw_text('World Name:', font, white, 235, 150)     
                    if settings_difficulty == 0:
                        screen.blit(self.button_selected, self.peaceful_button.rect)
                        draw_text(self.peaceful_button.text, font, white, (self.peaceful_button.rect.centerx - (self.peaceful_button.text_width / 2)), self.peaceful_button.rect.centery - 15)
                        if self.player.draw(0):
                            self.player.reset_rect()
                            settings_difficulty = 1
                    elif settings_difficulty == 1:
                        screen.blit(self.button_selected, self.player.rect)
                        draw_text(self.player.text, font, white, (self.player.rect.centerx - (self.player.text_width / 2)), self.player.rect.centery - 15)
                        if self.peaceful_button.draw(0):
                            self.peaceful_button.reset_rect()
                            settings_difficulty = 0
                    if self.select_back_button.draw(0):
                        world_names[world_num] = world_name_settings
                        world_difficulties[world_num] = settings_difficulty
                        with open(f'game_files/world_data/world_{world_num}/name/world_name.json', "w") as file:
                            json.dump(world_name_settings, file)
                        with open(f'game_files/world_data/world_{world_num}/difficulty/difficulty.json', "w") as file:
                            json.dump(settings_difficulty, file)
                        self.game_state = 7
                    if self.delete_world_button.draw(0):
                        self.delete_state = 1
                elif self.delete_state == 1:
                    draw_text("Are you sure you want to delete?", font, white, 130, 200)
                    if self.delete_yes_button.draw(0):
                        self.delete_state = 0
                        world_generated[world_num] = False
                        with open(f'game_files/world_data/world_{world_num}/generated/generated.json', "w") as file:
                            json.dump(False, file)
                            self.game_state = 7
                    if self.delete_no_button.draw(0):
                        self.delete_state = 0
            elif self.game_state == 9:
                screen.blit(self.settings_bg, (0, 0))
                settings_state = self.setting_selector.update(ingame)
                #save and change state if back button is pressed
                if settings_state == 'back':
                    save_settings()
                    self.set_self.keybinds.get_self.keybinds()
                    if ingame:
                        #save new difficulty
                        world_difficulties[world_num] = settings_difficulty_ingame
                        with open(f'game_files/world_data/world_{world_num}/difficulty/difficulty.json', "w") as file:
                            json.dump(settings_difficulty_ingame, file)
                        self.game_state = 2
                    else:
                        self.game_state = 6
                    continue
                if settings_state == 'audio':
                    draw_text('Sound Effects', font, (0, 0, 0), 200, 85)
                    draw_text('Music', font, (0, 0, 0), 200, 185)
                    if self.sfx == True:
                        if self.sfx_on_button.draw(0):
                            self.sfx = False
                    else:
                        if self.sfx_off_button.draw(0):
                            self.sfx = True
                    if self.music == True:
                        if self.music_on_button.draw(0):
                            self.music = False
                    else:
                        if self.music_off_button.draw(0):
                            self.music = True
                elif settings_state == 'controls':
                     self.set_self.keybinds.update()
                elif settings_state == 'graphics':
                    draw_text('Show Coordinates:', font, (0, 0, 0), 170, 85)
                    if self.coords_on == True:
                        if self.coords_on_button.draw(0):
                            coords_on = False
                    elif coords_on == False:
                        if self.coords_off_button.draw(0):
                            coords_on = True
                elif settings_state == 'credits':
                    #Thanks again, guys, for the inspiration. I liley would never have made this project without it
                    draw_text_freetype('Thanks to Jacob Alexander and James Bates,', settings_font, 20, (0, 0, 0), 100, 75)
                    draw_text_freetype('who helped to inspire this game.', settings_font, 20, (0, 0, 0), 150, 100)
                    #Draw library license viewer buttons
                    draw_text_freetype('Numpy:', settings_font, 25, (0, 0, 0), 90, 150)
                    draw_text_freetype('Open Simplex Noise:', settings_font, 25, (0, 0, 0), 90, 210)
                    draw_text_freetype('Pillow:', settings_font, 25, (0, 0, 0), 90, 270)
                    draw_text_freetype('Pyperclip:', settings_font, 25, (0, 0, 0), 90, 330)
                    draw_text_freetype('Pygame-ce:', settings_font, 25, (0, 0, 0), 110, 390)
                    draw_text_freetype('Medieval Sharp:', settings_font, 25, (0, 0, 0), 110, 430)
                    draw_text_freetype('DM Serif Text:', settings_font, 25, (0, 0, 0), 110, 490)
        
                    if self.numpy_button.draw(0):
                        self.game_state = 'view_attributions'
                        license_image = get_license_text('numpy-1.26.4')
                    elif self.open_simplex_button.draw(0):
                        self.game_state = 'view_attributions'
                        license_image = get_license_text('open_simplex-0.4.5.1')
                    elif self.pillow_button.draw(0):
                        self.game_state = 'view_attributions'
                        license_image = get_license_text('pillow-10.4.0')
                    elif self.pyperclip_button.draw(0):
                        self.game_state = 'view_attributions'
                        license_image = get_license_text('pyperclip-1.9.0')
                    elif self.pygame_ce_button.draw(0):
                        self.game_state = 'view_attributions'
                        license_image = get_license_text('pygame_ce-2.5.3')
                    elif self.medieval_sharp_button.draw(0):
                        self.game_state = 'view_attributions'
                        license_image = get_license_text('medieval-sharp-font')
                    elif self.DM_Serif_Text_button.draw(0):
                        self.game_state = 'view_attributions'
                        license_image = get_license_text('DM_Serif_Text')
                elif settings_state == 'world':
                    draw_text('Seed: '+ str(self.world_seeds[world_num]), font, white, 120, 100)     
                    draw_text('World Name: ' + world_names[world_num], font, white, 120, 20)     
                    if settings_difficulty_ingame == 0:
                        screen.blit(self.button_selected, self.peaceful_button_ingame.rect)
                        draw_text(self.peaceful_button_ingame.text, font, white, (self.peaceful_button_ingame.rect.centerx - (self.peaceful_button_ingame.text_width / 2)), self.peaceful_button_ingame.rect.centery - 15)
                        if self.player_ingame.draw(0):
                            self.player_ingame.reset_rect()
                            settings_difficulty_ingame = 1
                    elif settings_difficulty_ingame == 1:
                        screen.blit(self.button_selected, self.player_ingame.rect)
                        draw_text(self.player_ingame.text, font, white, (self.player_ingame.rect.centerx - (self.player_ingame.text_width / 2)), self.player_ingame.rect.centery - 15)
                        if self.peaceful_button_ingame.draw(0):
                            self.peaceful_button_ingame.reset_rect()
                            settings_difficulty_ingame = 0
            elif self.game_state == 'view_attributions':
                screen.blit(self.settings_bg, (0, 0))
                license_scroll = self.license_settings_scroll_bar.update()
                draw_license_text(license_image, license_scroll)
                if self.license_back_button.update():
                    self.game_state = 9
            elif self.game_state == 'select_self.player':
                screen.blit(self.player_select_bg, (0, 0))
                self.select_charachter.update()
                if self.done_charachter_button.draw(0):
                    self.player.get_self.player_image()
                    self.inventory.get_self.player_image()
                    self.game_state = 6
                #only can edit if not on a defult
                if self.select_charachter.current_self.player != 1 and self.select_charachter.current_self.player != 2:
                    if self.edit_charachter_button.draw(0):
                        self.select_charachter.edit_setup()
                        self.game_state = 'edit_self.player'
                else:
                    draw_text('Default', font, (0, 0, 0), 260, 435)
            elif self.game_state == 'edit_self.player':
                screen.blit(self.player_select_bg, (0, 0))
                if self.back_charachter_button.draw(0):
                    #save genders, images, and current self.player
                    self.select_charachter.save_genders()
                    self.select_charachter.save_self.players()
                    save_settings()
                    self.game_state = 'select_self.player'
                #draw input boxes    
                h = self.h_input.draw(0)
                s = self.s_input.draw(0)
                v = self.v_input.draw(0)
                r = self.r_input.draw(0)
                g = self.g_input.draw(0)
                b = self.b_input.draw(0)
                hexcode = self.hex_input.draw(0)
                #draw input box labels
                draw_text('h', self.font_self.inventory, colour_inactive, 335, 372)
                draw_text('s', self.font_self.inventory, colour_inactive, 402, 372)
                draw_text('v', self.font_self.inventory, colour_inactive, 469, 372)
                draw_text('r', self.font_self.inventory, colour_inactive, 335, 422)
                draw_text('g', self.font_self.inventory, colour_inactive, 402, 422)
                draw_text('b', self.font_self.inventory, colour_inactive, 469, 422)
                draw_text('hex', self.font_self.inventory, colour_inactive, 360, 472)
                #draw divider lines
                pygame.draw.line(screen, (174, 144, 92), (90, 370), (510, 370))
                pygame.draw.line(screen, (174, 144, 92), (275, 50), (275, 370))
                pygame.draw.line(screen, (174, 144, 92), (90, 105), (510, 105))
                #try-except prevents the user from inputting things that will not work
                try:
                    #check if the user has updated them
                    if int(h) != self.select_charachter.colour_picker_colour['hsv'][0]:
                        if int(h) <= 360 and int(h) >= 0:
                            self.select_charachter.change_pos_on_input('h', h)
                        else:
                            self.select_charachter.reset_inputs()
                    elif int(s) != self.select_charachter.colour_picker_colour['hsv'][1]:
                        if int(s) <= 100 and int(s) >= 0:
                            self.select_charachter.change_pos_on_input('s', s)
                        else:
                            self.select_charachter.reset_inputs()
                    elif int(v) != self.select_charachter.colour_picker_colour['hsv'][2]:
                        if int(v) <= 100 and int(v) >= 0:
                            self.select_charachter.change_pos_on_input('v', v)
                        else:
                            self.select_charachter.reset_inputs()
                    elif int(r) != self.select_charachter.colour_picker_colour['rgb'][0]:
                        if int(r) <= 255 and int(r) >= 0:
                            self.select_charachter.change_pos_on_input('r', r)
                        else:
                            self.select_charachter.reset_inputs()
                    elif int(g) != self.select_charachter.colour_picker_colour['rgb'][1]:
                        if int(g) <= 255 and int(g) >= 0:
                            self.select_charachter.change_pos_on_input('g', g)
                        else:
                            self.select_charachter.reset_inputs()
                    elif int(b) != self.select_charachter.colour_picker_colour['rgb'][2]:
                        if int(b) <= 255 and int(b) >= 0:
                            self.select_charachter.change_pos_on_input('b', b)
                        else:
                            self.select_charachter.reset_inputs()
                    elif hexcode != self.select_charachter.colour_picker_colour['hex']:
                        self.select_charachter.change_pos_on_input('hex', hexcode)
                except:
                    #just reset if bad input
                    self.select_charachter.reset_inputs()
                #Run selection buttons. Only show buttons if they can be pressed
                if self.select_charachter.get_editing() == 'hair':
                    screen.blit(self.charachter_hair_button.txt_surface, (self.charachter_hair_button.rect.centerx - (self.charachter_hair_button.text_width / 2), self.charachter_hair_button.rect.centery - 15))
                else:
                    if self.charachter_hair_button.draw(0):
                        self.select_charachter.set_editing('hair')
                if self.select_charachter.get_editing() == 'skin':
                    screen.blit(self.charachter_skin_button.txt_surface, (self.charachter_skin_button.rect.centerx - (self.charachter_skin_button.text_width / 2), self.charachter_skin_button.rect.centery - 15))
                else:
                    if self.charachter_skin_button.draw(0):
                        self.select_charachter.set_editing('skin')
                if self.select_charachter.get_editing() == 'eyes':
                    screen.blit(self.charachter_eyes_button.txt_surface, (self.charachter_eyes_button.rect.centerx - (self.charachter_eyes_button.text_width / 2), self.charachter_eyes_button.rect.centery - 15))
                else:
                    if self.charachter_eyes_button.draw(0):
                        self.select_charachter.set_editing('eyes')
                if self.select_charachter.get_editing() == 'shirt':
                    screen.blit(self.charachter_shirt_button.txt_surface, (self.charachter_shirt_button.rect.centerx - (self.charachter_shirt_button.text_width / 2), self.charachter_shirt_button.rect.centery - 15))
                else:
                    if self.charachter_shirt_button.draw(0):
                        self.select_charachter.set_editing('shirt')
                if self.select_charachter.get_editing() == 'pants':
                    screen.blit(self.charachter_pants_button.txt_surface, (self.charachter_pants_button.rect.centerx - (self.charachter_pants_button.text_width / 2), self.charachter_pants_button.rect.centery - 15))
                else:
                    if self.charachter_pants_button.draw(0):
                        self.select_charachter.set_editing('pants')
                if self.select_charachter.get_editing() == 'shoes':
                    screen.blit(self.charachter_shoes_button.txt_surface, (self.charachter_shoes_button.rect.centerx - (self.charachter_shoes_button.text_width / 2), self.charachter_shoes_button.rect.centery - 15))
                else:
                    if self.charachter_shoes_button.draw(0):
                        self.select_charachter.set_editing('shoes')
                if self.swap_gender.draw(0):
                    self.select_charachter.swap_genders()
                #run editor code. Needs to be at bottom or input boxes don't work
                self.select_charachter.edit()
            #refresh the screen
            pygame.display.update() 
            #limit fps
            clock.tick(fps)
#create instance of main class
main = Main()
#run game loop
main.game_loop()
#close window
pygame.quit()