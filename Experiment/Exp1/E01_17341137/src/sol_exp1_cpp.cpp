// AI - exp 1 - cpp - Pacman
// ID:17341137

#include <iostream> 
#include <fstream>
#include <string> 
#include <vector> 
#include <utility>
using namespace std; 
vector < pair < int, int > > res; 

void formatprint(vector < string >  & map) {
    for (int i = 0; i < map.size(); i++) {
        for (int j = 0; j < map[0].size(); j++) {
            cout << map[i][j] << " "; 
        }
        cout << endl; 
    }
}


void printpath(vector < string > map, vector < pair < int, int > > path) {
    cout << "Shortest Path with " << path.size() << "steps! (Noted with '#')" << endl; 
    for (int i = 0; i < path.size(); i++) {
        map[path[i].first][path[i].second] = '#'; 
    }
    formatprint(map); 
}


bool in(vector < pair < int, int > > path, int itemx, int itemy) {
    for (int i = 0; i < path.size(); i++) {
        if (path[i].first == itemx && path[i].second == itemy) {
            return true; 
        }
    }
    return false; 
}

void dfs(vector <string> & map, int x, int y, vector <pair<int, int> > used) {
    if (res.size() && res.size() < used.size())
        return;
    else if (x == -1 || y == -1 || x == map.size() || y == map[0].size() || map[x][y] == '1' || in(used, x, y))
        return; 
    else if (map[x][y] == 'E') {
        if (used.size() + 1 < res.size() || res.empty()) {
            res = used; 
            res.push_back(make_pair(x, y)); 
        }
        return; 
    }
    else {
        used.push_back(make_pair(x, y));
        dfs(map, x + 1, y, used);
        dfs(map, x - 1, y, used);
        dfs(map, x, y + 1, used);
        dfs(map, x, y - 1, used);
        used.pop_back(); 
    }
}


int main() {
    string FilePath = "./MazeData.txt"; 
    ifstream MazeFile(FilePath.c_str()); 
    vector < string > Maze_with_nums; 
    vector < pair < int, int > > used; 
    if (MazeFile.is_open()) {
        string buf; 
        while (getline(MazeFile, buf)) {
            if (buf[0] == '0' || buf[0] == '1') {
                Maze_with_nums.push_back(buf); 
            }
        }
        formatprint(Maze_with_nums); 
    }

    // Solution
    for (int i = 0; i < Maze_with_nums.size(); i++) {
        for (int j = 0; j < Maze_with_nums[0].size(); j++) {
            if (Maze_with_nums[i][j] == 'S') {
                dfs(Maze_with_nums, i, j, used); 
                break; 
            }
        }
    }

    // Print the result
    printpath(Maze_with_nums, res); 
    return 0; 
}
