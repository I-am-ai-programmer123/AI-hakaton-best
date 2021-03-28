import numpy as np


def getMostProbableValues(dataset):
    most_probable_value = {}
    for x in range(len(dataset[0])):
        current_column = {}
        for y in range(len(dataset)):
            param = dataset[y][x]
            if param == "?":
                continue
            if param not in current_column:
                current_column[param] = 1
            else:
                current_column[param] += 1
        most_probable_value[x] = max(current_column, key=current_column.get)
    return most_probable_value


def prepareDataSet(dataset):
    most_probable_value = getMostProbableValues(dataset)
    for y in range(len(dataset)):
        for x in range(len(dataset[y])):
            if dataset[y][x] == "?":
                dataset[y][x] = most_probable_value[x]
    return dataset


def prepareAttrDict(recent_attr, current_attr, dataset):
    attr_dict = {}
    # attr_dict = {weak:{num:8, param:{yes:6, no:2}}}
    for dataline in dataset:
        fulfills_req = True
        for key in recent_attr:
            if recent_attr[key] != dataline[key]:
                fulfills_req = False
        if fulfills_req:
            param = dataline[current_attr]
            solution = dataline[-1]
            if param not in attr_dict:
                attr_dict[param] = {"num": 1, "solution": {solution: 1}}
            elif solution not in attr_dict[param]["solution"]:
                attr_dict[param]["num"] += 1
                attr_dict[param]["solution"][solution] = 1
            else:
                attr_dict[param]["num"] += 1
                attr_dict[param]["solution"][solution] += 1
    # print(attr_dict)
    return attr_dict


def prepareEnthropyDecision(attr_dict):
    enthropy_dict = {}
    for attr in attr_dict:
        for param in attr_dict[attr]["solution"]:
            if param not in enthropy_dict:
                enthropy_dict[param] = attr_dict[attr]["solution"][param]
            else:
                enthropy_dict[param] += attr_dict[attr]["solution"][param]
    return enthropy_dict


def calculateEnthropy(enthropy_dict):
    sum_of_params = sum(enthropy_dict.values())
    result = 0

    for value in enthropy_dict.values():
        try:
            result += -1 * (value/sum_of_params) * np.log2(value/sum_of_params)
            # print(result)
        except ValueError:
            continue
    return result


def calculateEnthropyForParam(enthropy_dict):
    sum_of_params = sum(enthropy_dict.values())
    result = 0

    for value in enthropy_dict.values():
        try:
            result += -1 * (value/sum_of_params) * \
                (value/sum_of_params) * np.log2(value/sum_of_params)
            # print(result)
        except ValueError:
            continue
    return result


def calculateEnthropyDecision(enthropy_dict):
    result = 0
    return calculateEnthropy(enthropy_dict)


def calculateEnthropyParam(attr_dict, param):
    return calculateEnthropyForParam(attr_dict[param]["solution"])


def calculateEnthropyParamSum(attr_dict):
    enthropy_sum = 0
    for param in attr_dict:
        enthropy_sum += calculateEnthropyParam(attr_dict, param)
    return enthropy_sum


def calculateSplitInfo(attr_dict):
    split_sum = 0
    split_info = 0
    for param in attr_dict:
        split_sum += attr_dict[param]["num"]
    # print(split_sum)
    for param in attr_dict:
        value = attr_dict[param]["num"]
        split_info += (-1) * (value / split_sum) * np.log2(value/split_sum)
    return split_info


def calculateGain(recent_attr, current_attr, dataset):
    attr_dict = prepareAttrDict(recent_attr, current_attr, dataset)
    enthropy_dict = prepareEnthropyDecision(attr_dict)
    split_info = calculateSplitInfo(attr_dict)
    if split_info == 0:
        return float("-inf")
    return (calculateEnthropyDecision(enthropy_dict) - calculateEnthropyParamSum(attr_dict))/(calculateSplitInfo(attr_dict))
