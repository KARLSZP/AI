/**
 * Futoshiki Using GAC algorithm.
 * Futoshiki: https://www.futoshiki.org/
 * 
 * Author: Karl
 * ID: 17341137
 * 
 **/

#include<iostream>
#include<cstring>
#include<vector>
#include<chrono>
using namespace std;
using namespace chrono;
#define DWO false

// Define the SIZE of the chessboard.
// Test cases from 4 to 9.
const int SIZE = 8;

// Denotes the times GAC() is called.
static int nodes = 0;

// Use <chrono> to count the elapsing time.
auto _start = std::chrono::system_clock::now();

/* ###################################################################################### */
/* DEFINITION  */
// Position of the block.
struct Position{
    int row, col;
    Position() {}
    Position(int a, int b): row(a), col(b) {}
};

// Relation from one block to its 'enemy'.
struct Relation {
    Position enemy;
    int r;                      // 1 for {'>'}, -1 for {'<'}.
    Relation() {}
    Relation(Position a, int re): enemy(a), r(re) {}
};

// Relations of the whole board.
struct MultiRelation {
    Position x, y;
    int r;
    MultiRelation() {}
    MultiRelation(Position a, Position b, int re): x(a), y(b), r(re) {}
};

// Each block is defined as a 'Do'.
struct Do {
    int val;                    // {VALUE}.
    Position pos;               // {POSITION} on the board.
    int curdom[SIZE+1];         // curdom[1] to curdom[SIZE]: 1 for {INVALID}, 0 for {VALID}.
                                // curdom[0] stores the number of {INVALID} choices.
    bool assigned;              // 1 for {ASSIGNED}, 0 for {UNASSIGNED}
    vector<Relation> relation;  // List of {RELATION} between other 'Do' and itself.
    Do() {}
};

// The futoshiki game.
struct futoshiki {
    Do board[SIZE+1][SIZE+1];               // The chessboard.
    vector<MultiRelation> multirelation;    // The relationship List.
    futoshiki() {}
};

/* ###################################################################################### */
/* Fuctions */
// GAC & GAC_Enforce
void GAC(futoshiki* FTSK);
bool GAC_Enforce(futoshiki* FTSK, Do* v);

// Heuristic Function Using MRV
Do* heuristicpick(futoshiki* FTSK);

// Helper Functions
bool Goal(futoshiki* FTSK);
bool RowCheck(futoshiki* FTSK, Do* m);
bool ColCheck(futoshiki* FTSK, Do* m);
bool NeiCheck(futoshiki* FTSK);
int CDcount(Do* m);
void Copyboard(futoshiki* dest, const futoshiki* src);
void display(futoshiki* FTSK);

/* ###################################################################################### */
/* MAIN FUNCTION */
int main() {
// 1. Initialization
    futoshiki FTSK;
    futoshiki* ptr = &FTSK;
    for (int i = 1;i<=SIZE;i++) {
        for (int j = 1;j<=SIZE;j++) {
            ptr->board[i][j].val = 0;
            ptr->board[i][j].pos.row = i;
            ptr->board[i][j].pos.col = j;
            ptr->board[i][j].assigned = 0;
            memset(ptr->board[i][j].curdom, 0, sizeof(ptr->board[i][j].curdom));
        }
    }
// 2. Input Chessboard
    cout << "FUTOSHIKI Solver Ver 1.2" << endl;
    cout << "\n>>> Please Input as 'a b < c d'" << endl;
    cout << "E.g.:" << endl;
    cout << "   1 1 < 1 2" << endl;
    cout << "   2 1 > 1 1" << endl;
    cout << "   0 0 0 0 0 (As the end of RELATIONS.)" << endl;
    while(1) {
        Position x, y;
        char c;        
        cin >> x.row >> x.col >> c >> y.row >> y.col;
        if (c!='<' && c!='>') break;
        Relation tmp1(y, ((c == '>') ? 1 : -1));
        Relation tmp2(x, ((c == '>') ? -1 : 1));
        MultiRelation tmp(x, y, ((c == '>') ? 1 : -1));
        ptr->multirelation.push_back(tmp);
        ptr->board[x.row][x.col].relation.push_back(tmp1);
        ptr->board[y.row][y.col].relation.push_back(tmp2);
    }
    cout << "\n>>> Please Input pre-set value as 'a b v': " << endl;
    cout << "E.g.:" << endl;
    cout << "   1 1 3" << endl;
    cout << "   0 0 0 (As the end of pre-set values)" << endl;
    while(1) {
        int a, b, v;
        cin >> a >> b >> v;
        if (a+b+v == 0) break;
        ptr->board[a][b].val = v;
        ptr->board[a][b].assigned = 1;
        GAC_Enforce(ptr, &ptr->board[a][b]);
    }
    cout << ">>> Futoshiki Board:" << endl;
    display(ptr);
// 3. Generate the Result
    cout << ">>> Solving..." << endl;
    _start = std::chrono::system_clock::now();
    GAC(ptr);
    system("pause");
    return 0;
}

/* ###################################################################### */
/* Implementation */
bool GAC_Enforce(futoshiki* FTSK, Do* v) {
    bool flag_row = 0, flag_col = 0, flag_compare = 0;
    flag_row = RowCheck(FTSK, v);                   // {FALSE} if DWO occured.
    flag_col = ColCheck(FTSK, v);                   // {FALSE} if DWO occured.
    flag_compare = NeiCheck(FTSK);                  // {FALSE} if DWO occured.
    return (flag_row && flag_col && flag_compare);  // Return the LOGIC-AND of each flag.
}

void GAC(futoshiki* FTSK) {
    nodes++;
    if (Goal(FTSK)) {
        // Return when all cells are assigned.
        auto _end = std::chrono::system_clock::now();
        std::chrono::duration<double> elapsed_seconds = _end - _start;
        cout << ">>> Goal!" << endl;
        display(FTSK);
        cout << "=========================================" << endl;
        cout << "GAC has been called for " << nodes << " times." << endl;
        cout << "Solution generated in " << elapsed_seconds.count() << " s." << endl;
        cout << "=========================================" << endl;
        exit(0);
    }
    Do* v = heuristicpick(FTSK); // Pick an {UN-ALL-ASSIGNED} node with MRV
    v->assigned = true;
    for (int i = 1;i<=SIZE;i++) if (!v->curdom[i]) {
        v->val = i;
        futoshiki boardcopy;    // Store the chessboard, in case of DWO.
        Copyboard(&boardcopy, FTSK);
        // Prune all other values (GAC's feature)
        for (int j = 1;j<=SIZE;j++) if (j != i && !v->curdom[j]) { 
            v->curdom[j] = 1;
            v->curdom[0] = CDcount(v);
        }
        if (GAC_Enforce(FTSK, v) != DWO) {
            GAC(FTSK);
        }
        Copyboard(FTSK, &boardcopy); // DWO occured, Restore from copy.
    }
    v->assigned = false;
}

// Count all {INVALID} values to update {curdom[0]}.
int CDcount(Do* m) {
    int res = 0;
    for (int i = 1;i<=SIZE;i++) {
        res += m->curdom[i];
    }
    return res;
}

/**
 * To Prune the assigned value from other member in the constraint's scope.
 * In other words, remove the value from the member's domain and check if 
 * the domain is empty. If so, raise a DWO.
*/
bool RowCheck(futoshiki* FTSK, Do* m) {
    int row = m->pos.row;
    int val = m->val;
    for(int i = 1;i<=SIZE;i++) {
        Do* current_Do = &FTSK->board[row][i];        
        if (current_Do->assigned) continue;
        if (!current_Do->curdom[val]) {
            current_Do->curdom[val] = 1;
            current_Do->curdom[0] = CDcount(&FTSK->board[row][i]);
        }
        if(current_Do->curdom[0] == SIZE) return false;
    }
    return true;
}

bool ColCheck(futoshiki* FTSK, Do* m) {
    int col = m->pos.col;
    int val = m->val;
    for(int i = 1;i<=SIZE;i++) {
        Do* current_Do = &FTSK->board[i][col];
        if (current_Do->assigned) continue;
        if (!current_Do->curdom[val]) {
            current_Do->curdom[val] = 1;
            current_Do->curdom[0] = CDcount(&FTSK->board[i][col]);
        }
        if(current_Do->curdom[0] == SIZE) return false;
    }
    return true;
}

/**
 * NeiCheck denote Neighbour Check.
 * For each relation in the futoshiki,
 *  | X, Y :- two members;
 *  | re   :- relation (1 for '>' & -1 for '<')
 *  | x_row, x_col, y_row, y_col: positions.
 * 
 * Rules may seem to be a little tricky:
 *  1. Both X and Y are assigned:
 *      | Nothing to do, pass.
 *  2. One is assigned, the other is not (Assume X is assigned):
 *      | (2.1) get X's value, store in 'v'
 *      | (2.2) for values in Y's domain that are still valid,
 *      |       if X > Y (re == 1):
 *      |           Prune those exceed or equal to 'v'.('v' to SIZE)
 *      |       if X < Y (re == -1):
 *      |           Prune those behind or equal to 'v'.(1 to 'v')
 *  3. Neither X or Y is assigned:
 *      | (3.1) If X > Y (re == 1):
 *      |           For each value in X'domain (Assume as 'xd'):
 *      |               if all values in Y's domain exceed 'xd',
 *      |               remove 'xd'.
 *      |           For each value in Y'domain (Assume as 'yd'):
 *      |               if all values in Y's domain are behind 'yd',
 *      |               remove 'yd'.
 *      | (3.2) Vice versa.
 */
bool NeiCheck(futoshiki* FTSK) {
    bool flag = true;
    for (size_t m = 0;m<FTSK->multirelation.size();m++) {
        int x_row = FTSK->multirelation[m].x.row;
        int x_col = FTSK->multirelation[m].x.col;
        int y_row = FTSK->multirelation[m].y.row;
        int y_col = FTSK->multirelation[m].y.col;
        Do* X = &FTSK->board[x_row][x_col];
        Do* Y = &FTSK->board[y_row][y_col];
        int re = FTSK->multirelation[m].r;
        
        // Both assigned, Ignore.
        if (X->assigned && Y->assigned) continue;

        // One assigned, prune the other.
        else if (X->assigned) {
            int v = X->val;
            if (re == 1) {
                for (int j = v;j<=SIZE;j++) if (!Y->curdom[j]) {
                    Y->curdom[j] = 1;
                    Y->curdom[0] = CDcount(Y);
                }
                if(Y->curdom[0] == SIZE) flag = false;
            }
            else if (re == -1)  {
                for (int j = v;j>0;j--) if (!Y->curdom[j]) {
                    Y->curdom[j] = 1;
                    Y->curdom[0] = CDcount(Y);
                }
                if(Y->curdom[0] == SIZE) flag = false;
            }
        }
        else if (Y->assigned) {
            int v = Y->val;
            if (re == 1) {
                for (int j = v;j>0;j--) if (!X->curdom[j]) {
                    X->curdom[j] = 1;
                    X->curdom[0] = CDcount(X);
                }
                if(X->curdom[0] == SIZE) flag = false;
            }
            else if (re == -1)  {
                for (int j = v;j<=SIZE;j++) if (!X->curdom[j]) {
                    X->curdom[j] = 1;
                    X->curdom[0] = CDcount(X);
                }
                if(X->curdom[0] == SIZE) flag = false;
            }            
        }
        // Both not assigned.
        else {
            if (re == 1) {
                for (int j = 1;j<=SIZE;j++) if (!X->curdom[j]) {
                    int t = 1;
                    while (Y->curdom[t++]) {
                        if(t == j) {
                            X->curdom[j] = 1;
                            X->curdom[0] = CDcount(X);
                        }
                    }
                    if(X->curdom[0] == SIZE) flag = false;
                }
                for (int j = 1;j<=SIZE;j++) if (!Y->curdom[j]) {
                    int t = j + 1;
                    while (X->curdom[t++]) {
                        if(t == SIZE + 1) {
                            Y->curdom[j] = 1;
                            Y->curdom[0] = CDcount(Y);
                        }
                    }
                    if(Y->curdom[0] == SIZE) flag = false;
                }
            }
            else if (re == -1)  {
                for (int j = 1;j<=SIZE;j++) if (!X->curdom[j]) {
                    int t = j + 1;
                    while (Y->curdom[t++]) {
                        if(t == SIZE + 1) {
                            X->curdom[j] = 1;
                            X->curdom[0] = CDcount(X);
                        }
                    }
                    if(X->curdom[0] == SIZE) flag = false;
                }
                for (int j = 1;j<=SIZE;j++) if (!Y->curdom[j]) {
                    int t = 1;
                    while (X->curdom[t++]) {
                        if(t == j) {
                            Y->curdom[j] = 1;
                            Y->curdom[0] = CDcount(Y);
                        }
                    }
                    if(Y->curdom[0] == SIZE) flag = false;
                }
            }
        }
    }
    return flag;
}

// Goal Checks if all blocks are assigned.
bool Goal(futoshiki* FTSK) {
    for (int i = 1;i<=SIZE;i++) {
        for (int j = 1;j<=SIZE;j++) if (!FTSK->board[i][j].assigned) {
            return false;
        }
    }
    return true;
}

Do* heuristicpick(futoshiki* FTSK) {
    // MRV
    Do* maxi = &FTSK->board[1][1];
    for (int i = 1;i<=SIZE;i++) {
        for (int j = 1;j<=SIZE;j++) {
            if(FTSK->board[i][j].assigned) continue;
            if(maxi->curdom[0] < FTSK->board[i][j].curdom[0] || maxi->assigned) {
                maxi = &FTSK->board[i][j];
                if (maxi->curdom[0] == SIZE-1) return maxi;
            }
        }
    }
    return maxi;
}

void Copyboard(futoshiki* dest, const futoshiki* src) {
    // Clear destination
    memset(dest->board, 0, sizeof(dest->board));
    dest->multirelation.clear();
    // Copy
    for (int i =1;i<=SIZE;i++) {
        for (int j =1;j<=SIZE;j++) {
            dest->board[i][j].val = src->board[i][j].val;
            dest->board[i][j].pos.row = src->board[i][j].pos.row;
            dest->board[i][j].pos.col = src->board[i][j].pos.col;
            memcpy(dest->board[i][j].curdom, src->board[i][j].curdom, sizeof(dest->board[i][j].curdom));
            dest->board[i][j].assigned = src->board[i][j].assigned;
            dest->board[i][j].relation = src->board[i][j].relation;
        }
    }
    dest->multirelation = src->multirelation;
}

string lrarrow(futoshiki* FTSK, Do* m);
string udarrow(futoshiki* FTSK, Do* m);

void display(futoshiki* FTSK) {
    for (int i = 1;i<=SIZE;i++) {
        cout << "\t";
        for (int j = 1;j<=SIZE;j++) {
            cout << " " << FTSK->board[i][j].val << lrarrow(FTSK, &FTSK->board[i][j]);
        }
        cout << endl << "\t";
        for (int j = 1;j<=SIZE;j++) if (i!=SIZE) {
            cout << udarrow(FTSK, &FTSK->board[i][j]);
        }
        cout << endl;
    }
    cout << endl;
}
string lrarrow(futoshiki* FTSK, Do* m) {
    if (!FTSK->board[m->pos.row][m->pos.col].relation.size()) return "  ";
    else for(size_t i = 0;i<FTSK->board[m->pos.row][m->pos.col].relation.size();i++) {
        int col = FTSK->board[m->pos.row][m->pos.col].relation[i].enemy.col;
        int r = FTSK->board[m->pos.row][m->pos.col].relation[i].r;
        if (col == m->pos.col+1) return (r == -1) ? " <" : " >";
    }
    return "  ";
}

string udarrow(futoshiki* FTSK, Do* m) {
    if (!FTSK->board[m->pos.row][m->pos.col].relation.size()) return "    ";
    else for(size_t i = 0;i<FTSK->board[m->pos.row][m->pos.col].relation.size();i++) {
        int row = FTSK->board[m->pos.row][m->pos.col].relation[i].enemy.row;
        int r = FTSK->board[m->pos.row][m->pos.col].relation[i].r;
        if (row == m->pos.row+1) return (r == -1) ? " ^  " : " v  ";
    }
    return "    ";
}