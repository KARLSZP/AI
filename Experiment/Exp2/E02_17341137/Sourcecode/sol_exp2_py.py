# AI - exp 2 - python - 15Puzzle
# ID: 17341137

import sys
import time


# Estimated cost of the cheapest path (node-to-goal)
def h(node):
    val = 0
    for i in range(len(node)):
        for j in range(len(node[0])):
            if not node[i][j]:
                val += abs(3-i) + abs(3-j)
            else:
                val += abs(i - (node[i][j]-1)/4) + abs(j - (node[i][j]-1) % 4)
    return int(val)


# Step cost func.
def cost(node, succ):
    return 1


# Goal test
def is_goal(node):
    t = 1
    for i in node:
        for j in i:
            if j != t:
                break
            else:
                t += 1
    return t == 16


# node expanding func.
def successors(node):
    x, y = 0, 0
    succ = []
    for i in range(len(node)):
        for j in range(len(node[0])):
            if node[i][j] == 0:
                x, y = i, j
    dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    for i, j in dirs:
        tmp = [[r for r in c] for c in node]
        _x, _y = x + i, y + j
        if 0 <= _x < len(node) and 0 <= _y < len(node[0]):
            tmp[x][y] = tmp[_x][_y]
            tmp[_x][_y] = 0
            succ.append(tmp)
    return sorted(succ, key=lambda t: h(t))


# return NOT_FOUND or (best_path, cost)
def ida_star(root):
    bound = h(root)
    path = [root]
    while 1:
        t = search(path, 0, bound)
        if t == "FOUND":
            return path, bound
        if t == sys.maxsize:
            return [], sys.maxsize
        bound = t


# DFS
def search(path, g, bound):
    node = path[-1]
    f = g + h(node)
    if f > bound:
        return f
    elif is_goal(node):
        print("\nGoal!")
        return "FOUND"
    min_dist = sys.maxsize
    for succ in successors(node):
        if succ in path:
            continue
        path.append(succ)
        t = search(path, g + cost(node, succ), bound)
        if t == "FOUND":
            return "FOUND"
        if t < min_dist:
            min_dist = t
        path.pop()
    return min_dist


def load():
    Map = [
        [[7, 5, 2, 4],
         [9, 0, 1, 8],
         [6, 10, 3, 12],
         [13, 14, 11, 15]],
        [[2, 10, 3, 4],
         [1, 9, 6, 7],
         [13, 5, 11, 8],
         [0, 14, 15, 12]],
        [[3, 4, 1, 0],
         [5, 2, 10, 8],
         [9, 7, 6, 11],
         [13, 14, 15, 12]]
    ]
    return Map


def generate(Map):
    for i in Map:
        for j in i:
            if j == 0:
                print("\t\033[41m 0\033[0m", end=" ")
            else:
                print("\t%2d" % j, end=" ")
        print("")


if __name__ == "__main__":
    # Generate the Map
    MAP = load()
    for i in range(len(MAP)):
        print("\n\n >>> Puzzle - ", i, ">>>")
        generate(MAP[i])
        print(" <<< Puzzle - ", i, "<<<")
        tik = time.time()
        (path, bound) = ida_star(MAP[i])
        tok = time.time()
        for node in range(len(path)):
            print("\n >>> Step ", node, ">>>")
            generate(path[node])
        print("IDA* for Puzzle - ", i, ":")
        print("Optimal Solution:", len(path) - 1, "steps.")
        print("Generated in:", 1000*(tok - tik), "ms.")
