"""
Author: Bartłomiej Baran
"""
from Population import Population
from optproblems.cec2005 import F6
import numpy as np


def round_array(array, digits=2):
    """
    Rounds all elements in array.

    :param array: array of elements to be rounded
    :type array: float or int

    :param digits: number the digits to element to be rounded to
    :type digits: int

    Returns array of rounded values.
    """
    return [round(i, digits) for i in array]


def evolution_algorithm(function, dimension, lower, upper, pop_size,
                        mutation_scale, mutation_chance):
    """
    Executes every step of evolution algorithm.
    """
    B = 10000 * dimension  # 10000*10
    iter_num = int(B/pop_size)

    # Starting population
    pop = Population(function, dimension, lower, upper, pop_size,
                     mutation_scale, mutation_chance)

    # Evolution algorithm
    for i in range(iter_num):
        pop.roulette_selection()
        pop.generational_succession()
        pop.mutate_population()
        pop.rate_population()

    # Print and return best invidual
    best = pop.find_best()
    print("Best invidual:")
    print(round_array(best.genes))
    print(round(best.fitness, 2), "\n")
    return (best.genes, best.fitness)


if __name__ == '__main__':
    # CONFIGURATION
    # Seed
    np.random.seed(20)
    # Number of variables / dimension
    dimension = 10
    # Function F6 from cec2005
    function = F6(dimension)
    # Limitations <-100; 100>
    lower = -100
    upper = 100
    # Power/scale of mutation/sigma - change to 0 to disable mutation
    mutation_scale = 1
    # Chance for mutation - change to 0 to disable mutation
    mutation_chance = 1  # 1=100%
    # Population size
    pop_size = 500
    results = []
    # number of independent runs
    number_of_runs = 25
    for run in range(number_of_runs):
        print(f"Run number {run+1}")
        results.append(evolution_algorithm(function, dimension,
                                           lower, upper, pop_size,
                                           mutation_scale,
                                           mutation_chance))

    # Display results
    print("\n--Results--")
    print("Number of independent runs:", number_of_runs)
    print(f"Population size: {pop_size}")

    # Split results into two arrays (genes, fitnesses)
    genes = []
    fitnesses = []
    for j in range(len(results)):
        genes.append(results[j][0])
        fitnesses.append(results[j][1])

    # Print final results
    print("Average fitness:",
          np.format_float_scientific(round(np.average(fitnesses), 2), 2))
    print("Min fitness:",
          np.format_float_scientific(round(min(fitnesses), 2), 2))
    print("Max fitness:",
          np.format_float_scientific(round(max(fitnesses), 2), 2))
    print("Std dev:",
          np.format_float_scientific(np.std(fitnesses), 2))
