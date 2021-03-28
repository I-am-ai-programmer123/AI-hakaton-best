'''
Author: Bartłomiej Baran
Album number: 304007
'''
import numpy as np
import matplotlib.pyplot as plt


def generate_start_point(domain, rng):
    """
        Generate random point (x, y)
        where x in range (domain[0], domain[1])
        and y in range (rng[0], rng[1]).

        :param domain: domain (x)
        :type domain: tuple

        :param rng: range (y)
        :type rng: tuple

        Returns generated coords (x, y).
    """
    return [np.random.uniform(domain[0], domain[1]),
            np.random.uniform(rng[0], rng[1])]


def random_neighbour(point, sigma, domain, rng):
    """
        Generate random point (x, y)
        where x in range (point[0]-sigma, point[0]+sigma)
        and y in range (point[1]-sigma, point[1]+sigma)
        using normal distribution (from numpy library).
        The point is generated again till it is in
        range and domain of the function.

        :param sigma: standard deviation
        :type domain: float

        :param point: mean
        :type point: array

        Returns generated (normal distribution) coords (x, y).
    """
    rand_nbour = [
                np.random.normal(loc=point[0], scale=sigma, size=None),
                np.random.normal(loc=point[1], scale=sigma, size=None)]

    while rand_nbour[0] < domain[0] or rand_nbour[0] > domain[1] \
            or rand_nbour[1] < rng[0] or rand_nbour[1] > rng[1]:
        rand_nbour = [
                    np.random.normal(loc=point[0], scale=sigma, size=None),
                    np.random.normal(loc=point[1], scale=sigma, size=None)]
    return rand_nbour


def calc_func_value(p):
    """
        Calculates value (Z) of function q(x, y).

        :param p: point (x,y)
        :type p: array

        Returns calculated value (Z) of q(x, y).
    """
    return np.sin((0.5 * np.power(p[0], 2)) - (0.25 * np.power(p[1], 2)) + 3) \
        * np.cos((2*p[0]) + 1 - (np.power(np.e, p[1])))


def hill_climb(domain, rng, start_point=None, sigma=0.1):
    """
        Executes hill-climbing algorithm.

        :param domain: domain (x)
        :type domain: tuple

        :param rng: range (y)
        :type rng: tuple

        :param start_point: (first) starting point
        :type start_point: array

        :param sigma: standard deviation
        :type sigma: float

        Returns array of points that algorithm choose to reach minimum
        (array of (x, y, z) coords).
    """
    # If starting point was not passed generate random one
    if start_point is None:
        start_point = generate_start_point(domain, rng)
    else:
        start_point = list(start_point)

    # Append points with starting point (x, y, z)
    start_point.append(calc_func_value(start_point))
    points = [start_point]

    # Execute hill-climbing algorithm
    for i in range(100):
        # Generate random neighbour point
        rand_neighbour = random_neighbour(start_point, sigma, domain, rng)
        val = calc_func_value(rand_neighbour)
        # If value is smaller (point is deeper) save it and move to it
        if val < calc_func_value(start_point):
            start_point = rand_neighbour
            start_point.append(val)
            points.append(start_point)
    return points


def main(starting_point, domain, rnge, sigma):
    """
        Creates final plot based on output of an algorithm.

        :param starting_point: (first) starting point
        :type starting_point: array

        :param domain: domain (x)
        :type domain: tuple

        :param rnge: range (y)
        :type rnge: tuple

        :param sigma: standard deviation
        :type sigma: float
    """
    # Create meshgrid
    X, Y = np.meshgrid(np.linspace(-2, 2, 200), np.linspace(-2, 2, 200))
    Z = calc_func_value((X, Y))

    # Set window size to 8x8 inches
    plt.figure(figsize=(8, 8))

    # Turn off grid
    plt.grid(False)

    plt.contour(X, Y, Z, np.linspace(-1, 1, 15), cmap='Spectral')
    plt.colorbar()
    # Name axes (x, y)
    plt.xlabel('x')
    plt.ylabel('y')

    # Get coordinates of points where algorithm went
    set_of_points = hill_climb(domain, rnge, starting_point, sigma)

    # Initiate arrays of coords
    x_coords = []
    y_coords = []
    z_coords = []
    for i in range(len(set_of_points)):
        x_coords.append(set_of_points[i][0])
        y_coords.append(set_of_points[i][1])
        z_coords.append(set_of_points[i][2])
    num_of_points = len(x_coords) - 1

    # Show points on plot
    # (starting point - green, transitional points - blue, end point - red)
    plt.scatter(x_coords[0], y_coords[0], c='g', zorder=100)
    plt.scatter(x_coords[1:len(x_coords)-1], y_coords[1:len(x_coords)-1],
                zorder=100, c="dodgerblue")
    plt.scatter(x_coords[len(x_coords)-1:], y_coords[len(x_coords)-1:], c='r',
                alpha=1, s=35, zorder=100)

    # Connect points on plot
    plt.plot(x_coords, y_coords, c="b", alpha=0.5)

    # Legend items
    red_dot = plt.Line2D(
        range(1), range(1), c="w", marker='o',
        markerfacecolor="red", markersize=10)
    mid_point = plt.Line2D(
        range(1), range(1), c="w", marker='o',
        markerfacecolor="dodgerblue", markersize=10)
    green_dot = plt.Line2D(
        range(1), range(1), c="w", marker='o',
        markerfacecolor="green", markersize=10)

    # Round coordinates of start and end point
    start_point = tuple([round(c, 2) for c in set_of_points[0]])
    end_point = tuple([round(c, 2) for c in set_of_points[num_of_points]])

    # Create legend
    plt.legend(
        (green_dot, mid_point, red_dot),
        (f'Start point (x, y, z) = {start_point}',
         f'Intermediate point',
         f'End point (x, y, z) = {end_point}'),
        numpoints=1,
        loc="best")

    # Set title of plot
    plt.title("Stochastic hill-climbing algorithm")

    # Enhance view
    plt.tight_layout()

    # Save plot to file named "output.png"
    plt.savefig("output.png", dpi=400)

    # Show plot
    plt.show()


if __name__ == '__main__':

    # CONFIGURATION:
    # Starting point (None - point will be generated randomly)
    starting_point = (-1, 1)
    # Domain (x)
    domain = (-2, 2)
    # Range (y)
    rnge = (-2, 2)
    # Sigma for normal distribution
    sigma = 0.1

    # Execute main function with passed configuration
    main(starting_point, domain, rnge, sigma)
