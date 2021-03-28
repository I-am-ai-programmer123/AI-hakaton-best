from WSI3_checkers_functions import *
import copy
from matplotlib import pyplot as plt

class Node:
    def __init__(self, field, parent, color):
        self.field = field
        self.parent = parent
        self.reward = rate_field(field)
        self.children = {}
        self.color = color
        self.alfa = None
        self.beta = None
        self.alfa_pointer = None
        self.beta_pointer = None


def create_or_update(root, update_depth):
    # print(update_depth)
    if update_depth == 0:
        return
    # print_field(root.field)
    if not root.children:
        if root.color == 'B':
            moves = generate_black_moves(root.field)
            # print(moves)
            for move in moves:
                root.children[move] = Node(generate_new_field(root.field, move), root, 'W')
        else:
            moves = generate_white_moves(root.field)
            # print(moves)
            for move in moves:
                root.children[move] = Node(generate_new_field(root.field, move), root, 'B')
    for child in root.children:
        create_or_update(root.children[child], update_depth-1)

def alfa_beta_pruning_white(root):

    if root.children:
        root.alfa = -float("inf")
        for child in root.children:
            alfa_beta_pruning_white(root.children[child])

    if not root.children:
        root.alfa = root.reward
        return

    for child in root.children:
        if root.children[child].alfa > root.alfa:
            root.alfa = max(root.alfa, root.children[child].alfa)
            root.alfa_pointer = child

    if root.color == 'W':
        root.children = {root.alfa_pointer: root.children[root.alfa_pointer]}

def alfa_beta_pruning_black(root):

    if root.children:
        root.beta = float("inf")
        for child in root.children:
            alfa_beta_pruning_black(root.children[child])

    if not root.children:
        root.beta = root.reward
        return

    for child in root.children:
        if root.children[child].beta < root.beta:
            root.beta = min(root.beta, root.children[child].beta)
            root.beta_pointer = child

    if root.color == 'B':
        root.children = {root.beta_pointer: root.children[root.beta_pointer]}






field = [
['B', '_', 'B', '_', 'B', '_', 'B', '_'],   # 0
['_', 'B', '_', 'B', '_', 'B', '_', 'B'],   # 1
['B', '_', 'B', '_', 'B', '_', 'B', '_'],   # 2
['_', '_', '_', '_', '_', '_', '_', '_'],   # 3
['_', '_', '_', '_', '_', '_', '_', '_'],   # 4
['_', 'W', '_', 'W', '_', 'W', '_', 'W'],   # 5
['W', '_', 'W', '_', 'W', '_', 'W', '_'],   # 6
['_', 'W', '_', 'W', '_', 'W', '_', 'W']    # 7
]


# while root.children:
#     myfile.write("---------------")
#     myfile.write('\n')
#     # print_field(root.field)
#     for i in range(len(root.field)):
#         myfile.write(str(root.field[i]))
#         myfile.write('\n')

#     for child in root.children:
#         root = root.children[child]
#         break
def simulate_game(game_len):
    root = Node(field, None, 'W')
    create_or_update(root, 4)
    alfa_beta_pruning_white(root)
    alfa_beta_pruning_black(root)
    myfile = open("pc_vs_pc.txt", "a+")
    x = [k for k in range(game_len)]
    y = []

    for j in range(game_len):
        if not root.children:
            create_or_update(root, 4)
            alfa_beta_pruning_white(root)
            alfa_beta_pruning_black(root)
        myfile.write("---------------")
        myfile.write('\n')
        # print_field(root.field)
        for i in range(len(root.field)):
            myfile.write(str(root.field[i]))
            myfile.write('\n')
        y.append(root.reward)
        for child in root.children:
            root = root.children[child]
            break
    
    plt.plot(x, y)
    plt.show()


def play_as_white():
    root = Node(field, None, 'W')
    create_or_update(root, 4)
    alfa_beta_pruning_black(root)
    while True:
        if not root.children:
            create_or_update(root, 4)
            alfa_beta_pruning_black(root)
        print_field(root.field)
        print(root.children.keys())
        move = str(input())
        if move not in root.children:
            print("wrong move")
            return
        root = root.children[move]
        if not root.children:
            create_or_update(root, 4)
            alfa_beta_pruning_black(root)
        print("--------------------------")
        print("--------------------------")
        print("--------------------------")
        print("--------------------------")
        print("--------------------------")
        print("--------------------------")
        print_field(root.field)
        print("--------------------------")
        print("--------------------------")
        print("--------------------------")
        print("--------------------------")
        print("--------------------------")
        print("--------------------------")
        for child in root.children:
            root = root.children[child]
            break




def play_as_black():
    root = Node(field, None, 'W')
    create_or_update(root, 4)
    alfa_beta_prun0ing_white(root)
    while True:
        if not root.children:
            create_or_update(root, 4)
            alfa_beta_pruning_white(root)
        print_field(root.field)

        for child in root.children:
            root = root.children[child]
            break
        print("--------------------------")
        print("--------------------------")
        print("--------------------------")
        print("--------------------------")
        print("--------------------------")
        print("--------------------------")
        print_field(root.field)


        print(root.children.keys())
        move = str(input())
        if move not in root.children:
            print("wrong move")
            return
        root = root.children[move]
        print("--------------------------")
        print("--------------------------")
        print("--------------------------")
        print("--------------------------")
        print("--------------------------")
        print("--------------------------")

        if not root.children:
            create_or_update(root, 4)
            alfa_beta_pruning_white(root)






simulate_game(50)
# play_as_white()
# play_as_black()