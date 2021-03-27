from math import sqrt
from ID3 import Node
from math import inf


def getMostCommonClass(data, Y, prevAttr):
    count = dict.fromkeys(Y, 0)
    for instance in data:
        isInSubTree = True
        for x, y in prevAttr.items():
            if instance[x] != y:
                isInSubTree = False

        if isInSubTree:
            count[instance['class']] += 1

        maxCount = -inf
        for x, y in count.items():
            if y > maxCount:
                maxCount = y
                ans = x

    return Node(ans)


def C45pruning(root, data, Y):
    for leave in Node.leaves:
        w = leave
        w = w.parent
        while w.parent is not None:
            prevAttr = getPrevAttr(w)
            e0 = TError(w, data, prevAttr)
            c = getMostCommonClass(data, Y, prevAttr)
            p = w.parent
            p.next[p.next.index(w)] = c
            e1 = TError(w, data, prevAttr)
            if e0 >= e1:
                c.parent = p
                delLeaves(w)

            else:
                p.next[p.next.index(c)] = w

            w = w.parent


def TError(root, data, prevAttr):
    e = 0
    c = 0   # ile instancji z data należy do tego poddrzewa
    for instance in data:
        isInSubTree = True
        for x, y in prevAttr.items():
            if instance[x] != y:
                isInSubTree = False
                break

        if isInSubTree:
            c += 1
            e += evaluate(root, instance)

    if e == 0:
        return 0
    e /= c
    return e + sqrt(e*(1-e))/c


def evaluate(root, instance):
    if root.children is None:
        if root.attribute == instance['class']:
            return 0
        else:
            return 1

    for i in range(len(root.children)):
        if root.children[i] == instance[root.attribute]:
            return evaluate(root.next[i], instance)

    return None


def delLeaves(root):
    if root.next is None:
        if root in Node.leaves:
            Node.leaves.remove(root)
        return
        return
    for i in root.next:
        delLeaves(i)


def getPrevAttr(w):
    d = {}
    prev = w
    w = w.parent
    while w is not None:
        d[w.attribute] = w.children[w.next.index(prev)]
        prev = w
        w = w.parent

    return d
