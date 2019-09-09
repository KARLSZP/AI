#include <iostream>
#include <algorithm> 
#include <cstdlib> 
#include <vector>
using namespace std; 

const int SIZE = 4; 
int Map[SIZE][SIZE] =  { {9, 1, 12, 15},  {4, 3, 11, 0},  {14, 2, 5, 8}, {10, 13, 6, 7}}; 
// int Map[SIZE][SIZE] =  { {7, 5, 2, 4},  {9, 0, 1, 8},  {6, 10, 3, 12},  {13, 14, 11, 15}}; 
const int fact[10] = {1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880};

int h(int **node) {
    int val = 0;
    for(int i = 0;i<SIZE;i++) {
        for(int j = 0;j<SIZE;j++) {
            val += abs(i - (node[i][j]-1)/SIZE) + abs(j - (node[i][j]-1)%SIZE);
        }
    }
    return (int)val;
}


void generate(int **m) {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            cout << m[i][j] << " "; 
        }
        cout << endl; 
    }
}

bool is_goal(int **node) {
    int t = 1;
    for(int i = 0;i<SIZE;i++) {
        for(int j = 0;j<SIZE;j++) {
            if(node[i][j]!=t) break;
            else t++;
        }
    }
    return (t == 16);
}

bool cmp(int **a, int **b) {
    return h(a) < h(b);
}

vector<int **> successor(int **node) {
    int x = 0, y = 0;
    vector<int **> succ;
    for(int i = 0;i<SIZE;i++) {
        for(int j = 0;j<SIZE;j++) {
            if(node[i][j]==0) {
                x = i;
                y = j;
            }
        }
    }
    int dirs[4][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
    for(int i = 0;i<4;i++) {
        int **tmp = new int *[SIZE];
        for(int j = 0;j<SIZE;j++) {
            tmp[j] = new int[SIZE];
        }
        for(int m = 0;m<SIZE;m++) {
            for(int n = 0;n<SIZE;n++) {
                tmp[m][n] = node[m][n];
            }
        }
        int _x = x + dirs[i][0];
        int _y = y + dirs[i][1];
        if(_x>=0&&_x<SIZE&&_y>=0&&_y<SIZE) {
            tmp[x][y] = tmp[_x][_y];
            tmp[_x][_y] = 0;
            succ.push_back(tmp);
        }
    }
    sort(succ.begin(), succ.end(), cmp);
    // for(int i = 0;i<succ.size();i++) {
    //     cout<<h(succ[i])<<endl;
    //     generate(succ[i]);
    //     cout<<endl;
    // }
    return succ;
}

int contor(int ** permutation, int n) {
    int num = 0;
    for (int i = 0; i < n; ++i) {
        int cnt = 0; // 在 i 之后，比 i 还小的有几个
        for (int j = i + 1; j < n; ++j)
            if (permutation[i] > permutation[j]) ++cnt;
        num += cnt * fact[n - i - 1];
    }
    return num + 1;
}

bool in_path(vector<int **> &path, int **node) {
    bool check;
    for(int i = 0;i<path.size();i++) {
        check = true;
        for(int j = 0;j<SIZE;j++) {
            for(int k = 0;k<SIZE;k++) {
                if(node[j][k]!=path[i][j][k]) {
                    check = false;
                    break;
                }
            }
            if(!check) break;
        }
        if(check) break;
    }
    return check;
}

int search(vector<int **> &path, int g, int bound) {
    int **node = path.back();
    // generate(node);
    int f = g + h(node);
    if(f > bound) return f;
    else if(is_goal(node)) {
        generate(node);
        cout<<"Goal!"<<endl;
        return -1;
    }
    int min_dist = INT_MAX;
    vector<int **> successors = successor(node);
    for(int i = 0;i<successors.size();i++) {
        if(in_path(path, successors[i])) continue;
        path.push_back(successors[i]);
        int t = search(path, g + 1, bound);
        if(t==-1) return -1;
        if(t<min_dist) min_dist = t;
        path.pop_back();
    }
    return min_dist;
}

vector<int **> ida_star(int **root) {
    int bound = h(root);
    vector<int **> path;
    path.push_back(root);
    int t = 0;
    while(1) {
        t = search(path, 0, bound);
        cout<<"ida*: "<<t<<endl;
        if(t==-1) return path;
        if(t==INT_MAX) {
            path.clear();
            return path;
        }
        bound = t;
    }
}

int ** load() {    
    int ** ptr = new int *[SIZE]; 
    for (int i = 0; i < SIZE; i++) {
        ptr[i] = new int[SIZE]; 
        ptr[i] = (Map[i]);
    }
    return ptr; 
}

int main() {
    int **Map = load(); 
    cout<<"\n\n >>> Puzzle - "<< "1" << ">>>"<<endl;
    generate(Map);
    cout<<" <<< Puzzle - " << "1" << "<<<"<<endl;
    // tik = time.time()
    vector<int **> path = ida_star(Map);
    cout<<path.size()<<endl;
    // tok = time.time()
    for(int i = 0;i<path.size();i++) {
        cout << "\n >>> Step " << i << ">>>"<<endl;
        generate(path[i]);
    }

    cout << "IDA* for Puzzle - " << "1" << ":"<<endl;
    // cout << "Optimal Solution:" << path.size() - 1 << "steps."<<endl;
    // cout << "Generated in:" << 1000*(tok - tik) << "ms.";
    system("pause");
    return 0; 
}