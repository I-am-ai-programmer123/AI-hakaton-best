#!/usr/bin/env python3

import csv
from ID3 import ID3
from C45 import C45pruning
from random import shuffle


def getError(root, data):
    counter = 0
    for instance in data:
        w = root
        while w.next is not None:
            w = w.next[w.children.index(instance[w.attribute])]

        if instance['class'] == w.attribute:
            counter += 1

    return counter/len(data)


def errorMatrix(root, data):
    matrix = [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]
            ]

    classes = {'unacc': 0, 'acc': 1, 'good': 2, 'vgood': 3, 'Failure': 4}
    for instance in data:
        w = root
        while w.next is not None:
            w = w.next[w.children.index(instance[w.attribute])]

        matrix[classes[instance['class']]][classes[w.attribute]] += 1

    for row in matrix:
        for i in range(len(row)):
            row[i] = row[i]

    return matrix


def values(data):
    s = set()
    for i in data:
        s.add(i['class'])
    return s


def attributes(data):
    attr = data[0].copy()
    for key in attr:
        attr[key] = set()

    for instance in data:
        for x, y in instance.items():
            attr[x].add(y)

    attr.pop('class')
    return attr


def getData():
    data = []
    # with open('car.data', newline='') as file:
    #     fieldnames = ['buying', 'maint', 'doors', 'persons', 'lung_boot', 'safety', 'class']
    with open('audiology.standardized.data', newline='') as file:
        fieldnames = [
            'age_gt_60',
            'air()',
            'airBoneGap',
            'ar_c()',
            'ar_u()',
            'bone()',
            'boneAbnormal',
            'bser()',
            'history_buzzing',
            'history_dizziness',
            'history_fluctuating',
            'history_fullness',
            'history_heredity',
            'history_nausea',
            'history_noise',
            'history_recruitment',
            'history_ringing',
            'history_roaring',
            'history_vomiting',
            'late_wave_poor',
            'm_at_2k',
            'm_cond_lt_1k',
            'm_gt_1k',
            'm_m_gt_2k',
            'm_m_sn',
            'm_m_sn_gt_1k',
            'm_m_sn_gt_2k',
            'm_m_sn_gt_500',
            'm_p_sn_gt_2k',
            'm_s_gt_500',
            'm_s_sn',
            'm_s_sn_gt_1k',
            'm_s_sn_gt_2k',
            'm_s_sn_gt_3k',
            'm_s_sn_gt_4k',
            'm_sn_2_3k',
            'm_sn_gt_1k',
            'm_sn_gt_2k',
            'm_sn_gt_3k',
            'm_sn_gt_4k',
            'm_sn_gt_500',
            'm_sn_gt_6k',
            'm_sn_lt_1k',
            'm_sn_lt_2k',
            'm_sn_lt_3k',
            'middle_wave_poor',
            'mod_gt_4k',
            'mod_mixed',
            'mod_s_mixed',
            'mod_s_sn_gt_500',
            'mod_sn',
            'mod_sn_gt_1k',
            'mod_sn_gt_2k',
            'mod_sn_gt_3k',
            'mod_sn_gt_4k',
            'mod_sn_gt_500',
            'notch_4k',
            'notch_at_4k',
            'o_ar_c()',
            'o_ar_u()',
            's_sn_gt_1k',
            's_sn_gt_2k',
            's_sn_gt_4k',
            'speech()',
            'static_normal',
            'tymp()',
            'viith_nerve_signs',
            'wave_V_delayed',
            'waveform_ItoV_prolonged',
            'indentifier',
            'class'
            ]
        reader = csv.DictReader(file, fieldnames=fieldnames)
        for row in reader:
            row.pop('indentifier')
            data.append(row)

    return data


def draw(root):
    if root.children is None:
        return

    print(root.attribute)
    print(' '.join(root.children))
    s = ''
    for i in root.next:
        s += i.attribute
        s += ' '

    print(s)

    for i in root.next:
        draw(i)


def show(res):
    classes = {0: 'unacc', 1: 'acc', 2: 'good', 3: 'vgood', 4: 'Failure'}
    print("\n\tunacc acc good vgood Failure")
    for idx, row in enumerate(res):
        print(f"{classes[idx]}\t{row}")


def measure():
    matrix1 = [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]
            ]

    error1 = 0

    matrix2 = [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]
            ]

    error2 = 0
    n = 1
    for i in range(n):
        data = getData()
        shuffle(data)

        R = attributes(data)
        Y = values(data)

        root = ID3(R, data[int(len(data)*1/3):], Y)
        draw(root)
        print()

        # res1 = errorMatrix(root, data[:int(len(data)*1/3)])

        err1 = getError(root, data[:int(len(data)*1/3)])

        C45pruning(root, data[int(len(data)*1/3):], Y)
        draw(root)

        # res2 = errorMatrix(root, data[:int(len(data)*1/3)])

        err2 = getError(root, data[:int(len(data)*1/3)])

        # for y in range(len(matrix1)):
        #     for x in range(len(matrix1[0])):
        #         matrix1[y][x] += res1[y][x] / int(len(data)*1/3)
        #         matrix2[y][x] += res2[y][x] / int(len(data)*1/3)

        error1 += err1
        error2 += err2

    # for y in range(len(matrix1)):
    #     for x in range(len(matrix1[0])):
    #         matrix1[y][x] = round(matrix1[y][x] / n, 2)
    #         matrix2[y][x] = round(matrix2[y][x] / n, 2)

    error1 = round(error1/n, 3)
    error2 = round(error2/n, 3)

    print(f"Error ID3: {error1}")
    print(f"Error C4.5: {error2}")

    # print()
    # show(matrix1)
    # print()
    # show(matrix2)


if __name__ == "__main__":
    measure()
