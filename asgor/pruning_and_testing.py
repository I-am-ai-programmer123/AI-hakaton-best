from decision_tree_clasifier import *
from calculate_gainratio import *


def getMostProbableKey(root, current_attr, testline):
    return max(root.children, key=lambda k: root.children[k].prob)


def getDecisionValue(root, testline):
    if root.solution:
        return root.solution

    current_attr = root.current_attr
    current_attr_test_value = testline[current_attr]
    if testline[current_attr] not in root.children:
        current_attr_test_value = getMostProbableKey(
            root, current_attr, testline)
    return getDecisionValue(root.children[current_attr_test_value], testline)


def getTestResults(root, testset):
    good_test = 0
    wrong_test = 0
    test_results = {}
    arr = []

    for testline in testset:
        dec = getDecisionValue(root, testline)
        arr.append([dec, testline[-1]])
        if dec in test_results:
            test_results[dec] += 1
        else:
            test_results[dec] = 1
        if dec == testline[-1]:
            good_test += 1
        else:
            wrong_test += 1
    return arr, good_test / (wrong_test + good_test)


def getMostCommonResult(root, d):
    if root.solution:
        if root.solution not in d:
            d[root.solution] = 1
        else:
            d[root.solution] += 1
    if not root.children:
        return d
    for child in root.children:
        d = getMostCommonResult(root.children[child], d)
    return d


def getNewTestAttr(root):
    d = {}
    d = getMostCommonResult(root, d)
    return max(d, key=d.get)


def getNewTestResults(test_value, testset):
    good_test = 0
    wrong_test = 0
    result_comparision = []
    for testline in testset:
        if test_value == testline[-1]:
            good_test += 1
        else:
            wrong_test += 1
    return good_test / (good_test + wrong_test)


def PruneNode(root, testset):
    if root.children:
        for child in root.children:
            PruneNode(root.children[child], testset)
    # when reaches leaf return to parent
    if not root.children:
        return
    arr = []
    arr, previous_prob = getTestResults(root, testset)
    test_value = getNewTestAttr(root)
    new_prob = getNewTestResults(test_value, testset)

    print("previous prob: ", previous_prob)
    print("new prob: ", new_prob)
    if new_prob >= previous_prob:
        print("A")
        root.children = {}
        root.solution = test_value


dataset = []
testset = []
with open('audiology.standardized.data', 'r') as f:
    for l in f:
        line = l.split(",")
        dataset.append(line)
root = Classifier_node()

with open('audiology.standardized.test', 'r') as f:
    for l in f:
        line = l.split(",")
        testset.append(line)

dataset = prepareDataSet(dataset)

createDecisionTree(root, dataset)

arr1, first_result = getTestResults(root, testset)

PruneNode(root, testset)

arr2, second_result = getTestResults(root, testset)


print(first_result)
print(second_result)

for id3, c45 in zip(arr1, arr2):
    print(id3[0], " | ", c45[0], " | ", id3[1])


mistake_matrix = [[0, 0], [0, 0]]

for line in arr2:
    if line[0] == line[1] and line[1] == "normal ear":
        mistake_matrix[0][0] += 1
    elif line[1] == "normal ear":
        mistake_matrix[0][1] += 1
    elif line[0] == line[1]:
        mistake_matrix[1][1] += 1
    else:
        mistake_matrix[1][0] += 1

print(mistake_matrix)
