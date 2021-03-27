#!/usr/bin/env python3

# Andrzej Kusiak
# Stochastyczny algorytm wspinaczkowy

from math import sin, cos, e, sqrt
from random import uniform
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize


def q(point):
    # Wylicza wartość funkcji dla danego punktu
    x = point[0]
    y = point[1]

    return sin(1/2*x**2 - 1/4*y**2 + 3) * cos(2*x + 1 - e**y)


def selRandom(point):
    # Znajduje losowy punkt z sąsiedztwa w zależności od parametru sigma
    sigma = 0.85    # PARAMETR ALGORYTMU

    x = point[0]
    y = point[1]

    x = x + uniform(-sigma, sigma)
    while(x <= -2 or x >= 2):
        x = x + uniform(-sigma, sigma)

    y = y + uniform(-sigma, sigma)
    while(y <= -2 or y >= 2):
        y = y + uniform(-sigma, sigma)

    return x, y


def hillcimbing(x0):
    # Implementacja stochastycznego algorytmu wspinaczkowego
    x = x0
    data = [x]
    for _ in range(100):
        y = selRandom(x)
        if q(y) > q(x):
            x = y
            data.append(x)

    return data


def draw_plot(points):
    # Rysowanie poziomicy funkcji
    x = np.arange(-2, 2.01, 0.01)
    y = np.arange(-2, 2.01, 0.01)

    xx, yy = np.meshgrid(x, y)
    z = np.sin(1/2*xx**2 - 1/4*yy**2 + 3) * np.cos(2*xx + 1 - e**yy)    # sin(1/2*x**2 - 1/4*y**2 + 3) * cos(2*x + 1 - e**y)

    cp = plt.contour(x, y, z, 20)
    plt.clabel(cp, inline=1, fontsize=8)

    plt.title('Hill climbing algorithm', fontsize=15)
    plt.xlabel('x')
    plt.ylabel('y')

    # punkty zaczepienia wektorów
    vec_x = []
    vec_y = []

    # współżędne wektorów
    vec_dir_x = []
    vec_dir_y = []

    lenght = len(points)
    for i in range(lenght - 1):
        vec_x.append(points[i][0])
        vec_y.append(points[i][1])
        vec_dir_x.append(points[i+1][0] - points[i][0])
        vec_dir_y.append(points[i+1][1] - points[i][1])

    # Ustawianie kolorów wektorów
    colors = np.arctan2(vec_dir_y, vec_dir_x)
    norm = Normalize()
    norm.autoscale(colors)

    colormap = cm.plasma

    # Rysowanie wektorów
    plt.quiver(vec_x, vec_y, vec_dir_x, vec_dir_y, color=colormap(norm(colors)), angles='xy', scale_units='xy', scale=1, width=0.007)

    plt.show()

    return points[-1]


def get_min_distance(point):
    # Oblicza odległość od najliższego wierzchołka
    local_max = [(-1.89, -0.81), (1.88, 0.48), (-2, 1.85), (0.05, 2), (1.99, 2), (-0.38, -2)]

    min_dist = 6    # Min dystans na pewno będzie mniejszy niż przekątna - 4*sqrt2
    for p in local_max:
        d = sqrt((point[0] - p[0])**2 + (point[1] - p[1])**2)
        if d < min_dist:
            min_dist = d

    return d


def collect_measurements():
    distances = []
    for _ in range(25):
        x0 = uniform(-2, 2), uniform(-2, 2) # losowy punkt startowy
        #print(x0)
        points = hillcimbing(x0)    # procedura zwraca punkty do których po koleji przemieścił się algorytm

        dist = get_min_distance(points[-1])
        distances.append(dist)

        # draw_plot(points)

    return distances


def get_statistics(data):
    mini = data[0]
    maxi = data[0]
    suma = 0

    for i in data:
        suma += i
        if i > mini:
            mini = i
        if i < maxi:
            maxi = i

    average = suma/len(data)

    # Odchylenie standardowe
    variance = 0
    for i in data:
        variance += (i-average)**2

    return mini, maxi, average, sqrt(variance/len(data))    # <- odchylenie standardowe


if __name__ == "__main__":
    # dist = collect_measurements()
    # print("\nDistances from nearest local maximums")
    # for i in dist:
    #     print(i)

    # mi, mx, ave, standard_deviation = get_statistics(dist)
    # print(f"\nmin: {mi}\nmax: {mx}\naverage: {ave}\nstandard deviation: {standard_deviation}")

    # x0 = 0.41, 0.77
    x0 = uniform(-2, 2), uniform(-2, 2) # losowy punkt startowy
    print(x0)
    points = hillcimbing(x0)
    draw_plot(points)
