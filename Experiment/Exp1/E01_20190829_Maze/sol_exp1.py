# AI - exp 1 - python - Pacman
# ID: 17341137

import sys
sys.setrecursionlimit(10000)


def formatprint(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            print(map[i][j], end=' ')
        print("")
    print("")


def printpath(map, path):
    print("Shortest Path with %d steps! (Noted with '#')" % len(path))
    for i in range(len(map)):
        for j in range(len(map[i])):
            if (i, j) in path[1:-1]:
                print('#', end=" ")
            else:
                print(map[i][j], end=" ")
        print("")
    print("")


def dfs(map, x, y, used):
    global res
    if len(res) and len(used) > len(res):
        return
    if x == -1 or y == -1 or x == len(map) or y == len(map[0]) or map[x][y] == '1' or (x, y) in used:
        return
    elif map[x][y] == 'E':
        # print("goal with %d" % (len(used) + 1))
        if len(used) + 1 < len(res) or len(res) == 0:
            res = used
            res.append((x, y))
        return
    else:
        used.append((x, y))
        dfs(map, x + 1, y, used[:])
        dfs(map, x - 1, y, used[:])
        dfs(map, x, y + 1, used[:])
        dfs(map, x, y - 1, used[:])
        used.remove(used[-1])


if __name__ == "__main__":
    # Generate the Map
    FilePath = "./MazeData.txt"
    Maze_with_nums = []
    res = []
    with open(FilePath, 'r') as Maze:
        for i in Maze.readlines():
            if i[0] == '1' or i[0] == '0':
                Maze_with_nums.append(i[:-1])
    formatprint(Maze_with_nums)

    # Solution
    for i in range(len(Maze_with_nums)):
        for j in range(len(Maze_with_nums[i])):
            if Maze_with_nums[i][j] == 'S':
                dfs(Maze_with_nums, i, j, [])
                break
    # Print the result
    printpath(Maze_with_nums, res)
