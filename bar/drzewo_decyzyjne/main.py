"""
Author: Bartlomiej Baran
"""
import pandas as pd
import math as m
import numpy as np
from matrix import confusion_matrix
import copy


def get_decision(tree, param, person, data):
    """
    Searches through tree till reaches leaf node and returns its value.

    :param tree: tree
    :type tree: dict
    :param param: current attribute
    :type param: string
    :param person: informations which decision to make
    :type person: dict
    :param data: dataframe with instances that
    tree was built based on
    :type data: dataframe
    """
    if type(tree) != dict:
        return tree[0]
    if param is None:
        k = list(tree.keys())[0]
        return get_decision(tree[k], k, person, data)
    try:
        return get_decision(tree[person[param]], None, person, data)
    except Exception:
        data_count = data[param].value_counts()
        for i in range(len(data_count)):
            data1 = data[param].value_counts().index[i]
            if data1 in tree.keys():
                save = i
                break
        return get_decision(tree[data[param].value_counts().index[save]], None, person, data)


def calc_class_entropy(U):
    """
    Calculates entropy of U set and returns it.

    I(U) = - Σ fi ln(fi)
             i

    :param U: set
    :type U: dataframe
    """
    last_col_name = U.columns[-1]
    last_col = U[last_col_name]
    lcol_len = len(last_col)
    states_values = last_col.unique().tolist()
    return sum(-(last_col.value_counts()[i]/lcol_len)*m.log(last_col.value_counts()[i]/lcol_len, m.e) for i in states_values)


def calc_attribute_inf(d, U):
    """
    Calculates entropy of a set divided into subsets
    by attribute d and returns it.

    Inf(d, U) = Σ (|Uj|/|U|) * I(Uj)
                j

    :param d: attribute
    :type d: string
    :param U: U set
    :type U: dataframe
    """
    last_col_name = U.columns[-1]
    last_col = U[last_col_name]
    state_values = last_col.unique().tolist()
    attr_col = U[d]
    attr_values = attr_col.unique().tolist()
    inf = 0
    # U_len - |U|
    U_len = len(U)
    for i in range(len(attr_values)):
        I_U = 0
        # Uj_len - |Uj|
        Uj_len = attr_col[attr_col == attr_values[i]].count()
        # I(U)
        for j in range(len(state_values)):
            count_occur = attr_col[(attr_col == attr_values[i]) & (last_col == state_values[j])].count()
            if Uj_len == 0 or count_occur/Uj_len == 0:
                continue
            I_U -= (count_occur/Uj_len)*m.log(count_occur/Uj_len, m.e)
        # Inf(d, Uj)
        inf -= (Uj_len/U_len)*I_U
    return inf


def input_decision(correct, decision, matrix):
    """
    Put decision into matrix.

    :param correct: correct decision
    :type correct: string
    :param decision: tree decision
    :type decision: string
    :param matrix: confusion matrix
    :type matrix: array
    """
    dict1 = {"not_recom":  0,
             "recommend":  1,
             "very_recom": 2,
             "priority":   3,
             "spec_prior": 4}
    for k in dict1.keys():
        if k == correct:
            row = dict1[k]
        if k == decision:
            col = dict1[k]
    matrix[row][col] += 1
    return matrix


def fill_confusion_matrix(data, tree1, matrix, n=12960):
    """
    Fills matrix with decisions.

    :param data: data set
    :type data: dataframe
    :param tree1: decision tree
    :type tree1: dict
    :param matrix: matrix to fill
    :type matrix: array
    :param n: number of decisions
    :type n: int
    """
    for i in range(0, n):
        person = data.iloc[i].to_dict()
        correct = person.popitem()[1]
        decision = get_decision(tree1, None, person, data)
        input_decision(correct, decision, matrix)
    return matrix


def calc_precision(matrix, length):
    """
    Calculates precision based on confusion matrix.

    :param matrix: confusion matrix
    :type matrix: array
    :param length: size of matrix
    :type length: int
    """
    correct = 0
    for row in range(len(matrix)):
        for col in range(len(matrix)):
            if row == col:
                correct += matrix[row][col]
    return correct/length


def ID3(U):
    """
    ID3 algorithm, creates decision tree based on training set
    using attribute information gains.

    :param U: training set
    :type U: dataframe
    """
    last_col = U.columns[-1]
    attr_cols = U.columns[:len(U.columns)-1].to_list()
    # maxInfGain = max(I(U)-Inf(d, U))
    info_gains = [calc_class_entropy(U)-abs(calc_attribute_inf(col, U)) for col in attr_cols]
    d = attr_cols[info_gains.index(max(info_gains))]
    decision_tree = {d: {}}
    for attr_val in U[d].unique():
        mask = U[d] == attr_val
        split_U = U[mask].reset_index(drop=True)
        val, num = np.asarray(np.unique(split_U[last_col], return_counts=True)).tolist()
        if len(num) > 1:
            decision_tree[d][attr_val] = ID3(split_U)
        elif len(num) == 1:
            decision_tree[d][attr_val] = [val[0]]
        else:
            continue
    return decision_tree


def create_and_test_tree(data, ratio):
    """
    Creates, tests tree and returns precision based on confusion matrix.

    :param data: entire set
    :type data: dataframe
    :param ratio: ratio to split data into two sets for testing and training
    """
    mask = np.random.rand(len(data)) < ratio
    train = copy.deepcopy(data[mask].reset_index(drop=True))
    test = copy.deepcopy(data[~mask].reset_index(drop=True))
    tree1 = ID3(train)
    conf_matrix = fill_confusion_matrix(test, tree1, copy.deepcopy(confusion_matrix), len(test))
    print(np.matrix(conf_matrix))
    return calc_precision(conf_matrix, len(test))


if __name__ == '__main__':
    # CONFIGURATION
    columns = ["parents", "has_nurs", "form", "children", "housing", "finance", "social", "health", "state"]
    data = pd.read_csv("nursery.data", names=columns, header=None)
    # train/test set size ratio
    ratio = 0.7  # splitting ratio
    prec = create_and_test_tree(data, ratio)
    print("Precision:", round(prec, 2))
