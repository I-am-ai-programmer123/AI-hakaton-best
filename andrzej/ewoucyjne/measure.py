#!/usr/bin/env python3

from evolutionary_algorithm import evolutionaryAlgorithm
from math import sqrt


def average(data):
    return sum(data)/len(data)


def standardDeviation(data):
    ave = average(data)
    m = 0
    for i in data:
        m += (i - ave)**2

    return sqrt(m/(len(data) - 1))


def getResaults():
    # Zbiera dane dla różnych populacji
    dim = 10
    B = 10000 * dim
    # B = rozmiar_populacji*liczba_iteracji
    data = {}

    for popSize in [3, 5, 7, 10, 12, 15, 20, 25, 30, 40, 50, 75, 100, 500, 1000, 1500, 2000, 5000]:
        data[popSize] = []
        for _ in range(10):
            P = evolutionaryAlgorithm(dim, popSize, B)
            data[popSize].append(P[0].rank)

    return data


def saveResaults(data):
    # Zapisuje dane do pliku
    with open("Evolutionary algorithm resaults", "w") as f:
        f.write("Resaults for evolutionary algorithm\n")
        for key, value in data.items():
            s = str(key) + " : "
            ave = average(value)
            sd = standardDeviation(value)

            if ave > 10000:
                    s += " " + format(ave, "5.2E")
            else:
                s += " " + str(int(ave))

            if sd > 10000:
                s += " " + format(sd, "5.2E")
            else:
                s += " " + str(int(sd))
            s += " : "

            for i in value:
                if i > 10000:
                    s += " " + format(i, "5.2E")
                else:
                    s += " " + str(int(i))
            s += "\n"
            f.write(s)


if __name__ == "__main__":
    t = getResaults()
    saveResaults(t)
