from math import log, inf


class Node:
    leaves = []

    def __init__(self, attribute, children=None):
        self.attribute = attribute
        self.children = children
        self.parent = None
        self.next = None


def ID3(R, S, Y):   # R - non-categorical attributes, S - training set, Y - classes
    if not S:
        return Node('Failure')
    value = set()
    for i in S:
        value.add(i['class'])
        if len(value) > 1:
            break

    if len(value) == 1:
        n = Node(value.pop())
        Node.leaves.append(n)
        return n

    if not R:
        count = dict.fromkeys(Y, 0)
        for i in S:
            count[i['class']] += 1

        maxCount = -inf
        for x, y in count.items():
            if y > maxCount:
                maxCount = y
                ans = x

        n = Node(ans)
        Node.leaves.append(n)
        return n

    maxInfGain = -inf
    ent = entropy(S, Y)
    for i in R:
        InfGain = ent - AveInfEnt(R, i, S, Y)
        if InfGain > maxInfGain:
            maxInfGain = InfGain
            d = i

    root = Node(d, list(R[d]))
    R.pop(d)
    child = []
    for i in root.children:
        child.append(ID3(R, [x for x in S if x[d] == i], Y))

    for i in child:
        i.parent = root

    root.next = child

    return root


def entropy(S, Y):
    count = dict.fromkeys(Y, 0)

    for i in S:
        count[i['class']] += 1

    entr = 0
    for i in count.values():
        if i != 0:
            entr -= (i/len(S) * log(i/len(S)))

    return entr


def AveInfEnt(R, attr, S, Y):

    ans = 0
    for i in R[attr]:
        S_attr = [x for x in S if x[attr] == i]
        ans += len(S_attr)/len(S)*entropy(S_attr, Y)

    return ans
