"""
Author: Bartłomiej Baran
"""
import numpy as np


class Invidual():
    """
    Class representing invidual.
    """
    def __init__(self, fit_function, dimension, low, up):
        """
        Constructor of Invidual class.

        :param fit_function: fitness function
        :type fit_function: float

        :param dimension: amout of variables passed
                           to function / dimension of function
        :type var_amout: int

        :param low: lower boundry of genes values
        :type low: int

        :param up: upper boundry of genes values
        :type up: int
        """
        # self.fit_function = fit_function
        self.dimension = dimension
        self.low = low
        self.up = up
        self.genes = self.__generate_genes()
        self.fitness = self.calculate_fitness(fit_function)

    def __generate_genes(self):
        """
        Generates random genes in range <low, up> boundries.
        Method is used only when constructing an Invidual object.
        """
        return [np.random.uniform(self.low, self.up)
                for g in range(self.dimension)]

    def mutate_random_gene(self, mut_scale):
        """
        Mutates invidual genes using normal distribution where sigma=mut_scale

        :param mut_scale: mutation scale
        :type mut_scale: float
        """
        new_genes = []
        for g in self.genes:
            new_genes.append(max(min(self.up,
                             np.random.normal(g, mut_scale)), self.low))
        self.genes = new_genes

    def calculate_fitness(self, fit_function):
        """
        Returns and set new calculated fitness of an Invidual object
        using fitness function.
        """
        self.fitness = fit_function(self.genes)
        return self.fitness
