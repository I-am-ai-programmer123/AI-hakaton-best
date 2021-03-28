import random
from matplotlib import pyplot as plt


def main_genetic_algorithm(n, l, t, iter=50):
    population = generate_population(n, l)
    final_value = 0
    for i in range(iter):
        parents = select_parents(population, t)
        population = [cross_parents(p) for p in parents]
        # print(population)
        max_value = 0
        solution = ""
        for p in population:
            v = q(p, t)
            if v > max_value:
                solution = p
                max_value = max(max_value, q(p, t))
        print("max_value : ", max_value)
        print("solution : ", solution)
        final_value = max(final_value, max_value)
    return final_value


# generating population based on python random module


def generate_population(n, l):
    population = []
    for i in range(n):
        speciman = ""
        for j in range(l):
            speciman += str(random.choice([0, 1]))
        population.append(speciman)

    # print(population)
    return population


# selecting parents based on roulette function


def select_parents(population, t):
    total = 0
    parent_values = []
    parents = []
    for p in population:
        c = q(p, t)
        # print(c)
        total += c
        parent_values.append(total)
    # print("total : ", total)
    for i in range(len(population)):
        t1 = random.randint(0, total)
        t2 = random.randint(0, total)
        # print(t1, t2)
        p1, p2 = None, None
        for c, pv in enumerate(parent_values):
            if t1 <= pv:
                p1 = population[c]
                break
        for c, pv in enumerate(parent_values):
            if t2 <= pv:
                p2 = population[c]
                break
        parents.append([p1, p2])
        # print(p1, p2)

    # print(parents)
    return parents


# single crossing parents and ev. mutation


def cross_parents(parents):
    child = ""
    for i in range(len(parents[0])):
        tr = random.uniform(0, 1)
        if tr <= 0.4:
            child += str(parents[0][i])
        elif tr <= 0.8:
            child += str(parents[1][i])
        else:
            child += str(random.choice([0, 1]))

    return child


# functions as they were described in task


def o(x):
    r = 0
    for s in x:
        if s == "1":
            r += 1
        else:
            return r
    return r


def z(x):
    r = 0
    for s in x[::-1]:
        if s == "0":
            r += 1
        else:
            return r
    return r


def REWARD(x, t):
    if o(x) >= t and z(x) >= t:
        return 100
    else:
        return 0


def q(x, t):
    return max(o(x), z(x)) + REWARD(x, t)


# pop = generate_population(10, 6)
# parents = select_parents(pop, 3)

# main_genetic_algorithm(400, 20, 9, 100)


def generate_plot(min_iter=30, max_iter=200, step_iter=20, population_size=300, genome_len=30, param_t=7):
    x = [i for i in range(min_iter, max_iter, step_iter)]
    y = [main_genetic_algorithm(population_size, genome_len, param_t, i) for i in x]
    plt.plot(x, y)
    plt.xlabel("iterations amount")
    plt.ylabel("esitmated max value")
    plt.title(f"For population of {str(population_size)}, genome length of {str(genome_len)} and t equal to {str(param_t)}")
    plt.show()


generate_plot()
