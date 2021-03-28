from calculate_gainratio import *
import copy


class Classifier_node:
    def __init__(self):
        self.recent_attr = {}
        self.current_attr = None
        self.value = None
        self.current_attr_name = None
        self.children = {}
        self.prob = None
        self.result = None
        self.solution = None


def getFreeParameters(root, dataset):
    free_param = {}
    for i in range(len(dataset[0]) - 1):
        if i not in root.recent_attr:
            free_param[i] = 0

    return free_param


def getGainRatios(free_param, recent_attr, dataset):
    for current_param in free_param:
        gain_ratio = calculateGain(recent_attr, current_param, dataset)
        free_param[current_param] = gain_ratio
    return free_param


def selectMaxAttr(free_param):
    return max(free_param, key=free_param.get)


def getMaxAttr(root, dataset):
    free_param = getFreeParameters(root, dataset)
    free_param = getGainRatios(free_param, root.recent_attr, dataset)
    return selectMaxAttr(free_param)


def getSolutionForParam(recent_param, dataset):
    solutions = {}
    for dataline in dataset:
        solution = dataline[-1]
        fulfills_requirements = True
        for param in recent_param:
            if recent_param[param] != dataline[param]:
                fulfills_requirements = False
        if fulfills_requirements:
            if solution not in solutions:
                solutions[solution] = 0
            solutions[solution] += 1
    return solutions


def getSumProbablities(attr_dict):
    sum_prob = 0
    for key in attr_dict:
        sum_prob += attr_dict[key]["num"]
    return sum_prob


def createDecisionTree(root, dataset):
    solutions = getSolutionForParam(root.recent_attr, dataset)
    if len(root.recent_attr) >= len(dataset[0]) - 2:
        root.solution = max(solutions, key=solutions.values())
        return
    elif len(solutions) == 1:
        root.solution = max(solutions.keys())
        return
    elif len(solutions) == 0:
        print("ERROR")
        return

    root.current_attr = getMaxAttr(root, dataset)
    attr_dict = prepareAttrDict(root.recent_attr, root.current_attr, dataset)
    sum_of_probablities = getSumProbablities(attr_dict)

    for attr in attr_dict:
        root.children[attr] = Classifier_node()
        root.children[attr].value = attr
        root.children[attr].prob = attr_dict[attr]["num"]
        root.children[attr].recent_attr = copy.deepcopy(root.recent_attr)
        root.children[attr].recent_attr[root.current_attr] = attr
        createDecisionTree(root.children[attr], dataset)
