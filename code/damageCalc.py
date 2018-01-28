from numpy import random
from pokemon_data import *
import numpy as np


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


def DamageCalc(poke, oppPoke, move):
#     """
#     Takes two pokemon and the first pokemon's move choice
#     Then calculates the damage and status effects to be applied.
#     """
    def modifier(moveType,pokeType,oppType):
#     """
#     Calculates super effective or non effective moves and stab boost based on inputs
#     """
        td = {
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
        if pokeType == moveType:
            stab = 1.5
        else:
            stab = 1
    
        effmat = [[1,  1,  1,  1,  1, .5,  1,  0.25,  1,  1,  1,  1,  1,  1,  1],
                  [2,  1, .5, .5,  1,  2, .5,  0.25,  1,  1,  1,  1, .5,  2,  1],
                  [1,  2,  1,  1,  1, .5,  2,  1,  1,  1,  2, .5,  1,  1,  1],
                  [1,  1,  1, .5, .5, .5,  2, .5,  1,  1,  2,  1,  1,  1,  1],
                  [1,  1,  0.25,  2,  1,  2, .5,  1,  2,  1, .5,  2,  1,  1,  1],
                  [1, .5,  2,  1, .5,  1,  2,  1,  2,  1,  1,  1,  1,  2,  1],
                  [1, .5, .5,  2,  1,  1,  1, .5, .5,  1,  2,  1,  2,  1,  1],
                  [0.25,  1,  1,  1,  1,  1,  1,  2,  1,  1,  1,  1,  0.25,  1,  1],
                  [1,  1,  1,  1,  1, .5,  2,  1, .5, .5,  2,  1,  1,  2, .5],
                  [1,  1,  1,  1,  2,  2,  1,  1,  2, .5, .5,  1,  1,  1, .5],
                  [1,  1, .5, .5,  2,  2, .5,  1, .5,  2, .5,  1,  1,  1, .5],
                  [1,  1,  2,  1,  0.25,  1,  1,  1,  1,  2, .5, .5,  1,  1, .5],
                  [1,  2,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1, .5,  1,  1],
                  [1,  1,  2,  1,  2,  1,  1,  1,  1, .5,  2,  1,  1, .5,  2],
                  [1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  2]]
     
        effective = sum(effmat[td[moveType]][td[ot]] for ot in oppType)
        noise = .15*random.uniform()+.85
        mod = stab*effective*noise
        return mod
    

    damage = 0
    eff = None
    stat = None
    #Some attacks cause stats to change. In gen 1, this resulted in increasing/lowering either the numerator or denominator
    stage = [2./8,  2./7,  2./6,  2./5,  2./4,  2./3,  2./2,  3./2,  4./2,  5./2,  6./2,  7./2,  8./2]
    acc = move.accuracy*stage[poke.accuracy[1]+6]
    attack = poke.attack[0]

    if poke.stat == 'paralysis': #if the attacking pokemon is paralyzed it has a 25% chance of doing nothing
        if random.uniform() <= 0.25:
            acc = -1
    elif poke.stat == 'burn': #if the attacking pokemon is burned the attack is half as powerful
        attack /= 2
    elif poke.stat == 'freeze' or poke.stat == 'sleep': #if the attacking pokemon is asleep or frozen, it can't attack
        acc = -1
        
    if random.uniform()*100 <= acc:
        if move.kind == 'physical': #if the move is physical, use the physical attack and defense stats else use special attack / defense stats
            damage = ((2*poke.level+10)/250.0*attack*stage[poke.attack[1]+6]/(oppPoke.defense[0]*stage[oppPoke.defense[1]+6])*move.power+2)*modifier(move.type,poke.type,oppPoke.type)
        elif move.kind == 'special': #special attacks
            damage =((2*poke.level+10)/250.0*poke.sp_attack[0]*stage[poke.sp_attack[1]+6]/(oppPoke.sp_defense[0]*stage[oppPoke.sp_defense[1]+6])*move.power+2)*modifier(move.type,poke.type,oppPoke.type)
        
        #apply any chance of status effect
        if move.statEffectProb!=0:
            if random.uniform() <= move.statEffectProb:
                if move.statEffect != 'reduce': #stat<6 are stage changing stats. they change attack of defense etc. other stat changes are status effects thus these are handled differently
                    eff = move.statEffect
                    #how do we deal with wrap, fire spin, leech seed, etc?
                else:
                    stat = move.statEffected
    
    damage = np.floor(damage)
    # damage (reduces HP), stat effect to the oppPoke (status effected of the oppPok e.g., hp, defense, attack) eff (status to be applied to the oppPoke, e.g., paralysis, sleep)
    return (damage, stat, eff)

def Recoil(move, damage):
    heal = np.ceil(damage*move.recoil)
    eff = None
    stat = None
    if 1 in move.target and damage != 0:
        acc = 1
    else:
        acc = move.accuracy

    if random.rand()*100 <= acc:
        if random.rand() <= move.statEffectProb:
            if move.statEffect is not 'reduce':
                eff = move.statEffect
            else:
                stat = move.statEffected

    return (heal, stat, eff)










