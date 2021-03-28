"""
Author: Bartłomiej Baran
"""
from Invidual import Invidual
import numpy as np
import copy


class Population():
    """
    Class representing population.
    """
    def __init__(self, func, dimension, low,
                 up, pop_size, mutation_scale=0.001, mutation_chance=0.05):
        """
        Constructor of Population class.

        :param func: fitness function
        :type func: float

        :param dimension: amout of variables passed
                           to function / dimension of function
        :type dimension: int

        :param low: lower boundry of genes values
        :type low: int

        :param up: upper boundry of genes values
        :type up: int

        :param pop_size: size of population
        :type pop_size: int

        :param mutation_scale: scale of mutation
        :type mutation_scale: float

        :param mutation_chance: chance of mutating
        :type mutation_chance: float
        """
        self.func = func
        self.dimension = dimension
        self.low = low
        self.up = up
        self.pop_size = pop_size
        self.mutation_scale = mutation_scale
        self.mutation_chance = mutation_chance
        self.population = self.__generate_population()
        self.invidual_fitnesses = self.get_individual_fitnesses()
        self.overall_pop_value = self.value_population()

    def __generate_population(self):
        """
        Generates and returns array of inviduals,
        generated based on parameters passed.
        """
        return [Invidual(self.func, self.dimension, self.low, self.up)
                for i in range(self.pop_size)]

    def mutate_population(self):
        """
        Mutates population based on mutation chance.
        """
        for invidual in self.population:
            if(np.random.uniform(0, 1) < self.mutation_chance):
                invidual.mutate_random_gene(self.mutation_scale)
        self.rate_population()

    def value_population(self):
        """
        Returns sum of fitnesses of all inviduals in the population.
        """
        return sum(self.invidual_fitnesses)

    def get_individual_fitnesses(self):
        """
        Calculates fitness of all inviduals in population,
        and returns those fitnesses in an array.
        """
        for i in self.population:
            i.calculate_fitness(self.func)
        return [invidual.fitness for invidual in self.population]

    def find_best(self):
        """
        Returns an invidual that has the best fitness in population.
        """
        return min(self.population, key=lambda x: x.fitness)

    def __roulette_selection_picker(self):
        """
        Executes roulette selection.
        Invidual who has the best fitness has the smallest
        chance to be selected (minimalization).
        Returns index of a selected invidual.
        """
        maximum = sum([c.fitness for c in self.population])
        select_probs = [c.fitness/maximum for c in self.population]
        return self.pop_size - \
            np.random.choice(len(self.population), p=select_probs) - 1

    def __create_children_roulette_select(self):
        """
        Creates children from parents using roulette selection method.
        Returns an array of new population.
        """
        self.population = sorted(self.population,
                                 key=lambda x: x.fitness, reverse=True)
        self.invidual_fitnesses = self.get_individual_fitnesses()
        self.overall_pop_value = self.value_population()
        return [copy.deepcopy(
                self.population[self.__roulette_selection_picker()])
                for i in range(self.pop_size)]

    def generational_succession(self):
        """
        Generational succession, children becomes current population.
        """
        self.population = self.children
        self.rate_population()

    def roulette_selection(self):
        """
        Rates fitness of inviduals and overall population fitness.
        """
        self.children = self.__create_children_roulette_select()

    def rate_population(self):
        """
        Rates fitness of inviduals and overall population fitness.
        """
        self.invidual_fitnesses = self.get_individual_fitnesses()
        self.overall_pop_value = self.value_population()
