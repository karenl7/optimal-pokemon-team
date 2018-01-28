from __future__ import division
from pokemon_data import *
from damageCalc import *
import random, math, copy, itertools, collections
import numpy as np


full_pd = {
    'Venusaur' : Pokemon(venusaur_dict),
    'Charizard' : Pokemon(charizard_dict),
    'Blastoise' : Pokemon(blastoise_dict),
    'Butterfree' : Pokemon(butterfree_dict),
    'Beedrill' : Pokemon(beedrill_dict),
    'Pidgeot' : Pokemon(pidgeot_dict),
    'Fearow' : Pokemon(fearow_dict),
    'Arbok' : Pokemon(arbok_dict),
    'Raichu' : Pokemon(raichu_dict),
    'Sandslash' : Pokemon(sandslash_dict),
    'Nidoking' : Pokemon(nidoking_dict),
    'Clefable' : Pokemon(clefable_dict)
}

small_pd = {
    'Butterfree' : Pokemon(butterfree_dict),
    'Pidgeot' : Pokemon(pidgeot_dict),
    'Arbok' : Pokemon(arbok_dict),
    'Clefable' : Pokemon(clefable_dict)
}

pd = full_pd

md = {'Thunderbolt' : Moves(thunderbolt_dict),
    'Quick Attack' : Moves(quickattack_dict),
    'Thunder Wave' : Moves(thunderwave_dict),
    'Growl' : Moves(growl_dict),
    'Ember' : Moves(ember_dict),
    'Smoke Screen' : Moves(smokescreen_dict),
    'Scratch' : Moves(scratch_dict),
    'Toxic' : Moves(toxic_dict),
    'Tackle' : Moves(tackle_dict),
    'Vine Whip' : Moves(vinewhip_dict),
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



# $$$$$$$\   $$$$$$\ $$$$$$$$\ $$$$$$$$\ $$\       $$$$$$$$\       $$\      $$\ $$$$$$$\  $$$$$$$\  
# $$  __$$\ $$  __$$\\__$$  __|\__$$  __|$$ |      $$  _____|      $$$\    $$$ |$$  __$$\ $$  __$$\ 
# $$ |  $$ |$$ /  $$ |  $$ |      $$ |   $$ |      $$ |            $$$$\  $$$$ |$$ |  $$ |$$ |  $$ |
# $$$$$$$\ |$$$$$$$$ |  $$ |      $$ |   $$ |      $$$$$\          $$\$$\$$ $$ |$$ |  $$ |$$$$$$$  |
# $$  __$$\ $$  __$$ |  $$ |      $$ |   $$ |      $$  __|         $$ \$$$  $$ |$$ |  $$ |$$  ____/ 
# $$ |  $$ |$$ |  $$ |  $$ |      $$ |   $$ |      $$ |            $$ |\$  /$$ |$$ |  $$ |$$ |      
# $$$$$$$  |$$ |  $$ |  $$ |      $$ |   $$$$$$$$\ $$$$$$$$\       $$ | \_/ $$ |$$$$$$$  |$$ |      
# \_______/ \__|  \__|  \__|      \__|   \________|\________|      \__|     \__|\_______/ \__|      
                                                                                                  
                                                                                                                                                                                                                                                                                                              
class PokemonBattleMDP:
    def __init__(self, ownPoke, oppPoke, trans=(None,None), hp_bin=10.0):
        self.ownPoke = ownPoke
        self.oppPoke = oppPoke
        self.ownSleepCount = 0
        self.oppPokeSleepCount = 0
        self.bin = hp_bin
        self.td = trans[0]
        self.rd = trans[1]

    def startState(self):
        return ((self.ownPoke.name, self.bin, self.ownPoke.stat), (self.oppPoke.name, self.bin, self.oppPoke.stat))

    def actions(self, state, oppPolicy=None):
        global pd
        ownActions = pd[state[0][0]].moves
        if oppPolicy:
            # must be a list
            oppActions = oppPolicy(state)
        else:
            oppActions = pd[state[1][0]].moves
        return [(a0, a1) for a0 in ownActions for a1 in oppActions]

    # def succAndProbReward(self, state, action, refine=10):
    #     global pd
    #     if len(self.td[state]) == 0:
    #         for i in range(refine):
    #             p1 = copy.copy(pd[state[0][0]])
    #             p2 = copy.copy(pd[state[1][0]])
    #             pp1 = self.ownPoke
    #             pp2 = self.oppPoke
    #             self.ownPoke = p1
    #             self.oppPoke = p2
    #             ownHP, oppHP = self.ownPoke.hp, self.oppPoke.hp
    #             self.ownPoke.hp = state[0][1]/self.bin*self.ownPoke.hp_max
    #             self.oppPoke.hp = state[1][1]/self.bin*self.oppPoke.hp_max
    #             sar = self.pokemonMakeMove(state, action)
    #             self.ownPoke.hp, self.oppPoke.hp = ownHP, oppHP
    #             self.ownPoke = pp1
    #             self.oppPoke = pp2
    #             newState = sar[0]
    #             reward = sar[2]
    #             self.td[state][action][newState] += 1
    #             # print self.td[state][action][newState]
    #             self.rd[state][action][newState].append(reward)
    #     total = sum(self.td[state][action].values())
    #     results = []
    #     for ns in self.td[state][action]:
    #         newState = ns
    #         prob = self.td[state][action][ns]/total
    #         reward = float(sum(self.rd[state][action][ns]))/len(self.rd[state][action][ns])
    #         results.append((ns, prob, reward))
    #     return results


    def computeStates(self):
        global pd
        self.states = set()
        for p1 in pd:
            for p2 in pd:
                for i in range(int(self.bin)):
                    for j in range(int(self.bin)):
                        for stat1 in [None, 'burn', 'paralysis', 'poison']:
                            for stat2 in [None, 'burn', 'paralysis', 'poison']:
                                self.states.add(((p1, i, stat1), (p2, j, stat2)))

    def pokemonMakeMove(self, state, action, verbose=0):
        global pd
        # own poke goes first
        ownState, oppState = state[0], state[1]
        if self.ownPoke.stat == "paralysis":
            if verbose:
                print '%s has paralysis, speed has decreased'%(self.ownPoke.name)
            ownPokeSpeed = self.ownPoke.speed[0] / 4.0
        else: ownPokeSpeed = self.ownPoke.speed[0]
        if self.oppPoke.stat == "paralysis":
            if verbose:
                print '%s has paralysis, speed has decreased'%(self.oppPoke.name)
            oppPokeSpeed = self.oppPoke.speed[0] / 4.0
        else: oppPokeSpeed = self.oppPoke.speed[0]

        if ownPokeSpeed == oppPokeSpeed:
            if np.random.rand() > 0.5:
                ownPokeSpeed += 0.01

        if ownPokeSpeed > oppPokeSpeed:
            if verbose:
                print '%s (EGO PLAYER) goes first'%(self.ownPoke.name)
            # if ownPoke is faster
            # ownPoke goes first
            if self.ownSleepCount!=0:
                self.ownSleepCount-=1
                if self.ownSleepCount==0:
                    self.ownPoke.stat=None
            if 1 in action[0].target:
                (damage, stat, eff) = DamageCalc(self.ownPoke, self.oppPoke, action[0])
                self.oppPoke.hp -= damage
                
                if eff is not None and self.oppPoke.stat is None:
                    if eff == 'sleep':
                        self.oppPokeSleepCount = np.ceil((7*np.random.rand()))
                    self.oppPoke.stat = eff

                if stat == 'attack' and self.oppPoke.attack[1] > -6:
                    if verbose:
                        print '%s attack has decreased ' % (self.oppPoke.name)
                    self.oppPoke.attack[1] -= 1
                if stat == 'defense' and self.oppPoke.defense[1] > -6:
                    if verbose:
                        print '%s defense has decreased ' % (self.oppPoke.name)
                    self.oppPoke.defense[1] -= 1
                if stat == 'special attack' and self.oppPoke.sp_attack[1] > -6:
                    if verbose:
                        print '%s special attack has decreased ' % (self.oppPoke.name)
                    self.oppPoke.sp_attack[1] -= 1
                if stat == 'special defense' and self.oppPoke.sp_defense[1] > -6:
                    if verbose:
                        print '%s special defense has decreased ' % (self.oppPoke.name)
                    self.oppPoke.sp_defense[1] -= 1
                if stat == 'speed' and self.oppPoke.speed[1] > -6:
                    if verbose:
                        print '%s speed has decreased ' % (self.oppPoke.name)
                    self.oppPoke.speed[1] -= 1
                if stat == 'accuracy' and self.oppPoke.accuracy[1] > -6:
                    if verbose:
                        print '%s accuracy has decreased ' % (self.oppPoke.name)
                    self.oppPoke.accuracy[1] -= 1
                
                oppState = (state[1][0], getHPRatio(self.oppPoke), self.oppPoke.stat)
                if verbose:
                    print '%s uses %s against %s. -------  %s hp drops to %i' % (self.ownPoke.name, action[0].name, self.oppPoke.name, self.oppPoke.name, max([self.oppPoke.hp,0]))
                    
                if self.isEnd((ownState, oppState)):
                    if verbose:
                        print '%s died ' % (self.oppPoke.name)
                    return ((ownState, oppState), (action[0], None), 100)

            if 0 in action[0].target:
                heal, stat, eff = Recoil(action[0], damage)
                self.ownPoke.hp = min([self.ownPoke.hp + heal, self.ownPoke.hp_max])
                ownState = (state[0][0], getHPRatio(self.ownPoke), state[0][2])
                if self.isEnd((ownState, oppState)):
                    if verbose:
                        print '%s died from recoil' % (self.ownPoke.name)
                    return ((ownState, oppState), (action[0], None), -100)
                if eff is not None and self.ownPoke.stat is None:
                    if eff == 'sleep':
                        self.ownSleepCount = np.ceil((7*np.random.rand()))
                    self.ownPoke.stat = eff
                if stat == 'attack' and self.ownPoke.attack[1] < 6:
                    if verbose:
                        print '%s speed has increased ' % (self.ownPoke.name)
                    self.ownPoke.attack[1] += 1
                if stat == 'defense' and self.ownPoke.defense:
                    if verbose:
                        print '%s defense has increased ' % (self.ownPoke.name)
                    self.ownPoke.defense[1] += 1
                if stat == 'special attack' and self.ownPoke.sp_attack[1] < 6:
                    if verbose:
                        print '%s special attack has increased ' % (self.ownPoke.name)
                    self.ownPoke.sp_attack[1] += 1
                if stat == 'special defense' and self.ownPoke.sp_defense[1] < 6:
                    if verbose:
                        print '%s special defense has increased ' % (self.ownPoke.name)
                    self.ownPoke.sp_defense[1] += 1
                if stat == 'speed' and self.ownPoke.speed[1] < 6:
                    if verbose:
                        print '%s speed has increased ' % (self.ownPoke.name)
                    self.ownPoke.speed[1] += 1
                if stat == 'accuracy' and self.ownPoke.accuracy[1] < 6:
                    if verbose:
                        print '%s accuracy has increased ' % (self.ownPoke.name)
                    self.ownPoke.accuracy[1] += 1
                    

            # oppPoke goes second
            if self.oppPokeSleepCount!=0:
                self.oppPokeSleepCount-=1
                if self.oppPokeSleepCount==0:
                    self.oppPoke.stat=None
            if 1 in action[1].target:
                (damage, stat, eff) = DamageCalc(self.oppPoke, self.ownPoke, action[1])
                self.ownPoke.hp -= damage
                
                if eff is not None and self.ownPoke.stat is None:
                    if eff == 'sleep':
                        self.ownPokeSleepCount = np.ceil((7*np.random.rand()))
                    self.ownPoke.stat = eff

                if stat == 'attack' and self.ownPoke.attack[1] > -6:
                    if verbose:
                        print '%s attack has decreased ' % (self.ownPoke.name)
                    self.ownPoke.attack[1] -= 1
                if stat == 'defense' and self.ownPoke.defense:
                    if verbose:
                        print '%s defense has decreased ' % (self.ownPoke.name)
                    self.ownPoke.defense[1] -= 1
                if stat == 'special attack' and self.ownPoke.sp_attack[1] > -6:
                    if verbose:
                        print '%s special attack has decreased ' % (self.ownPoke.name)
                    self.ownPoke.sp_attack[1] -= 1
                if stat == 'special defense' and self.ownPoke.sp_defense[1] > -6:
                    if verbose:
                        print '%s special defense has decreased ' % (self.ownPoke.name)
                    self.ownPoke.sp_defense[1] -= 1
                if stat == 'speed' and self.ownPoke.speed[1] > -6:
                    if verbose:
                        print '%s speed has decreased ' % (self.ownPoke.name)
                    self.ownPoke.speed[1] -= 1
                if stat == 'accuracy' and self.ownPoke.accuracy[1] > -6:
                    if verbose:
                        print '%s accuracy has decreased ' % (self.ownPoke.name)
                    self.ownPoke.accuracy[1] -= 1
                
                ownState = (state[0][0], getHPRatio(self.ownPoke), self.ownPoke.stat)
                if verbose:
                    print '%s uses %s against %s. -------  %s hp drops to %i' % (self.oppPoke.name, action[1].name, self.ownPoke.name, self.ownPoke.name, max([self.ownPoke.hp,0]))
                if self.isEnd((ownState, oppState)):
                    if verbose:
                        print '%s died ' % (self.ownPoke.name)
                    return ((ownState, oppState), (action[0], action[1]), -100)

            if 0 in action[1].target:
                heal, stat, eff = Recoil(action[1], damage)
                self.oppPoke.hp = min([self.oppPoke.hp + heal, self.oppPoke.hp_max])
                oppState = (state[1][0], getHPRatio(self.oppPoke), state[1][2])
                if self.isEnd((ownState, oppState)):
                    if verbose:
                        print '%s died from recoil' % (self.oppPoke.name)
                    return ((ownState, oppState), (action[0], action[1]), 100)
                if eff is not None and self.oppPoke.stat is None:
                    if eff == 'sleep':
                        self.oppSleepCount = np.ceil((7*np.random.rand()))
                    self.oppPoke.stat = eff
                if stat == 'attack' and self.oppPoke.attack[1] < 6:
                    if verbose:
                        print '%s attack has increased ' % (self.oppPoke.name)
                    self.oppPoke.attack[1] += 1
                if stat == 'defense' and self.oppPoke.defense[1] < 6:
                    if verbose:
                        print '%s defense has increased ' % (self.oppPoke.name)
                    self.oppPoke.defense[1] += 1
                if stat == 'special attack' and self.oppPoke.sp_attack[1] < 6:
                    if verbose:
                        print '%s special attack has increased ' % (self.oppPoke.name)
                    self.oppPoke.sp_attack[1] += 1
                if stat == 'special defense' and self.oppPoke.sp_defense[1] < 6:
                    if verbose:
                        print '%s special defense has increased ' % (self.oppPoke.name)
                    self.oppPoke.sp_defense[1] += 1
                if stat == 'speed' and self.oppPoke.speed[1] < 6:
                    self.oppPoke.speed[1] += 1
                if stat == 'accuracy' and self.oppPoke.accuracy[1] < 6:
                    self.oppPoke.accuracy[1] += 1

            if self.ownPoke.stat == 'burn' or self.ownPoke.stat == 'poison':
                self.ownPoke.hp -= max([np.floor(self.ownPoke.hp_max/16.0), 1])
                ownState = (state[0][0], getHPRatio(self.ownPoke), state[0][2])
                if verbose:
                    print '%s is %s-ed. -------  %s hp drops to %i' % (self.ownPoke.name, self.ownPoke.stat, self.ownPoke.name, max([ownState[1],0]))
                if self.isEnd((ownState, oppState)):
                    if verbose:
                        print '%s died ' % (self.ownPoke.name)
                    return ((ownState, oppState), (action[0], action[1]), -100)
        else:
            # if oppPoke is faster
            # oppPoke goes first
            if verbose:
                print '%s (OPPONENT GOES FIRST) goes first'%(self.oppPoke.name)
            if self.oppPokeSleepCount!=0:
                self.oppPokeSleepCount-=1
                if self.oppPokeSleepCount==0:
                    self.oppPoke.stat=None
            if 1 in action[1].target:
                (damage, stat, eff) = DamageCalc(self.oppPoke, self.ownPoke, action[1])
                self.ownPoke.hp -= damage
                
                if eff is not None and self.ownPoke.stat is None:
                    if eff == 'sleep':
                        self.ownPokeSleepCount = np.ceil((7*np.random.rand()))
                    self.ownPoke.stat = eff

                if stat == 'attack' and self.ownPoke.attack[1] > -6:
                    if verbose:
                        print '%s attack has decreased ' % (self.ownPoke.name)
                    self.ownPoke.attack[1] -= 1
                if stat == 'defense' and self.ownPoke.defense:
                    if verbose:
                        print '%s defense has decreased ' % (self.ownPoke.name)
                    self.ownPoke.defense[1] -= 1
                if stat == 'special attack' and self.ownPoke.sp_attack[1] > -6:
                    if verbose:
                        print '%s special attack has decreased ' % (self.ownPoke.name)
                    self.ownPoke.sp_attack[1] -= 1
                if stat == 'special defense' and self.ownPoke.sp_defense[1] > -6:
                    if verbose:
                        print '%s special defense has decreased ' % (self.ownPoke.name)
                    self.ownPoke.sp_defense[1] -= 1
                if stat == 'speed' and self.ownPoke.speed[1] > -6:
                    if verbose:
                        print '%s speed has decreased ' % (self.ownPoke.name)
                    self.ownPoke.speed[1] -= 1
                if stat == 'accuracy' and self.ownPoke.accuracy[1] > -6:
                    if verbose:
                        print '%s accuracy has decreased ' % (self.ownPoke.name)
                    self.ownPoke.accuracy[1] -= 1
                    
                ownState = (state[0][0], getHPRatio(self.ownPoke), self.ownPoke.stat)
                if verbose:
                    print '%s uses %s against %s. -------  %s hp drops to %i' % (self.oppPoke.name, action[1].name, self.ownPoke.name, self.ownPoke.name, max([self.ownPoke.hp,0]))
                if self.isEnd((ownState, oppState)):
                    if verbose:
                        print '%s died ' % (self.ownPoke.name)
                    return ((ownState, oppState), (action[0], action[1]), -100)

            if 0 in action[1].target:
                heal, stat, eff = Recoil(action[1], damage)
                self.oppPoke.hp = min([self.oppPoke.hp + heal, self.oppPoke.hp_max])
                oppState = (state[1][0], getHPRatio(self.oppPoke), state[1][2])
                if self.isEnd((ownState, oppState)):
                    if verbose:
                        print '%s died from recoil' % (self.oppPoke.name)
                    return ((ownState, oppState), (action[0], action[1]), 100)
                if eff is not None and self.oppPoke.stat is None:
                    if eff == 'sleep':
                        self.oppSleepCount = np.ceil((7*np.random.rand()))
                    self.oppPoke.stat = eff
                if stat == 'attack' and self.oppPoke.attack[1] < 6:
                    if verbose:
                        print '%s attack has increased ' % (self.oppPoke.name)
                    self.oppPoke.attack[1] += 1
                if stat == 'defense' and self.oppPoke.defense[1] < 6:
                    if verbose:
                        print '%s defense has increased ' % (self.oppPoke.name)
                    self.oppPoke.defense[1] += 1
                if stat == 'special attack' and self.oppPoke.sp_attack[1] < 6:
                    if verbose:
                        print '%s special attack has increased ' % (self.oppPoke.name)
                    self.oppPoke.sp_attack[1] += 1
                if stat == 'special defense' and self.oppPoke.sp_defense[1] < 6:
                    if verbose:
                        print '%s special defense has increased ' % (self.oppPoke.name)
                    self.oppPoke.sp_defense[1] += 1
                if stat == 'speed' and self.oppPoke.speed[1] < 6:
                    self.oppPoke.speed[1] += 1
                if stat == 'accuracy' and self.oppPoke.accuracy[1] < 6:
                    self.oppPoke.accuracy[1] += 1
            # ownPoke goes second
            if self.ownSleepCount!=0:
                self.ownSleepCount-=1
                if self.ownSleepCount==0:
                    self.ownPoke.stat=None
            if 1 in action[0].target:
                (damage, stat, eff) = DamageCalc(self.ownPoke, self.oppPoke, action[0])
                self.oppPoke.hp -= damage

                if eff is not None and self.oppPoke.stat is None:
                    if eff == 'sleep':
                        self.oppPokeSleepCount = np.ceil((7*np.random.rand()))
                    self.oppPoke.stat = eff

                if stat == 'attack' and self.oppPoke.attack[1] > -6:
                    if verbose:
                        print '%s attack has decreased ' % (self.oppPoke.name)
                    self.oppPoke.attack[1] -= 1
                if stat == 'defense' and self.oppPoke.defense[1] > -6:
                    if verbose:
                        print '%s defense has decreased ' % (self.oppPoke.name)
                    self.oppPoke.defense[1] -= 1
                if stat == 'special attack' and self.oppPoke.sp_attack[1] > -6:
                    if verbose:
                        print '%s special attack has decreased ' % (self.oppPoke.name)
                    self.oppPoke.sp_attack[1] -= 1
                if stat == 'special defense' and self.oppPoke.sp_defense[1] > -6:
                    if verbose:
                        print '%s special defense has decreased ' % (self.oppPoke.name)
                    self.oppPoke.sp_defense[1] -= 1
                if stat == 'speed' and self.oppPoke.speed[1] > -6:
                    if verbose:
                        print '%s speed has decreased ' % (self.oppPoke.name)
                    self.oppPoke.speed[1] -= 1
                if stat == 'accuracy' and self.oppPoke.accuracy[1] > -6:
                    if verbose:
                        print '%s accuracy has decreased ' % (self.oppPoke.name)
                    self.oppPoke.accuracy[1] -= 1
                    
                oppState = (state[1][0], getHPRatio(self.oppPoke), self.oppPoke.stat)
                if verbose:
                    print '%s uses %s against %s. -------  %s hp drops to %i' % (self.ownPoke.name, action[0].name, self.oppPoke.name, self.oppPoke.name, max([self.oppPoke.hp,0]))
                if self.isEnd((ownState, oppState)):
                    if verbose:
                        print '%s died ' % (self.oppPoke.name)
                    return ((ownState, oppState), (action[0], None), 100)

            if 0 in action[0].target:
                heal, stat, eff = Recoil(action[0], damage)
                self.ownPoke.hp = min([self.ownPoke.hp + heal, self.ownPoke.hp_max])
                ownState = (state[0][0], getHPRatio(self.ownPoke), state[0][2])
                if self.isEnd((ownState, oppState)):
                    if verbose:
                        print '%s died from recoil' % (self.ownPoke.name)
                    return ((ownState, oppState), (action[0], None), -100)
                if eff is not None and self.ownPoke.stat is None:
                    if eff == 'sleep':
                        self.ownSleepCount = np.ceil((7*np.random.rand()))
                    self.ownPoke.stat = eff
                if stat == 'attack' and self.ownPoke.attack[1] < 6:
                    if verbose:
                        print '%s speed has increased ' % (self.ownPoke.name)
                    self.ownPoke.attack[1] += 1
                if stat == 'defense' and self.ownPoke.defense:
                    if verbose:
                        print '%s defense has increased ' % (self.ownPoke.name)
                    self.ownPoke.defense[1] += 1
                if stat == 'special attack' and self.ownPoke.sp_attack[1] < 6:
                    if verbose:
                        print '%s special attack has increased ' % (self.ownPoke.name)
                    self.ownPoke.sp_attack[1] += 1
                if stat == 'special defense' and self.ownPoke.sp_defense[1] < 6:
                    if verbose:
                        print '%s special defense has increased ' % (self.ownPoke.name)
                    self.ownPoke.sp_defense[1] += 1
                if stat == 'speed' and self.ownPoke.speed[1] < 6:
                    if verbose:
                        print '%s speed has increased ' % (self.ownPoke.name)
                    self.ownPoke.speed[1] += 1
                if stat == 'accuracy' and self.ownPoke.accuracy[1] < 6:
                    if verbose:
                        print '%s accuracy has increased ' % (self.ownPoke.name)
                    self.ownPoke.accuracy[1] += 1

        # return ((ownState, oppState), action, ownState[1] - oppState[1])
        return ((ownState, oppState), action, 0)

    def discount(self):
        return 1

    def isEnd(self, state):
        return state[0][1] <= 0 or state[1][1] <= 0


# $$\      $$\ $$$$$$$\  $$$$$$$\  
# $$$\    $$$ |$$  __$$\ $$  __$$\ 
# $$$$\  $$$$ |$$ |  $$ |$$ |  $$ |
# $$\$$\$$ $$ |$$ |  $$ |$$$$$$$  |
# $$ \$$$  $$ |$$ |  $$ |$$  ____/ 
# $$ |\$  /$$ |$$ |  $$ |$$ |      
# $$ | \_/ $$ |$$$$$$$  |$$ |      
# \__|     \__|\_______/ \__|      
                                                             
    

def getHPRatio(poke, bin = 10):
    return max([0, int(np.ceil(float(poke.hp)/poke.hp_max*bin))])


def randomActions(state):
    global pd
    oppPoke = pd[state[1][0]]
    ownPoke = pd[state[0][0]]
    return (random.choice(ownPoke.moves),random.choice(oppPoke.moves))

def randomOppPolicy(state):
    return [randomActions(state)[1]]

def randomOwnPolicy(state):
    return [randomActions(state)[0]]

def pokemonBattle(ownPoke, oppPoke, ownPolicy, oppPolicy, verbose=0):
    mdp = PokemonBattleMDP(ownPoke, oppPoke)
    stateActionRewardSeq  = []
    state = mdp.startState()
    # stateActionRewardSeq.append((state, (None, None), 0))
    while not mdp.isEnd(state):
        action = (ownPolicy(state)[0], oppPolicy(state)[0])
        stateActionReward = mdp.pokemonMakeMove(state, action, verbose)
        newState, action, reward = stateActionReward[0], stateActionReward[1], stateActionReward[2]
        stateActionReward = (state, action, reward)
        stateActionRewardSeq.append(stateActionReward)
        state = newState
    stateActionRewardSeq.append((state, None, 0))
    return stateActionRewardSeq

def chooseRandomPokemonPairs(pokemon_list):
    p1 = random.choice(pokemon_list)
    p2 = random.choice(pokemon_list)
    # while p1 == p2:
    #     p2 = random.choice(pokemon_list)
    return Pokemon(eval(p1.lower() + '_dict')), Pokemon(eval(p2.lower() + '_dict'))
    


def generateData(ownPolicy, oppPolicy, trials=100, verbose=0):
    dataset = []
    for i in range(trials):
        ownPoke, oppPoke = chooseRandomPokemonPairs(pd.keys())
        seq = pokemonBattle(ownPoke, oppPoke, ownPolicy, oppPolicy, verbose)
        dataset.append(seq)
        # dataset.append(exploitSymmetry(seq))
    return dataset

def exploitSymmetry(stateActionRewardseq):
    flip_list = []
    for (state, action, reward) in stateActionRewardseq:
        sar = ((state[1], state[0]), (action[1], action[0]), -reward)
        flip_list.append(sar)
    return flip_list


def modelBasedMonteCarlo(dataset):
    transition_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    reward_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for seq in dataset:
        # seq is a list of (state,action,reward) tuples
        n = len(seq)
        for i in range(n-1):
            state = seq[i][0]
            action = seq[i][1]
            nextState = seq[i+1][0]
            reward = seq[i][2]
            transition_dict[state][action][nextState] += 1
            reward_dict[state][action][nextState].append(reward)
        transition_dict[nextState][action][nextState] += 1
        reward_dict[nextState][action][nextState].append(0)
    return transition_dict, reward_dict

class MonteCarloPokemonMDP:
    def __init__(self, td, rd, hp_bin=10.0):
        self.td = td
        self.rd = rd
        self.bin = hp_bin

    def startState(self):
        global pd
        ownPoke, oppPoke = chooseRandomPokemonPairs(pd.keys())
        return ((ownPoke.name, self.bin, ownPoke.stat), (oppPoke.name, self.bin, oppPoke.stat))

    def actions(self, state):
        global pd
        ownActions = pd[state[0][0]].moves
        oppActions = pd[state[1][0]].moves
        return [(a0, a1) for a0 in ownActions for a1 in oppActions]

    def succAndProbReward(self, state, action):
        results = []
        total = sum(self.td[state][action].values())
        for ns in self.td[state][action]:
            prob = self.td[state][action][ns]/total
            reward = float(sum(self.rd[state][action][ns]))/len(self.rd[state][action][ns])
#             print reward
            results.append((ns, prob, reward))
        return results

    def computeStates(self):
        global pd
        # self.states = set(self.td.keys())
        states = set()
        for p1 in pd:
            for p2 in pd:
                for i in range(int(self.bin)+1):
                    for j in range(int(self.bin)+1):
                        for stat1 in [None, 'burn', 'poison', 'paralysis']:
                            for stat2 in [None, 'burn', 'poison', 'paralysis']:
                                states.add(((p1, i, stat1), (p2, j, stat2)))
        self.states = states



    def discount(self):
        return 1

    def isEnd(self, state):
        return state[0][1] <= 0 or state[1][1] <= 0

# $$\    $$\  $$$$$$\  $$\      $$\   $$\ $$$$$$$$\       $$$$$$\ $$$$$$$$\ $$$$$$$$\ $$$$$$$\   $$$$$$\ $$$$$$$$\ $$$$$$\  $$$$$$\  $$\   $$\ 
# $$ |   $$ |$$  __$$\ $$ |     $$ |  $$ |$$  _____|      \_$$  _|\__$$  __|$$  _____|$$  __$$\ $$  __$$\\__$$  __|\_$$  _|$$  __$$\ $$$\  $$ |
# $$ |   $$ |$$ /  $$ |$$ |     $$ |  $$ |$$ |              $$ |     $$ |   $$ |      $$ |  $$ |$$ /  $$ |  $$ |     $$ |  $$ /  $$ |$$$$\ $$ |
# \$$\  $$  |$$$$$$$$ |$$ |     $$ |  $$ |$$$$$\            $$ |     $$ |   $$$$$\    $$$$$$$  |$$$$$$$$ |  $$ |     $$ |  $$ |  $$ |$$ $$\$$ |
#  \$$\$$  / $$  __$$ |$$ |     $$ |  $$ |$$  __|           $$ |     $$ |   $$  __|   $$  __$$< $$  __$$ |  $$ |     $$ |  $$ |  $$ |$$ \$$$$ |
#   \$$$  /  $$ |  $$ |$$ |     $$ |  $$ |$$ |              $$ |     $$ |   $$ |      $$ |  $$ |$$ |  $$ |  $$ |     $$ |  $$ |  $$ |$$ |\$$$ |
#    \$  /   $$ |  $$ |$$$$$$$$\\$$$$$$  |$$$$$$$$\       $$$$$$\    $$ |   $$$$$$$$\ $$ |  $$ |$$ |  $$ |  $$ |   $$$$$$\  $$$$$$  |$$ | \$$ |
#     \_/    \__|  \__|\________|\______/ \________|      \______|   \__|   \________|\__|  \__|\__|  \__|  \__|   \______| \______/ \__|  \__|
                                                                                                                                             
                                                                                                                                             
                                                          

# An algorithm that solves an MDP (i.e., computes the optimal
# policy).
class MDPAlgorithm:
    # Set:
    # - self.pi: optimal policy (mapping from state to action)
    # - self.V: values (mapping from state to best values)
    def solve(self, mdp): raise NotImplementedError("Override me")

############################################################
class ValueIteration(MDPAlgorithm):
    '''
    Solve the MDP using value iteration.  Your solve() method must set
    - self.V to the dictionary mapping states to optimal values
    - self.pi to the dictionary mapping states to an optimal action
    Note: epsilon is the error tolerance: you should stop value iteration when
    all of the values change by less than epsilon.
    The ValueIteration class is a subclass of util.MDPAlgorithm (see util.py).
    '''
    def solve(self, mdp, maxIter=1000, epsilon=0.001):
        mdp.computeStates()
        def computeQ(mdp, V, state, action):
            # Return Q(state, action) based on V(state).
            return sum(prob * (reward + mdp.discount() * V[newState]) \
                            for newState, prob, reward in mdp.succAndProbReward(state, action))

        def computeOptimalPolicy(mdp, V):
            # Return the optimal policy given the values V.
            pi = {}
            for state in mdp.states:
                pi[state] = max((computeQ(mdp, V, state, action), action) for action in mdp.actions(state))[1]
            return pi

        V = collections.defaultdict(float)  # state -> value of state
        numIters = 0
        while numIters < maxIter:
            newV = {}
            for state in mdp.states:
                # print V[state]
                # This evaluates to zero for end states, which have no available actions (by definition)
                newV[state] = max(computeQ(mdp, V, state, action) for action in mdp.actions(state)) 
                # print newV[state]
                # newV[state] = computeQ(mdp, V, state, mdp.actions(state)[0])
            numIters += 1
            print "ValueIteration: %d iterations" % numIters
            if max(abs(V[state] - newV[state]) for state in mdp.states) < epsilon:
                V = newV
                break
            V = newV

        # Compute the optimal policy now
        pi = computeOptimalPolicy(mdp, V)
        print "ValueIteration: %d iterations" % numIters
        self.pi = pi
        # for v in V:
        #     V[v] /= numIters

        self.V = V

#  $$$$$$\          $$\       $$$$$$$$\  $$$$$$\  $$$$$$$\  $$\   $$\ $$$$$$\ $$\   $$\  $$$$$$\  
# $$  __$$\         $$ |      $$  _____|$$  __$$\ $$  __$$\ $$$\  $$ |\_$$  _|$$$\  $$ |$$  __$$\ 
# $$ /  $$ |        $$ |      $$ |      $$ /  $$ |$$ |  $$ |$$$$\ $$ |  $$ |  $$$$\ $$ |$$ /  \__|
# $$ |  $$ |$$$$$$\ $$ |      $$$$$\    $$$$$$$$ |$$$$$$$  |$$ $$\$$ |  $$ |  $$ $$\$$ |$$ |$$$$\ 
# $$ |  $$ |\______|$$ |      $$  __|   $$  __$$ |$$  __$$< $$ \$$$$ |  $$ |  $$ \$$$$ |$$ |\_$$ |
# $$ $$\$$ |        $$ |      $$ |      $$ |  $$ |$$ |  $$ |$$ |\$$$ |  $$ |  $$ |\$$$ |$$ |  $$ |
# \$$$$$$ /         $$$$$$$$\ $$$$$$$$\ $$ |  $$ |$$ |  $$ |$$ | \$$ |$$$$$$\ $$ | \$$ |\$$$$$$  |
#  \___$$$\         \________|\________|\__|  \__|\__|  \__|\__|  \__|\______|\__|  \__| \______/ 
#      \___|                                                                                      

# Performs Q-learning.  Read util.RLAlgorithm for more information.
# actions: a function that takes a state and returns a list of actions.
# discount: a number between 0 and 1, which determines the discount factor
# featureExtractor: a function that takes a state and action and returns a list of (feature name, feature value) pairs.
# explorationProb: the epsilon value indicating how frequently the policy
# returns a random action
class QLearningAlgorithm:
    def __init__(self, actions, discount, featureExtractor, oppPolicy, explorationProb=0.4):
        self.actions = actions          # takes in state and oppPolicy
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0
        self.oppPolicy = oppPolicy

    # Return the Q function associated with the weights and features
    def getQ(self, state, action):
        score = 0
        for f, v in self.featureExtractor(state, action[0]):
            score += self.weights[f] * v
        return score

    # This algorithm will produce an action given a state.
    # Here we use the epsilon-greedy algorithm: with probability
    # |explorationProb|, take a random action.
    def getAction(self, state):
        self.numIters += 1
        exploreProb = (self.explorationProb + 1.0/self.numIters)/(1+self.explorationProb)
        if self.explorationProb == 0:
            return max((self.getQ(state, action), action) for action in self.actions(state, self.oppPolicy))[1]
        if random.random() < exploreProb:
            return random.choice(self.actions(state, self.oppPolicy))
        else:
            return max((self.getQ(state, action), action) for action in self.actions(state, self.oppPolicy))[1]

    # Call this function to get the step size to update the weights.
    def getStepSize(self):
        return 1.0 / math.sqrt(self.numIters)

    # We will call this function with (s, a, r, s'), which you should use to update |weights|.
    # Note that if s is a terminal state, then s' will be None.  Remember to check for this.
    # You should update the weights using self.getStepSize(); use
    # self.getQ() to compute the current estimate of the parameters.
    # Q = (1-n)Q + n(r + gamma Vopt)
    # Vopt = max a' Q(s', a')
    def incorporateFeedback(self, state, action, reward, newState):
        eta = self.getStepSize()
        if newState is None:
            Vopt = [0.0]
        else:
            Vopt = max([(self.getQ(newState, a), a) for a in self.actions(newState, self.oppPolicy)])
            # print eta, self.getQ(state, action), reward, self.discount, Vopt[0], (Vopt[1][0].name, Vopt[1][1].name)
        scale = -eta * (self.getQ(state, action) - (reward + self.discount * Vopt[0]))
        increment(self.weights, scale, dict(self.featureExtractor(state, action)))

def QLearning(rlalg, oppPolicy, featureExtractor, maxIter = 10000, verbose = 0):
    global pd
    rl = rlalg(None, 1, featureExtractor, oppPolicy)
    for itr in range(maxIter):
        if (itr % 10) == 0:
            print 'running iteration %i'%(itr)
        ownPoke, oppPoke = chooseRandomPokemonPairs(pd.keys())
        mdp = PokemonBattleMDP(ownPoke, oppPoke)
        rl.actions = mdp.actions
        rl.numIters = 0
        state = mdp.startState()
        while not mdp.isEnd(state):
            action = rl.getAction(state)
            stateActionReward = mdp.pokemonMakeMove(state, action, verbose)
            newState, action, reward = stateActionReward[0], stateActionReward[1], stateActionReward[2]
            rl.incorporateFeedback(state, action, reward, newState)
            state = newState
        action = (None, None)
        newState = None
        reward = 0
        rl.incorporateFeedback(state, action, reward, newState)
    return rl

# Return a single-element list containing a binary (indicator) feature
# for the existence of the (state, action) pair.  Provides no generalization.
def identityFeatureExtractor(state, action):
    featureKey = (state, action)
    featureValue = 1
    return [(featureKey, featureValue)]

# def dotProduct(d1, d2):
#     if len(d1) < len(d2):
#         return dotProduct(d2, d1)
#     else:
#         return sum(d1.get(f, 0) * v for f, v in d2.items())

def increment(d1, scale, d2):
    for f, v in d2.items():
        d1[f] = d1.get(f, 0) + v * scale



# |        \|        \ /      \ |  \     /  \      |       \  /      \|        \|        \|  \      |      \|  \  |  \ /      \ 
#  \$$$$$$$$| $$$$$$$$|  $$$$$$\| $$\   /  $$      | $$$$$$$\|  $$$$$$\\$$$$$$$$ \$$$$$$$$| $$       \$$$$$$| $$\ | $$|  $$$$$$\
#    | $$   | $$__    | $$__| $$| $$$\ /  $$$      | $$__/ $$| $$__| $$  | $$      | $$   | $$        | $$  | $$$\| $$| $$ __\$$
#    | $$   | $$  \   | $$    $$| $$$$\  $$$$      | $$    $$| $$    $$  | $$      | $$   | $$        | $$  | $$$$\ $$| $$|    \
#    | $$   | $$$$$   | $$$$$$$$| $$\$$ $$ $$      | $$$$$$$\| $$$$$$$$  | $$      | $$   | $$        | $$  | $$\$$ $$| $$ \$$$$
#    | $$   | $$_____ | $$  | $$| $$ \$$$| $$      | $$__/ $$| $$  | $$  | $$      | $$   | $$_____  _| $$_ | $$ \$$$$| $$__| $$
#    | $$   | $$     \| $$  | $$| $$  \$ | $$      | $$    $$| $$  | $$  | $$      | $$   | $$     \|   $$ \| $$  \$$$ \$$    $$
#     \$$    \$$$$$$$$ \$$   \$$ \$$      \$$       \$$$$$$$  \$$   \$$   \$$       \$$    \$$$$$$$$ \$$$$$$ \$$   \$$  \$$$$$$ 
                                                                                                                              
       

def battleOtherTeams(ownTeam, pd, ownPolicy, oppPolicy, teamSize=4, verbose=0, trials = 50):
    ownTeamNames = set([ot.name for ot in ownTeam])
    allPoke = set(pd.keys())
    remainPoke = allPoke.difference(ownTeamNames)
    teamsToBattle = itertools.permutations(remainPoke, teamSize)
    healthRemain = []
    wins = []
    for oppTeam in teamsToBattle:
        print [oppTeamName for oppTeamName in oppTeam]
        battleWin = []
        battleHealth = []
        OT = copy.copy(ownTeam)
        for (ownp, oppp) in zip(OT, oppTeam):
            for i in range(trials):
                ownPoke = copy.copy(ownp)
                oppPoke = copy.copy(pd[oppp])
                ASRseq = pokemonBattle(ownPoke, oppPoke, ownPolicy, oppPolicy, verbose)
                battleWin.append(ASRseq[-2][2]>0)
                battleHealth.append(ASRseq[-1][0][0][1] - ASRseq[-1][0][1][1])

        wins.append(sum(battleWin))
        healthRemain.append(sum(battleHealth))
    return healthRemain, wins


def battleStatistics(ownTeam, pd, ownPolicy, oppPolicy, teamSize=4, verbose=0, trials = 50):
    health, wins = battleOtherTeams(ownTeam, pd, ownPolicy, oppPolicy, teamSize, verbose, trials)
    avgHealth = np.mean(np.array(health)/teamSize/trials)
    win = np.array(wins)/trials>(teamSize/2)
    winRate = sum(win)/len(win)
    return avgHealth, wins, winRate

