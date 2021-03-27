from optproblems.cec2005 import F6
import math
from random import uniform, randrange, gauss
from copy import deepcopy


class Subject:
    def __init__(self, dimension, parameters):
        self.dim = dimension
        if len(parameters) != dimension:
            print("Wrong dimension")
            raise Exception
        self.param = parameters
        self.rank = math.inf  # ponieważ minimalizuję - nim mniejsze tym lepiej

# Pseudokod algorytmu ewolucyjnego
# incjalizacja_parametrow
# t=0
# P0 = i n i c j a c j a ( )
# ocena ( P0 )
# while ( ! k o n i e c )
# Tt = s e l e k c j a ( Pt )
# Ot = o p e r a t o r y _ g e n e t y c z n e ( Tt )
# ocena ( Ot )
# Pt+1 = s u k c e s j a ( Ot , Pt )
# t = t+1


def init(dim, populationSize):
    # inicjalizuje obiekty na parametry z przediału [-100, 100]
    population = []
    for i in range(populationSize):
        population.append(Subject(dim, [uniform(-100, 100) for _ in range(dim)]))

    return population
    # return [
    #     Subject(dim, [1, 10, 100]),
    #     Subject(dim, [-100, -100, -100]),
    #     Subject(dim, [-20, 5, 70]),
    #     Subject(dim, [7, -77, -22]),
    #     Subject(dim, [5, 25, 97])
    #     ]


def evaluate(pop, dim):
    # obliczam ocenę obiektu
    f = F6(dim)
    for sub in pop:
        sub.rank = f(sub.param)


def select(pop, n):     # n ozn. ile osobników należy wybrać
    new_pop = []
    for _ in range(n):
        s1 = pop[randrange(len(pop))]
        s2 = pop[randrange(len(pop))]
        new_pop.append(deepcopy(s1) if s1.rank <= s2.rank else deepcopy(s2))

    return new_pop


def geneticOperators(pop):
    # Mutacje obiektów
    sigma = 0.3
    for subject in pop:
        for i in range(len(subject.param)):
            param = subject.param[i]
            param = gauss(param, sigma)
            while param < -100 or param > 100:
                param = gauss(param, sigma)

            subject.param[i] = param

    return pop


def succession(new_pop, old_pop, k):
    return new_pop[:k] + old_pop[:len(old_pop)-k]


def evolutionaryAlgorithm(dim, populationSize, B):
    P = init(dim, populationSize)
    evaluate(P, dim)
    P.sort(key=lambda x: x.rank)

    for t in range(int(B/populationSize)):
        T = select(P, populationSize*2//3)

        O = geneticOperators(T)
        evaluate(O, dim)
        O.sort(key=lambda x: x.rank)

        P = succession(O, P, len(O)//2)
        P.sort(key=lambda x: x.rank)

    return P
