import numpy as np
from pokedex import *
from collections import defaultdict

# http://www.psypokes.com/dex/stats.php

class Moves:
    def __init__(self, movesDict):
        self.name = movesDict['name']
        self.accuracy = movesDict['accuracy']                   # int
        self.power = movesDict['power']                         # int
        self.type = movesDict['type']                           # pokemon type, e.g., fire, water, etc
        self.kind = movesDict['kind']                           # kind of moves, physical, special, status
        self.statEffect = movesDict['statEffect']               # status this move can cause. if kind is special or status, what is it. e.g, Burn, Freeze, Poison, otherwise None
        self.statEffectProb = movesDict['statEffectProb']       # probability of the status working
        self.statEffected = movesDict['statEffected']           # how does it affect the opponent's stats
        self.priority = movesDict['priority']                   # priority
        self.count = movesDict['count']                         # number of times this moves can be used
        self.target = movesDict['target']                       # who is affected by the move. 0 for self, 1 for opponent
        self.recoil = movesDict['recoil']                       # does the move affect us?

class Pokemon:
    def __init__(self, pokeDict):
        self.name = pokeDict["name"]
        self.level = pokeDict["level"]
        self.type = pokeDict["type"]
        self.hp = pokeDict["hp"]
        self.hp_max = pokeDict["hp"]
        self.attack = pokeDict["attack"]
        self.defense = pokeDict["defense"]
        self.sp_attack = pokeDict["sp_attack"]
        self.sp_defense = pokeDict["sp_defense"]
        self.speed = pokeDict["speed"]
        self.stat = pokeDict["stat"]
        self.moves = pokeDict["moves"]
        self.accuracy = pokeDict["accuracy"]



# pokemon_dict = {
#     'Venusaur' : Pokemon(venusaur_dict),
#     'Charizard' : Pokemon(charizard_dict),
#     'Blastoise' : Pokemon(blastoise_dict),
#     'Butterfree' : Pokemon(butterfree_dict),
#     'Beedrill' : Pokemon(beedrill_dict),
#     'Pidegot' : Pokemon(pidgeot_dict),
#     'Fearow' : Pokemon(fearow_dict),
#     'Arbok' : Pokemon(arbok_dict),
#     'Raichu' : Pokemon(raichu_dict),
#     'Sandslash' : Pokemon(sandslash_dict),
#     'Nidoking' : Pokemon(nidoking_dict),
#     'Clefable' : Pokemon(nidoking_dict)
# }

# # reassigning moves to pokemon
# for (i, pokemon) in enumerate(pokemon_dict):
#     print(pokemon)
#     pokemon_dict[pokemon].moves = pokemon_moves_assignment[Pokemon]

thunderbolt_dict = {
                'name' : 'Thunderbolt',                 
                'accuracy' : 100,
                'power' : 95,
                'type' : 'electra',
                'kind' : 'special',
                'statEffect' : 'paralysis',
                'statEffectProb' : 0.1,
                'statEffected' : None,
                'priority' : 0,
                'count' : 15,
                'target' : [1],
                'recoil' : 0

                    }


quickattack_dict = {
                'name' : 'Quick Attack',                  
                'accuracy' : 100,
                'power' : 40,
                'type' : 'normal',
                'kind' : 'physical',
                'statEffect' : None,
                'statEffectProb' : 0,
                'statEffected' : None,
                'priority' : 1,
                'count' : 30,
                'target' : [1],
                'recoil' : 0
}

thunderwave_dict = {
                'name' : 'Thunder Wave',                  
                'accuracy' : 100,
                'power' : 0,
                'type' : 'electra',
                'kind' : 'status',
                'statEffect' : 'paralysis',
                'statEffectProb' : 1,
                'statEffected' : None,
                'priority' : 0,
                'count' : 20,
                'target' : [1],
                'recoil' : 0
}

growl_dict = {
                'name' : 'Growl', 
                'accuracy' : 100,
                'power' : 0,
                'type' : 'normal',
                'kind' : 'status',
                'statEffect' : 'reduce',
                'statEffectProb' : 1,
                'statEffected' : 'attack',
                'priority' : 0,
                'count' : 40,
                'target' : [1],
                'recoil' : 0
}

ember_dict = {
                'name' : 'Ember',
                'accuracy' : 100,
                'power' : 40,
                'type' : 'fire',
                'kind' : 'special',
                'statEffect' : 'burn',
                'statEffectProb' : 0.1,
                'statEffected' : None,
                'priority' : 0,
                'count' : 25,
                'target' : [1],
                'recoil' : 0
}

smokescreen_dict = {
                'name' : 'Smoke Screen',
                'accuracy' : 100,
                'power' : 0,
                'type' : 'normal',
                'kind' : 'status',
                'statEffect' : 'reduce',
                'statEffectProb' : 1,
                'statEffected' : 'accuracy',
                'priority' : 0,
                'count' : 20,
                'target' : [1],
                'recoil' : 0
}

scratch_dict = {
                'name' :'Scratch', 
                'accuracy' : 100,
                'power' : 40,
                'type' : 'normal',
                'kind' : 'physical',
                'statEffect' : None,
                'statEffectProb' : 0,
                'statEffected' : None,
                'priority' : 0,
                'count' : 35,
                'target' : [1],
                'recoil' : 0
}

toxic_dict = {
                'name' : 'Toxic',
                'accuracy' : 90,
                'power' : 0,
                'type' : 'poison',
                'kind' : 'status',
                'statEffect' : 'poison',
                'statEffectProb' : 1,
                'statEffected' : 'hp',
                'priority' : 0,
                'count' : 10,
                'target' : [1],
                'recoil' : 0
}

tackle_dict = {
                'name' : 'Tackle',
                'accuracy' : 95,
                'power' : 35,
                'type' : 'normal',
                'kind' : 'physical',
                'statEffect' : None,
                'statEffectProb' : 0,
                'statEffected' : None,
                'priority' : 0,
                'count' : 35,
                'target' : [1],
                'recoil' : 0
}

vinewhip_dict = {
                'name' : 'Vine Whip',
                'accuracy' : 100,
                'power' : 35,
                'type' : 'grass',
                'kind' : 'physical',
                'statEffect' : None,
                'statEffectProb' : 0,
                'statEffected' : None,
                'priority' : 0,
                'count' : 10,
                'target' : [1],
                'recoil' : 0
}

megadrain_dict = {
                'name' : 'Mega Drain',
                'accuracy' : 100,
                'power' : 40,
                'type' : 'grass',
                'kind' : 'special',
                'statEffect' : None,
                'statEffectProb' : 0,
                'statEffected' : None,
                'priority' : 0,
                'count' : 15,
                'target' : [0, 1],
                'recoil' : 0.5
}

aurorabeam_dict = {
                'name' : 'Aurora Beam',
                'accuracy' : 100,
                'power' : 65,
                'type' : 'ice',
                'kind' : 'special',
                'statEffect' : 'reduce',
                'statEffectProb' : 1,
                'statEffected' : 'attack',
                'priority' : 0,
                'count' : 20,
                'target' : [1],
                'recoil' : 0
}

bodyslam_dict = {
                'name' : 'Body Slam',
                'accuracy' : 100,
                'power' : 85,
                'type' : 'normal',
                'kind' : 'physical',
                'statEffect' : 'paralysis',
                'statEffectProb' : .3,
                'statEffected' : None,
                'priority' : 0,
                'count' : 15,
                'target' : [1],
                'recoil' : 0
}

flamethrower_dict = {
                'name' : 'Flamethrower',
                'accuracy' : 100,
                'power' : 90,
                'type' : 'fire',
                'kind' : 'special',
                'statEffect' : 'burn',
                'statEffectProb' : .1,
                'statEffected' : None,
                'priority' : 0,
                'count' : 15,
                'target' : [1],
                'recoil' : 0
}

surf_dict = {
                'name' : 'Surf',
                'accuracy' : 100,
                'power' : 90,
                'type' : 'water',
                'kind' : 'special',
                'statEffect' : None,
                'statEffectProb' : 0,
                'statEffected' : None,
                'priority' : 0,
                'count' : 15,
                'target' : [1],
                'recoil' : 0
}

hydropump_dict = {
                'name' : 'Hydro Pump',
                'accuracy' : 80,
                'power' : 110,
                'type' : 'water',
                'kind' : 'special',
                'statEffect' : None,
                'statEffectProb' : 0,
                'statEffected' : None,
                'priority' : 0,
                'count' : 5,
                'target' : [1],
                'recoil' : 0
}

thunder_dict = {
                'name' : 'Thunder',
                'accuracy' : 110,
                'power' : 70,
                'type' : 'electra',
                'kind' : 'special',
                'statEffect' : 'paralysis',
                'statEffectProb' : .3,
                'statEffected' : None,
                'priority' : 0,
                'count' : 15,
                'target' : [1],
                'recoil' : 0
}

icebeam_dict = {
                'name' : 'Ice Beam',
                'accuracy' : 100,
                'power' : 95,
                'type' : 'ice',
                'kind' : 'special',
                'statEffect' : 'freeze',
                'statEffectProb' : .1,
                'statEffected' : None,
                'priority' : 0,
                'count' : 10,
                'target' : [1],
                'recoil' : 0
}

submission_dict = {
                'name' : 'Submission',
                'accuracy' : 100,
                'power' : 80,
                'type' : 'fight',
                'kind' : 'physical',
                'statEffect' : 'paralysis',
                'statEffectProb' : .3,
                'statEffected' : None,
                'priority' : 0,
                'count' : 25,
                'target' : [0,1],
                'recoil' : -.25
}

sludge_dict = {
                'name' : 'Sludge',
                'accuracy' : 100,
                'power' : 65,
                'type' : 'poison',
                'kind' : 'special',
                'statEffect' : 'poison',
                'statEffectProb' : .3,
                'statEffected' : None,
                'priority' : 0,
                'count' : 20,
                'target' : [1],
                'recoil' : 0
}

earthquake_dict = {
                'name' : 'Earthquake',
                'accuracy' : 100,
                'power' : 100,
                'type' : 'ground',
                'kind' : 'physical',
                'statEffect' : None,
                'statEffectProb' : 0,
                'statEffected' : None,
                'priority' : 0,
                'count' : 10,
                'target' : [1],
                'recoil' : 0
}

drillpeck_dict = {
                'name' : 'Drill Peck',
                'accuracy' : 100,
                'power' : 80,
                'type' : 'flying',
                'kind' : 'physical',
                'statEffect' : None,
                'statEffectProb' : 0,
                'statEffected' : None,
                'priority' : 0,
                'count' : 20,
                'target' : [1],
                'recoil' : 0
}

psybeam_dict = {
                'name' : 'Psybeam',
                'accuracy' : 100,
                'power' : 65,
                'type' : 'psychc',
                'kind' : 'special',
                'statEffect' : None,
                'statEffectProb' : 0,
                'statEffected' : None,
                'priority' : 0,
                'count' : 20,
                'target' : [1],
                'recoil' : 0
}

psychic_dict = {
                'name' : 'Psychic',
                'accuracy' : 100,
                'power' : 90,
                'type' : 'psychc',
                'kind' : 'physical',
                'statEffect' : 'reduce',
                'statEffectProb' : .3,
                'statEffected' : 'sp_defense',
                'priority' : 0,
                'count' : 10,
                'target' : [1],
                'recoil' : 0
}

leechlife_dict = {
                'name' : 'Leech Life',
                'accuracy' : 100,
                'power' : 20,
                'type' : 'bug',
                'kind' : 'physical',
                'statEffect' : None,
                'statEffectProb' : 0,
                'statEffected' : None,
                'priority' : 0,
                'count' : 15,
                'target' : [0,1],
                'recoil' : 0.5
}

rockslide_dict = {
                'name' : 'Rock Slide',
                'accuracy' : 90,
                'power' : 75,
                'type' : 'rock',
                'kind' : 'physical',
                'statEffect' : None,
                'statEffectProb' : 0,
                'statEffected' : None,
                'priority' : 0,
                'count' : 10,
                'target' : [1],
                'recoil' : 0
}

nightshade_dict = {
                'name' : 'Night Shade',
                'accuracy' : 100,
                'power' : 40,
                'type' : 'ghost',
                'kind' : 'special',
                'statEffect' : None,
                'statEffectProb' : 0,
                'statEffected' : None,
                'priority' : 0,
                'count' : 15,
                'target' : [1],
                'recoil' : 0
}

dragonrage_dict = {
                'name' : 'Dragon Rage',
                'accuracy' : 100,
                'power' : 40,
                'type' : 'dragon',
                'kind' : 'special',
                'statEffect' : None,
                'statEffectProb' : 0,
                'statEffected' : None,
                'priority' : 0,
                'count' : 10,
                'target' : [1],
                'recoil' : 0
}

sleeppowder_dict = {
                'name' : 'Sleep Powder',
                'accuracy' : 60,
                'power' : 0,
                'type' : 'normal',
                'kind' : 'status',
                'statEffect' : 'sleep',
                'statEffectProb' : 1,
                'statEffected' : None,
                'priority' : 0,
                'count' : 20,
                'target' : [1],
                'recoil' : 0
}

moves_dict = {'Thunderbolt' : Moves(thunderbolt_dict),
              'Quick Attack' : Moves(quickattack_dict),
              'Thunder Wave' : Moves(thunderwave_dict),
              'Growl' : Moves(growl_dict),
              'Ember' : Moves(ember_dict),
              'Smoke Screen' : Moves(smokescreen_dict),
              'Scratch' : Moves(scratch_dict),
              'Toxic' : Moves(toxic_dict),
              'Tackle' : Moves(tackle_dict),
              'Vine Whip' : Moves(vinewhip_dict),
              'Mega Drain' : Moves(megadrain_dict),
              'Dragon Rage' : Moves(dragonrage_dict),
              'Aurora Beam' : Moves(aurorabeam_dict),
              'Body Slam' : Moves(bodyslam_dict),
              'Flamethrower' : Moves(flamethrower_dict),
              'Surf' : Moves(surf_dict),
              'Hydro Pump' : Moves(hydropump_dict),
              'Thunder' : Moves(thunder_dict),
              'Ice Beam' : Moves(icebeam_dict),
              'Submission' : Moves(submission_dict),
              'Sludge' : Moves(sludge_dict),
              'Earthquake' : Moves(earthquake_dict),
              'Drill Peck' : Moves(drillpeck_dict),
              'Psybeam' : Moves(psybeam_dict),
              'Psychic' : Moves(psychic_dict),
              'Leech Life' : Moves(leechlife_dict),
              'Rock Slide' : Moves(rockslide_dict),
              'Night Shade' : Moves(nightshade_dict),
              'Sleep Powder' : Moves(sleeppowder_dict)
            }


mv_list = moves_dict.keys()

num_pokemon = 12
num_moves = 27

full_pokemon_moves_assignment = {
    'Venusaur' : [moves_dict[move] for move in ['Sludge','Growl','Vine Whip','Mega Drain']],
    'Charizard' : [moves_dict[move] for move in ['Flamethrower','Smoke Screen','Dragon Rage','Ember']],
    'Blastoise' : [moves_dict[move] for move in ['Surf','Hydro Pump','Ice Beam','Submission']],
    'Butterfree' : [moves_dict[move] for move in ['Psychic','Toxic','Leech Life','Tackle']],
    'Beedrill' : [moves_dict[move] for move in ['Drill Peck','Sludge','Toxic','Leech Life']],
    'Pidgeot' : [moves_dict[move] for move in ['Drill Peck','Smoke Screen','Tackle','Quick Attack']],
    'Fearow' : [moves_dict[move] for move in ['Drill Peck','Quick Attack','Body Slam','Growl']],
    'Arbok' : [moves_dict[move] for move in ['Sludge','Toxic','Vine Whip','Scratch']],
    'Raichu' : [moves_dict[move] for move in ['Thunder','Thunderbolt','Thunder Wave','Quick Attack']],
    'Sandslash' : [moves_dict[move] for move in ['Smoke Screen','Earthquake','Tackle','Rock Slide']],
    'Nidoking' : [moves_dict[move] for move in ['Earthquake','Sludge','Toxic','Rock Slide']],
    'Clefable' : [moves_dict[move] for move in ['Psybeam','Body Slam','Aurora Beam','Night Shade']]
}

small_pokemon_moves_assignment = {
    'Venusaur' : [moves_dict[move] for move in ['Sludge','Growl']],
    'Charizard' : [moves_dict[move] for move in ['Flamethrower','Smoke Screen']],
    'Blastoise' : [moves_dict[move] for move in ['Surf','Hydro Pump']],
    'Butterfree' : [moves_dict[move] for move in ['Psychic','Toxic']],
    'Beedrill' : [moves_dict[move] for move in ['Drill Peck','Sludge']],
    'Pidgeot' : [moves_dict[move] for move in ['Drill Peck','Smoke Screen']],
    'Fearow' : [moves_dict[move] for move in ['Drill Peck','Quick Attack']],
    'Arbok' : [moves_dict[move] for move in ['Sludge','Toxic','Vine Whip']],
    'Raichu' : [moves_dict[move] for move in ['Thunder','Thunderbolt']],
    'Sandslash' : [moves_dict[move] for move in ['Smoke Screen','Earthquake']],
    'Nidoking' : [moves_dict[move] for move in ['Earthquake','Sludge']],
    'Clefable' : [moves_dict[move] for move in ['Psybeam','Body Slam']]
}

pokemon_moves_assignment = full_pokemon_moves_assignment

type_dict = {
    'normal' : 0,
    'fight' : 1,
    'flying' : 2,
    'poison' : 3,
    'ground' : 4,
    'rock' : 5,
    'bug' : 6,
    'ghost' : 7, 
    'fire' : 8,
    'water' : 9,
    'grass' : 10, 
    'electra' : 11,
    'psychc' : 12,
    'ice' : 13, 
    'dragon' : 14
}

kind_dict = {
    'physical' : 0,
    'special' : 1,
    'status' : 2
}

status_effect_dict = {
    'burn' : 1,
    'freeze' : 2,
    'paralysis' : 3,
    'poison' : 4,
    'sleep' : 5,
    'reduce' : 6
}

status_dict = {
    'hp' : 1,
    'attack' : 2,
    'defense' : 3,
    'special attack' : 4,
    'special defense' : 5,
    'speed' : 6,
    'evasion' : 7,
    'accuracy' : 8
}


venusaur_dict = {
"name" : 'Venusaur',
"level" : 50,
"type" : ['poison', 'grass'], 
"hp" : 155,
"hp_max" : 155,
"attack" : [122, 0],
"defense" : [103, 0],
"sp_attack" : [108, 0], 
"sp_defense" : [120, 0],
"speed" : [100, 0],
"accuracy" : [100, 0],
"stat" : None, 
"moves" : pokemon_moves_assignment['Venusaur']
}   


charizard_dict = {
"name" : 'Charizard',
"level" : 50,
"type" : ['fire', 'flying'], 
"hp" : 153,
"hp_max" : 153,
"attack" : [114, 0],
"defense" : [98, 0],
"sp_attack" : [116, 0], 
"sp_defense" : [105, 0], 
"speed" : [120, 0],
"accuracy" : [100, 0],
"stat" : None,
"moves" : pokemon_moves_assignment['Charizard']
}        

blastoise_dict = {
"name" : 'Blastoise',
"level" : 50,
"type" : ['water'],
"hp" : 154,
"hp_max" : 154,
"attack" : [113, 0],
"defense" : [120, 0],
"sp_attack" : [94, 0],
"sp_defense" : [125, 0],
"speed" : [98, 0],
"accuracy" : [100, 0],
"stat" : None,
"moves" : pokemon_moves_assignment['Blastoise']
}        

butterfree_dict = {
"name" : 'Butterfree',
"level" : 50,
"type" : ['bug', 'flying'],
"hp" : 135,
"hp_max" : 135,
"attack" : [71, 0],
"defense" : [70, 0],
"sp_attack" : [99, 0],
"sp_defense" : [100, 0],
"speed" : [90, 0],
"accuracy" : [100, 0],
"stat" : None,
"moves" : pokemon_moves_assignment['Butterfree']
}        

beedrill_dict = {
"name" : 'Beedrill',
"level" : 50,
"type" : ['bug', 'poison'],
"hp" : 140,
"hp_max" : 140,
"attack" : [121, 0],
"defense" : [60, 0],
"sp_attack" : [58, 0],
"sp_defense" : [100, 0],
"speed" : [95, 0],
"accuracy" : [100, 0],
"stat" : None,
"moves" : pokemon_moves_assignment['Beedrill']
}        

pidgeot_dict = {
"name" : 'Pidgeot',
"level" : 50,
"type" : ['flying', 'normal'],
"hp" : 158,
"hp_max" : 158,
"attack" : [110, 0],
"defense" : [95, 0],
"sp_attack" : [81, 0],
"sp_defense" : [90, 0],
"speed" : [121, 0],
"accuracy" : [100, 0],
"stat" : None,
"moves" : pokemon_moves_assignment['Pidgeot']
}        

fearow_dict = {
"name" : 'Fearow',
"level" : 50,
"type" : ['flying', 'normal'], 
"hp" : 140,
"hp_max" : 140, 
"attack" : [121,  0],
"defense" : [85, 0], 
"sp_attack" : [72, 0], 
"sp_defense" : [81, 0],
"speed" : [120, 0],
"accuracy" : [100, 0],
"stat" : None,
"moves" : pokemon_moves_assignment['Fearow']
}        

arbok_dict = {
"name" : 'Arbok',
"level" : 50,
"type" : ['poison'],
"hp" : 135,
"hp_max" : 135,
"attack" : [126, 0],
"defense" : [89, 0],
"sp_attack" : [76, 0],
"sp_defense" : [99, 0],
"speed" : [100, 0],
"accuracy" : [100, 0],
"stat" : None,
"moves" : pokemon_moves_assignment['Arbok']
}        

raichu_dict = {
"name" : 'Raichu',
"level" : 50,
"type" : ['electra'],
"hp" : 135,
"hp_max" : 135,
"attack" : [121, 0],
"defense" : [75, 0],
"sp_attack" : [99, 0],
"sp_defense" : [100, 0],
"speed" : [130, 0],
"accuracy" : [100, 0],
"stat" : None,
"moves" : pokemon_moves_assignment['Raichu']
}        

sandslash_dict = {
"name" : 'Sandslash',
"level" : 50,
"type" : ['ground'],
"hp" : 150,
"hp_max" : 150, 
"attack" : [132, 0],
"defense" : [130, 0],
"sp_attack" : [58, 0],
"sp_defense" : [75, 0],
"speed" : [85, 0],
"accuracy" : [100, 0],
"stat" : None,
"moves" : pokemon_moves_assignment['Sandslash']
}        

nidoking_dict = {
"name" : 'Nidoking',
"level" : 50,
"type" : ['ground', 'poison'],
"hp" : 156,
"hp_max" : 156,
"attack" : [134, 0],
"defense" : [97, 0],
"sp_attack" : [94, 0],
"sp_defense" : [95, 0],
"speed" : [105, 0],
"accuracy" : [100, 0],
"stat" : None,
"moves" : pokemon_moves_assignment['Nidoking']
}        

clefable_dict = {
"name" : 'Clefable',
"level" : 50,
"type" : ['normal'],
"hp" : 170,
"hp_max" : 170,
"attack" : [99, 0],
"defense" : [93, 0],
"sp_attack" : [103, 0],
"sp_defense" : [110, 0],
"speed" : [80, 0],
"accuracy" : [100, 0],
"stat" : None,
"moves" : pokemon_moves_assignment['Clefable']
}        
