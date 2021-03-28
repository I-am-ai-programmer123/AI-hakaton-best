import random
import numpy as np
import copy
from math import sin, cos, e
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy import stats


def main_quasi_newton_raphson(f):
    # f = lambda x,y: eval("sin(1/2*x**2 - 1/4*y**2 + 3)*cos(2*x+1-e**y)") - example of f

    x1 = random.uniform(-1, 1)
    x2 = random.uniform(-1, 1)
    x = np.array([x1, x2])
    qnr = quasiNewtonRaphson()
    qnr.calculate(f, x)
    qnr.getStepsCount()

    sX, sY = qnr.getSteps()

    sZ = list(map(f, sX, sY))
    return sX, sY, sZ



class quasiNewtonRaphson:
    stepsCount = 0  # initiate steps count as 0 and empty arrays for X and Y
    stepsX = []
    stepsY = []
    def calculate(self, f, x, tol=0.01, maxiter=100):
        self.stepsCount = 0
        self.stepsX = [x[0]]    # assign first values
        self.stepsY = [x[1]]
        B = approx_update_hessian(f, x) # approx. first matrices
        g = approx_gradient(f, x)

        for i in range(1, maxiter):
            try:

                xnew = x - np.dot(B, g)     # assign as first vector subtracted by dot product of reverseHessian and gradient
                xold = np.array([self.stepsX[-1], self.stepsY[-1]])
                self.stepsX.append(xnew[0])
                self.stepsY.append(xnew[1])
                gold = copy.deepcopy(g)     # gold - old gradient
                g = approx_gradient(f, xnew)    
                B = approx_update_hessian(f, x)     


                if abs(g[0]) < tol and abs(g[1]) < tol: # if below tolerance no need to pursue further gradient descent
                   break     

            except np.linalg.LinAlgError:   # anticipate numpy-related error
                print("Encountered LinAlgError - breaking")
                break
            x = xnew
        
        self.__stepsCount = i+1
        return xnew

    def getStepsCount(self):    # get methodes
        return self.stepsCount

    def getSteps(self):                                         
        return self.stepsX, self.stepsY
    
    

def approx_gradient(f, v):  # from definiton of derivative - further explained in documentation
    a = 0.01
    g1 = (f(x = v[0] + a, y = v[1]) - f(x = v[0] - a, y = v[1])) / (2 * a)
    g2 = (f(x = v[0], y = v[1] + a) - f(x = v[0], y = v[1] - a)) / (2 * a)
    return np.array([g1, g2])

def approx_update_hessian(f, x):
    h = 0.01
    ex = np.array([h, 0])
    ey = np.array([0, h])
    H = np.ones([2, 2])
    H[0][0], H[1][0] = (approx_gradient(f, x + ex) - approx_gradient(f, x)) / h
    H[0][1], H[1][1] = (approx_gradient(f, x + ey) - approx_gradient(f, x)) / h
    return np.linalg.inv(H)




def generate_plot(f, sX, sY):
    X = np.arange(-1*abs(3*min(sX)), abs(3*max(sX)), 0.01)       # generate array of points
    Y = np.arange(-1*abs(3*min(sY)), abs(3*min(sY)), 0.01)

    X, Y = np.meshgrid(X, Y)                    # calculate meshgrid of both
    Z = f(X, Y)

    plt.figure(figsize=(8, 8))                  # visual paramters

    plt.grid(False)

    plt.contour(X, Y, Z, np.linspace(-1, 1, 15), cmap='Spectral')       # create contours

    plt.xlabel('x')
    plt.ylabel('y')



    for i in range(1, len(sX)):             # draw arrows connect steps
        plt.arrow(x=sX[i-1], y=sY[i-1], dx=sX[i]-sX[i-1], dy=sY[i]-sY[i-1], width=0.01, zorder=100, color="k")


    plt.tight_layout()
    plt.colorbar()
    plt.show()          # show plot



# example test 
f = lambda x,y: np.sin(1/2*x**2 - 1/4*y**2 + 3)*np.cos(2*x+1-e**y)    #example of f
sX, sY, sZ = main_quasi_newton_raphson(f)
generate_plot(f, sX, sY)

# results = []
# # performing tests
# for i in range(25):
#     sx, sy, sz = main_quasi_newton_raphson(f)
#     results.append(min(sz))

# variancy = np.var(results)
# # median absolute deviation
# mad = stats.median_abs_deviation(results)

# print(mad)
# # print(abs(-1 - np.average(results)))