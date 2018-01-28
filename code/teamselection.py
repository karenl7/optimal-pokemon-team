# team selection
# direct methods
from itertools import izip
import numpy as np
import random, collections
argmax = lambda array: max(izip(array, xrange(len(array))))
argmin = lambda array: min(izip(array, xrange(len(array))))
# genetic algorithm


def optimize_pokemon_team(winRateEval, population, domain, geneticSettings, k_max = 10):
    S = geneticSettings['Selection'](1)
    C = geneticSettings['Crossover']()
    M = geneticSettings['Mutation']()
    return genetic_algorithm(winRateEval, population, domain, S, C, M, k_max)

# func : the evaluation function, takes in a list of PokemonTeams and returns a list of the win percentage (in the same order)
# population : list of PokemonTeams [[p11,p12,p13..],[p21,p22,p23..],[p31,p32,p33..]]
# selectionMethod : method of selecting parents, options are truncation, tournament, roulette, 
#   returns list of tuples wher each tuple is the index of each parent
# crossoverMethod : method of construction children, options are single point, twopoint, uniform
# mutationMethod : bitwise or gaussian zero mean noise
def genetic_algorithm(func, population, domain, selectionMethod, crossoverMethod, mutationMethod, k_max = 10):
    for k in range(k_max):
        print "genetic algorithm generation: ", k
        parents = selectionMethod.select(func(population))
        children = [crossoverMethod.crossover(population[p[0]], population[p[1]]) for p in parents]
        population = [mutationMethod.mutate(c, domain) for c in children]
    return argmin(func(population)), population   # returns (val, index)


class SelectionMethod(object):
    def __init__(self):
        pass

    def select(self, y):
        pass

class TruncationSelection(SelectionMethod):
    def __init__(self, k):
        self.k = k

    def select(self, y):
        p = list(np.argsort(y))
        return [[p[np.random.choice(self.k)], p[np.random.choice(self.k)]] for i in y]


class TournamentSelction(SelectionMethod):
    def __init__(self, k):
        self.k = k

    def select(self, y):
        def get_parent(): return argmin(np.random.permutation(y)[:self.k])[1]
        return [[get_parent(), get_parent()] for i in y]



# a and b are the parents
# returns a list of pokemon
class CrossoverMethod(object):
    def __init__(self):
        pass

    def crossover(self, a, b):
        pass

class TwoPointCrossover(CrossoverMethod):
    def __init__(self):
        pass

    def crossover(self, a, b):
        n = len(a)
        i, j = np.random.choice(n, 2)          # array([_, _])
        if i > j:
            (i,j) = (j,i)
        return a[:i] + b[i:j] + a[j:n]

class UniformCrossover(CrossoverMethod):
    def __init__(self):
        pass

    def crossover(self, a, b):
        child = a[:]
        for i in range(len(a)):
            if random.random() < 0.5:
                child[i] = b[i]
        return child



class MutationMethod(object):
    def __init__(self):
        pass

    def mutate(self, child, domain):
        if random.random() < 0.3:
            n = len(child)
            replace_idx = np.random.choice(n)
            replace_pokemon = np.random.choice(domain)
            child[replace_idx] = replace_pokemon
        return enforceUniquePokemon(child, domain)

def enforceUniquePokemon(team, domain):
    d = collections.defaultdict(int)
    free_poke = set(domain)
    new_team = []
    for p in team:
        d[p.name] += 1
        free_poke.difference_update([p])
        if d[p.name] > 1:
            new_poke = list(free_poke)[np.random.choice(len(free_poke))]
            free_poke.difference_update([new_poke])
            new_team.append(new_poke)
            d[new_poke.name] += 1
        else:
            new_team.append(p)
    return new_team

def printTeam(team):
    print([p.name for p in team])





