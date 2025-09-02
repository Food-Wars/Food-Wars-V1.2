# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 09:53:05 2024

@author: zrobi
"""
#import defult libraries
import random
import math
import copy
#import 3rd party libraries
import pygame

entitie_dict = {}
projectiles = {}
entities_to_pop = []
projectiles_to_pop = []
def spawn_entities(world_difficulties, world_num, player):
    #only spawn entities if hostile difficulty is on
    if world_difficulties[world_num] == 1:
        #only spwan entities if there are 3 or less; max total is 4
        if len(entitie_dict) < 4:
            #don't constantly spawn if there isn't an entity
            spawn = random.randint(0, 10)
            if spawn == 0:
                #select random position around the player
                x = random.randint(player.rect.x - 400, player.rect.x + 400)
                y = random.randint(player.rect.y - 400, player.rect.y + 400)
                #select random entity type
                entity_type = random.choice(['gelatin', 'cotten_candy'])
                entity_num = 0
                #make sure the entity has an unique id
                while entity_num in entitie_dict:
                    entity_num += 1
                #spawn entity
                if entity_type == 'gelatin':
                    entitie_dict[entity_num] = Gelatin(entity_num, x, y)
                elif entity_type == 'cotten_candy':
                    entitie_dict[entity_num] = Cotten_Candy(entity_num, x, y)

class Pathfinding():
    def circle_points_path(self, target_pos, own_pos, distance_from_target, diagonals = False):
        possible_points = []
        #add all 4 quadrantle points
        possible_points.append((target_pos[0] + distance_from_target, target_pos[1]))
        possible_points.append((target_pos[0], target_pos[1] + distance_from_target))
        possible_points.append((target_pos[0] - distance_from_target, target_pos[1]))
        possible_points.append((target_pos[0], target_pos[1] - distance_from_target))
        #use trig to add all 4 other points
        if diagonals == True:
            abs_point = math.sqrt(2 * distance_from_target) / 2
            possible_points.append((target_pos[0] + abs_point, target_pos[1] + abs_point))
            possible_points.append((target_pos[0] + abs_point, target_pos[1] - abs_point))
            possible_points.append((target_pos[0] - abs_point, target_pos[1] + abs_point))
            possible_points.append((target_pos[0] - abs_point, target_pos[1] - abs_point))
        #find which point is closest
        current_best = [1000000, (0, 0)]
        for point in possible_points:
            #give each point a score based on how far away it is
            point_score = (own_pos[0] - point[0]) + (own_pos[1] - point[1])
            if point_score < current_best[0]:
                current_best[0] = point_score
                current_best[1] = point 
        #create the vector
        vector = (own_pos[0] - current_best[1][0], own_pos[1] - current_best[1][1])
        #get normalised vector
        normalised_vector = self.normalise_vector(vector)
        return normalised_vector
    def normalise_vector(self, vector):
        #get megnitude using pythagorium therom
        magnitude = math.sqrt((vector[0] ** 2) + (vector[1] ** 2))
        #normalise vector
        if magnitude != 0:
            normalised_vector = (vector[0] / magnitude, vector[1] / magnitude)
        else:
            normalised_vector = vector
        #return the normalised vector
        return normalised_vector
def get_volume(distance):
    '''Get what entity volume for sfx should be based on distance to the player'''
    volume = math.exp2(-0.005 * abs(distance))
    print(volume, distance)
    return volume
class Cotten_Candy(Pathfinding):
    def __init__(self, entity_num, x, y):
        temp_sprite = pygame.image.load('game_files/imgs/entities/cotten_candy/cotten_candy.png')
        self.img = pygame.transform.scale(temp_sprite, (temp_sprite.get_width() * 2, temp_sprite.get_height() * 2))
        self.rect = pygame.rect.Rect(0, 0, 32, 64)
        self.x = x
        self.y = y
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.health = 20
        self.walk_count = 0
        self.direction = random.choice(['n', 'e', 's', 'w'])
        self.entity_num = entity_num
        self.attack_cooldown = 0
        self.animation_switch_counter =  0
        self.hors_frame = 0
        self.speed = 4
    def damage(self, damage_amount):
        self.health -= damage_amount
    def save_to_file(self):
        created_dict = vars(self)
        #this code is to avoid a whole seperate copy function, as copy.deepcopy cannot copy pygame surfaces
        #and just deleting the img form the dict deleates it from the class entierly
        img = created_dict['img'].copy()
        del created_dict['img']
        self_dict = copy.deepcopy(created_dict)
        #copy dict. previously editing created dict would edit class as well
        self_dict['class_type'] = 'cotten_candy'
        #sprite and rect need to converted to other form to be saved
        self_dict['rect'] = (0, 0, 32, 64)
        self_dict['rect_x'] = self.rect.x
        self_dict['rect_y'] = self.rect.y
        #add copied img back into class
        self.img = img
        return self_dict
    @classmethod 
    def load_from_file(cls, attributes):
        #create new object of this class
        obj = cls.__new__(cls)
        #create class variables from attributes
        sprite = pygame.image.load('game_files/imgs/entities/cotten_candy/cotten_candy.png')
        obj.img = pygame.transform.scale(sprite, (sprite.get_width() * 2, sprite.get_height() * 2))
        obj.rect = pygame.rect.Rect(0, 0, 32, 64)
        obj.x = attributes['x']
        obj.y =  attributes['y']
        obj.rect.centerx = attributes['rect_x']
        obj.rect.centery = attributes['rect_y']
        obj.health =  attributes['health']
        obj.walk_count =  attributes['walk_count']
        obj.direction =  attributes['direction']
        obj.entity_num =  attributes['entity_num']
        obj.attack_cooldown =  attributes['attack_cooldown']
        obj.hors_frame =  attributes['hors_frame']
        obj.speed =  attributes['speed']
        obj.animation_switch_counter =  attributes['animation_switch_counter']
        return obj
    def update(self, player, scroll, debug, screen, water_rects, grass_rects, Collectable, game_map, sfx, play_sfx):
        #check if dead, then drop item
        if self.health <= 0:
            #iterate through all tiles on screen
            drop_chunk = None
            for tile in grass_rects:
                if tile[0].collidepoint((self.rect.centerx, self.rect.centery)):
                    drop_chunk = tile[1]
                    drop_tile  = game_map[drop_chunk].index(tile[2])
                    break
            if drop_chunk != None:
                for tile in water_rects:
                    if tile[0].collidepoint((self.rect.centerx, self.rect.centery)):
                        drop_chunk = tile[1]
                        drop_tile  = game_map[drop_chunk].index(tile[2])
                        break
            #set interactable for tile to string
            if drop_chunk != None:
                game_map[drop_chunk][drop_tile][2] = Collectable((160, 0, 32, 32), drop_chunk, drop_tile, 13)
            #add self to list so it will be removed
            global entities_to_pop
            entities_to_pop.append(self.entity_num)
        else:
            #change speed if in water
            for tile in water_rects:
                if self.rect.colliderect(tile[0]):
                    speed = self.speed * 0.75
                    break
                else:
                    speed = self.speed
            distance = math.sqrt(((player.hitbox.centerx - self.rect.centerx) ** 2) + ((player.hitbox.centery - self.rect.centery) ** 2))
            #move based on scroll
            self.rect.x = self.x - scroll[0]
            self.rect.y = self.y - scroll[1]
            vector = self.circle_points_path((player.hitbox.x, player.hitbox.y), (self.rect.x, self.rect.y), 30)
            if abs(vector[0]) > abs(vector[1]):
                if vector[0] > 0:
                    self.direction = 'd'
                elif vector[0] < 0:
                    self.direction = 'a'
            elif abs(vector[0]) < abs(vector[1]):
                if vector[1] > 0:
                    self.direction = 'w'
                elif vector[1] < 0:
                    self.direction = 's'
            if distance < 4000 and distance > 20:
                #move based on vector
                #not sure why you need to flip vector direction to make them come closer not run away
                self.x += -vector[0] * speed
                self.y += -vector[1] * speed
            #despawn if player is to far away
            elif distance > 8000:
                entities_to_pop.append(self.entity_num)
            if self.walk_count == 3:
                self.walk_count = 0 
            elif self.animation_switch_counter >= 2:
                self.walk_count += 1
                self.animation_switch_counter = 0
            else:
                self.animation_switch_counter += 1
            #collision
            if distance <= 50:
                if self.attack_cooldown == 14:
                    player.damage(2)
                    self.attack_cooldown = 0
                else:
                    self.attack_cooldown += 1
            #wsad based
            if self.direction == 's':
                self.hors_frame = 0
            elif self.direction == 'd':
                self.hors_frame = 3
            elif self.direction  == 'w':
                self.hors_frame = 2
            elif self.direction == 'a':
                self.hors_frame = 1
            screen.blit(self.img, self.rect, (32 * self.hors_frame, 64 * self.walk_count, 32, 64))
            if debug == True:
                pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
        return game_map
class Gelatin(Pathfinding):
    def __init__(self, entity_num, x, y):
        self.colour = random.choice(['red', 'yellow', 'blue', 'green'])
        sprite = pygame.image.load('game_files/imgs/entities/gelatin/' + self.colour + '_gelatin.png')
        self.sprite = pygame.transform.scale(sprite, (sprite.get_width() * 2, sprite.get_height() * 2))
        self.rect = pygame.rect.Rect(0, 0, 32, 64)
        self.x = x
        self.y = y
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.health = 15
        self.walk_count = 0
        self.direction = random.choice(['n', 'e', 's', 'w'])
        self.entity_num = entity_num
        self.attack_cooldown = 0
        self.hors_frame = 0
        self.speed = 2.5
    def damage(self, damage_amount):
        self.health -= damage_amount
    def save_to_file(self):
        created_dict = vars(self)
        #this code is to avoid a whole seperate copy function, as copy.deepcopy cannot copy pygame surfaces
        #and just deleting the img form the dict deleates it from the class entierly
        sprite = created_dict['sprite'].copy()
        del created_dict['sprite']
        #copy dict. before editing created dict would edit class as well
        self_dict = copy.deepcopy(created_dict)
        self_dict['class_type'] = 'gelatin'
        #sprite and rect need to converted to other form to be saved
        self_dict['rect'] = (0, 0, 32, 64)
        self_dict['rect_x'] = self.rect.x
        self_dict['rect_y'] = self.rect.y
        #add copied sprite back to class
        self.sprite = sprite
        return self_dict
    @classmethod 
    def load_from_file(cls, attributes):
        #create new object of this class
        obj = cls.__new__(cls)
        #create class variables from attributes
        obj.colour = attributes['colour']
        sprite = pygame.image.load('game_files/imgs/entities/gelatin/' + obj.colour + '_gelatin.png')
        obj.sprite = pygame.transform.scale(sprite, (sprite.get_width() * 2, sprite.get_height() * 2))
        obj.rect = pygame.rect.Rect(0, 0, 32, 64)
        obj.x = attributes['x']
        obj.y =  attributes['y']
        obj.rect.centerx = attributes['rect_x']
        obj.rect.centery = attributes['rect_y']
        obj.health =  attributes['health']
        obj.walk_count =  attributes['walk_count']
        obj.direction =  attributes['direction']
        obj.entity_num =  attributes['entity_num']
        obj.attack_cooldown =  attributes['attack_cooldown']
        obj.hors_frame =  attributes['hors_frame']
        obj.speed =  attributes['speed']
        obj.sounds = []
        return obj
    def update(self, player, scroll, debug, screen, water_rects, grass_rects, Collectable, game_map, sfx, play_sfx):
        if self.health <= 0:
            #iterate through all tiles on screen
            #iterate through all tiles on screen
            drop_chunk = None
            for tile in grass_rects:
                if tile[0].collidepoint((self.rect.centerx, self.rect.centery)):
                    drop_chunk = tile[1]
                    drop_tile  = game_map[drop_chunk].index(tile[2])
                    break
            if drop_chunk != None:
                for tile in water_rects:
                    if tile[0].collidepoint((self.rect.centerx, self.rect.centery)):
                        drop_chunk = tile[1]
                        drop_tile  = game_map[drop_chunk].index(tile[2])
                        break
            #currently only blue
            if drop_chunk != None:
                if self.colour == 'red':
                    game_map[drop_chunk][drop_tile][2] = Collectable((128, 0, 32, 32), drop_chunk, drop_tile, 21)
                elif self.colour == 'yellow':
                    game_map[drop_chunk][drop_tile][2] = Collectable((128, 32, 32, 32), drop_chunk, drop_tile, 23)
                elif self.colour == 'blue':
                    game_map[drop_chunk][drop_tile][2] = Collectable((96, 0, 32, 32), drop_chunk, drop_tile, 20)
                elif self.colour == 'green':
                    game_map[drop_chunk][drop_tile][2] = Collectable((96, 32, 32, 32), drop_chunk, drop_tile, 22)
            global entities_to_pop
            entities_to_pop.append(self.entity_num)
        else:
            #change speed if in water
            for tile in water_rects:
                if self.rect.colliderect(tile[0]):
                    speed = self.speed * 0.5
                    break
                else:
                    speed = self.speed
            distance = math.sqrt(((player.hitbox.centerx - self.rect.centerx) ** 2) + ((player.hitbox.centery - self.rect.centery) ** 2))
            self.rect.x = self.x - scroll[0]
            self.rect.y = self.y - scroll[1]
            if distance < 4000 and distance > 100:
                vector = self.circle_points_path((player.hitbox.x, player.hitbox.y), (self.rect.x, self.rect.y), 100, True)
                if abs(vector[0]) > abs(vector[1]):
                    if vector[0] > 0:
                        self.direction = 'd'
                    elif vector[0] < 0:
                        self.direction = 'a'
                elif abs(vector[0]) < abs(vector[1]):
                    if vector[1] > 0:
                        self.direction = 'w'
                    elif vector[1] < 0:
                        self.direction = 's'
                #move based on vector
                #not sure why you need to flip vector direction to make them com closer not run away
                self.x += -vector[0] * speed
                self.y += -vector[1] * speed
            #despawn if player is to far away
            elif distance > 8000:
                entities_to_pop.append(self.entity_num)
            else:
                vector = self.circle_points_path((player.hitbox.x, player.hitbox.y), (self.rect.x, self.rect.y), 100)
                #check if vertically aligned with player
                if abs(vector[0]) > abs(vector[1]):
                    if vector[0] > 0:
                        self.direction = 'd'
                    elif vector[0] < 0:
                        self.direction = 'a'
                elif abs(vector[0]) < abs(vector[1]):
                    if vector[1] > 0:
                        self.direction = 'w'
                    elif vector[1] < 0:
                        self.direction = 's'
            if self.walk_count == 4:
                self.walk_count = 0 
            else:
                self.walk_count += 1
            #make sure that sounds are on
            if play_sfx == True:
                #play sound on right frame
                if self.walk_count == 0:
                    #get channel based on entity number 
                    channel = pygame.mixer.Channel(0)
                    #set volume based on distance to player
                    channel.set_volume(get_volume(distance)) 
                    #get random sfx
                    sound = random.choice(sfx['gelatin'])
                    #play the sound
                    channel.play(sound)

            #only atteck when in range
            if distance <= 300:
                #can only attack every so often
                if self.attack_cooldown == 25:
                    self.attack_cooldown = 0
                    global projectiles
                    projecilte_num = 0
                    while projecilte_num in projectiles:
                        projecilte_num += 1
                    #create vector for projectiel mvoement
                    vector = (self.rect.x - player.hitbox.x, self.rect.y - player.hitbox.y)
                    normalised_vector = self.normalise_vector(vector)
                    projectiles[projecilte_num] = Projectile(self.colour, self.x, self.y, projecilte_num, 25, normalised_vector)
                else:
                    self.attack_cooldown += 1
            #base on wsad
            if self.direction == 's':
                self.hors_frame = 0
            elif self.direction == 'd':
                self.hors_frame = 3
            elif self.direction  == 'w':
                self.hors_frame = 2
            elif self.direction == 'a':
                self.hors_frame = 1
            screen.blit(self.sprite, self.rect, (32 * self.hors_frame, 64 * self.walk_count, 32, 64))
            if debug == True:
                pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
        return game_map

class Projectile():
    def __init__(self, colour, x, y, projectile_num, hit_timer, vector):
        self.colour = colour
        self.hit_timer = hit_timer
        self.projectile_num = projectile_num
        sprite = pygame.image.load('game_files/imgs/entities/gelatin_projectile/' + self.colour + '_gelatin_projectile.png')
        self.sprite = pygame.transform.scale(sprite, (sprite.get_width() * 1.5, sprite.get_height() * 1.5))
        self.rect = pygame.rect.Rect(0, 0, 24, 24)
        self.x = x
        self.y = y
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.x_change = 0
        self.y_change = 0
        self.vector = vector
        if abs(self.vector[0]) > abs(self.vector[1]):
            if self.vector[0] > 0:
                self.direction = 'd'
            elif self.vector[0] < 0:
                self.direction = 'a'
        elif abs(self.vector[0]) < abs(self.vector[1]):
            if self.vector[1] > 0:
                self.direction = 'w'
            elif self.vector[1] < 0:
                self.direction = 's'
        else:
            #horizontal animation is the defult
            if self.vector[0] > 0:
                self.direction = 'd'
            elif self.vector[0] < 0:
                self.direction = 'a'
        self.hors_frame = 0
        if self.direction == 'a':
            self.hors_frame = 1
        elif self.direction == 'd':
            self.hors_frame = 3
        elif self.direction == 's':
            self.hors_frame = 0
        elif self.direction == 'w':
            self.hors_frame = 2
        self.frame_counter = 0
    def update(self, player, scroll, screen, debug):
        self.hit_timer -= 1
        global projectiles_to_pop
        if self.rect.colliderect(player.hitbox):
            projectiles_to_pop.append(self.projectile_num)
            player.damage(2)
        for tile in entitie_dict:
            if self.rect.colliderect(entitie_dict[tile].rect) and self.hit_timer <= 0:
                #gelatin projectiles dont hurt gelatin
                if not isinstance(entitie_dict[tile], Gelatin):
                    entitie_dict[tile].damage(1) 
                    projectiles_to_pop.append(self.projectile_num)
        #move based on window scroll
        self.rect.x = self.x - scroll[0]
        self.rect.y = self.y - scroll[1]
        #speed is 10
        #not sure why it has to be subtaction
        self.x -= self.vector[0] * 10.5
        self.y -= self.vector[1] * 10.5
        if self.frame_counter >= 5:
            self.frame_counter = 0
        else:
            self.frame_counter += 1
        screen.blit(self.sprite, self.rect, (24 * self.hors_frame, 24 * self.frame_counter, 24, 24))
        if debug == True:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
        