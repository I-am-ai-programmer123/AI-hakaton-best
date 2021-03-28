import numpy as np
import random
from matplotlib import pyplot as plt

def main_func(x):
    return np.sin(x*np.sqrt(5)) + np.cos(x*np.sqrt(3))

class Perceptron():
    def __init__(self, inputLayer, outputLayer, learningRate = 0.0001):
        self.inputLayer = inputLayer
        self.outputLayer = outputLayer
        self.inputSize = 1
        self.hiddenSize = 100
        self.outputSize = 1
        self.learningRate = learningRate

        self.X = None

        self.weightsHiddenLayer = np.random.randn(self.inputSize+1, self.hiddenSize)
        self.weightsOutputLayer = np.random.randn(self.hiddenSize+1, self.outputSize)

    def activation(self, x):
        return np.log(1 + np.exp(x))

    def activationDerivative(self, x):
        return np.exp(x) / (1 + np.exp(x))

    def forward(self, X):
        self.X = np.hstack((X, np.ones((X.shape[0], 1))))

        self.h1 = np.dot(self.X, self.weightsHiddenLayer)
        self.ha1 = self.activation(self.h1)
        self.ha1 = np.hstack((self.ha1, np.ones((self.ha1.shape[0], 1))))

        self.o2 = np.dot(self.ha1, self.weightsOutputLayer)
        self.oa2 = self.o2
        return self.oa2

    def backward(self, y):
        self.error_2 = (self.oa2 - y)
        self.error_delta_2 = self.error_2

        self.error_1 = self.error_delta_2.dot(self.weightsOutputLayer[:-1].T)
        self.error_delta_1 = self.error_1*self.activationDerivative(self.h1)
        
        self.stepSizesHidden = self.X.T.dot(self.error_delta_1)
        self.stepSizesOutput = self.ha1.T.dot(self.error_delta_2)

        # print(self.stepSizesHidden)
        # print(self.stepSizesOutput)

        self.weightsHiddenLayer -= self.learningRate*self.stepSizesHidden
        self.weightsOutputLayer -= self.learningRate*self.stepSizesOutput
        max_step_hidden = max(self.stepSizesHidden.min(), self.stepSizesHidden.max(), key=abs)
        max_step_output = max(self.stepSizesOutput.min(), self.stepSizesOutput.max(), key=abs)

        return max(max_step_hidden, max_step_output)

    def train(self):
        step_count = 0
        while step_count < 100000:

            self.forward(self.inputLayer)
            max_step = self.backward(self.outputLayer)
            if abs(max_step) < 0.000001:
                print("SC: ", step_count)
                break
            step_count += 1
            if step_count % 1000 == 0:
                print(self.calculateSSR())      # calculate sum of square residuals
                print(step_count)
            # print(self.calculateSSR())


    def calculateSSR(self):
        # print("LOSS")
        return sum(np.square(self.oa2 - self.outputLayer))



inputSample = [[random.uniform(-5,5)] for _ in range(50)]
outputSample = [[main_func(x[0])] for x in inputSample]
inputSample = np.array(inputSample)
outputSample = np.array(outputSample)



nn = Perceptron(inputSample, outputSample)
nn.train()

testPointsX = [[random.uniform(-5,5)] for _ in range(500)]
X = np.array(testPointsX)
testPointsY = nn.forward(X)
print(testPointsY)

new_X = [xc[0] for xc in X]
Y_proper = [main_func(x[0]) for x in testPointsX]
Y_nn = [y[0] for y in testPointsY]

print(sum(np.square(np.array(Y_proper) - np.array(Y_nn)) / len(Y_proper)))

for x,y in zip(new_X, Y_proper):
    plt.scatter(x, y, color="green")

for x,y in zip(new_X, Y_nn):
    plt.scatter(x, y, color="red")

plt.show()