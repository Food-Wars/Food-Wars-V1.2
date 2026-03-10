# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 13:31:29 2024

"""
import json


crafting_recepies = {
                    "sharp_stick_recepie": [[None,2,None,None,2,None,None,None,None], [7, 1]],
                    "planks_recepie": [[None,1,None,None,1,None,None,None,None], [3, 2]],
                    "wooden_axe_recepie": [[3,3,None,3,2,None,None,2,None], [8, 1]],
                    "stone_axe_recepie": [[5,5,None,5,2,None,None,2,None], [11, 1]],
                    "wooden_pickaxe_recepie": [[None,3,None,3,2,3,None,2,None], [9, 1]],
                    "stone_pickaxe_recepie": [[None,5,None,5,2,5,None,2,None], [12, 1]],
                    "suger_cloth_recepie": [[13,13,None,13,13,None,None,None,None], [14, 2]],
                    "suger_cloth_helmet_recepie": [[14,14,14,14,None,14,None,None,None], [16, 1]],
                    "suger_cloth_pants_recepie": [[14,14,14,14,None,14,14,None,14], [18, 1]],
                    "suger_cloth_chestplate_recepie": [[14,None,14,14,14,14,14,14,14], [17, 1]],
                    "suger_cloth_boots_recepie": [[None,None,None,14,None,14,14,None,14], [19, 1]],
                    }

with open('C:/Users/zrobi/Documents/python scripts/food wars/V_1.1/game_files/crafting/crafting_recepies.json', "w") as file:
    json.dump(crafting_recepies, file)
    
print('Saved!')