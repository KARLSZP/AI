#include<iostream>
#include<algorithm>
#include<cstring>
using namespace std;

const int SIZE = 7;
static int nodes = 0; 


struct Do {
    int val; // value
    int row, col; // position
    int l, r, u, d; // [-1:<] | [0:\] | [1:>]
    bool curdom[SIZE]; // 1~SIZE's availablity
    bool assigned;
};

struct futoshiki {
    Do board[SIZE][SIZE];
    bool RowCheck(futoshiki* board, Do* m);
    bool ColCheck(futoshiki* board, Do* m);
    bool NeiCheck(futoshiki* board, Do* m);
    int CDcount(Do* m);
    bool Goal(futoshiki* board);
    bool FCCheck(futoshiki* board, int c, Do* m);
    void Copyboard(futoshiki* dest, const futoshiki* src);
    Do* heuristicpick(futoshiki* board);
    void propagete(futoshiki* board, Do* m);
};

bool FC(futoshiki* board, int level);
void propagate(futoshiki* board, Do* m);
void display(futoshiki* board);


int main() {
    futoshiki FTSK;
    futoshiki* ptr = &FTSK;
    for (int i = 0;i<SIZE;i++) {
        for (int j = 0;j<SIZE;j++) {
            FTSK.board[i][j].val = 0;
            FTSK.board[i][j].row = i;
            FTSK.board[i][j].col = j;
            FTSK.board[i][j].u = 0;
            FTSK.board[i][j].d = 0;
            FTSK.board[i][j].l = 0;
            FTSK.board[i][j].r = 0;
            FTSK.board[i][j].assigned = 0;
            memset(FTSK.board[i][j].curdom, 0, sizeof(FTSK.board[i][j].curdom));
        }
    }
    cout << "Input as a b < c d, mind to make sure a <= c and b <= d !!" << endl;
    while(1) {
        int a, b, d, e;
        char c;        
        cin >> a >> b >> c >> d >> e;
        if (a == d) {
            FTSK.board[a-1][b-1].r = (c == '>') ? 1 : -1;
            FTSK.board[d-1][e-1].l = (c == '>') ? -1 : 1;
        }
        else {
            FTSK.board[a-1][b-1].u = (c == '>') ? 1 : -1;
            FTSK.board[d-1][e-1].d = (c == '>') ? -1 : 1;
        }
        if (a+b+d+e == 0) break;
    }
    cout << "Input Presets: " << endl;
    while(1) {
        int a, b, v;
        cin >> a >> b >> v;
        if (a+b+v == 0) break;
        FTSK.board[a-1][b-1].val = v;
        FTSK.board[a-1][b-1].assigned = 1;
        propagate(ptr, &FTSK.board[a-1][b-1]);
    }
    display(ptr);
    FC(ptr, 0);
    cout<<nodes<<endl;
    return 0;
}

/* ###################################################################### */

bool RowCheck(futoshiki* board, Do* m) {
    // return false: constraint falsified;
    //         true: NO falsification.
    int Row[SIZE];
    for(int i = 0;i<SIZE;i++) {
        Row[i] = board->board[m->row][i].val;
    }
    // Check Constraints
    sort(Row, Row + SIZE);
    for(int i = 0;i<SIZE-1;i++) {
        if (!Row[i]) continue;
        if (Row[i] == Row[i+1]) return false;
    }
    return true;
}

bool ColCheck(futoshiki* board, Do* m) {
    // return false: constraint falsified;
    //         true: NO falsification.
    int Col[SIZE];
    for(int i = 0;i<SIZE;i++) {
        Col[i] = board->board[i][m->col].val;
    }
    // Check Constraints
    sort(Col, Col + SIZE);
    for(int i = 0;i<SIZE-1;i++) {
        if (!Col[i]) continue;
        if (Col[i] == Col[i+1]) return false;
    }
    return true;
}

bool NeiCheck(futoshiki* board, Do* m) {
    int v = m->val;
    // Check Constraints
    // UP
    if (m->u && board->board[m->row - 1][m->col].assigned) {
        if (m->u == -1 && v > board->board[m->row - 1][m->col].val) return false; 
        else if (m->u == 1 && v < board->board[m->row - 1][m->col].val) return false;
    }
    // DOWN
    if (m->d && board->board[m->row + 1][m->col].assigned) {
        if (m->d == -1 && v > board->board[m->row + 1][m->col].val) return false; 
        else if (m->d == 1 && v < board->board[m->row + 1][m->col].val) return false;
    }
    // LEFT
    if (m->l && board->board[m->row - 1][m->col].assigned) {
        if (m->l == -1 && v > board->board[m->row][m->col - 1].val) return false; 
        else if (m->l == 1 && v < board->board[m->row][m->col - 1].val) return false;
    }
    // RIGHT
    if (m->r && board->board[m->row - 1][m->col].assigned) {
        if (m->r == -1 && v > board->board[m->row][m->col + 1].val) return false; 
        else if (m->r == 1 && v < board->board[m->row][m->col + 1].val) return false;
    }
    return true;
}

int CDcount(Do* m) {
    int res = 0;
    for (int i = 0;i<SIZE;i++) {
        res += m->curdom[i];
    }
    return res;
}

bool CheckCons(futoshiki* board, int c, Do* m) {
    int R = m->row, C = m->col, tot = 0;
    // c == 0 >>> row
    if (c == 0) {
        for (int i = 0;i<SIZE;i++) {
            tot += board->board[R][i].assigned;
        }
        return (tot == SIZE-1);
    }
    // c == 1 >>> col
    else if (c == 1) {
        for (int i = 0;i<SIZE;i++) {
            tot += board->board[i][C].assigned;
        }
        return (tot == SIZE-1);
    }
    // c == 2 >>> neighbour
    else if (c == 2) {
        tot += (R == 0)        ? 1 : board->board[R - 1][C].assigned;
        tot += (R == SIZE - 1) ? 1 : board->board[R + 1][C].assigned;
        tot += (C == 0)        ? 1 : board->board[R][C - 1].assigned;
        tot += (C == SIZE - 1) ? 1 : board->board[R][C + 1].assigned;
        return (tot == SIZE-1);
    }
    return false;
}

bool FCCheck(futoshiki* board, int c, Do* m) {
    // c == 0 >>> row
    if (c == 0) for (int i = 0;i<SIZE;i++) {
        if (!m->curdom[i]) {
            m->curdom[i] = 1;
            if(RowCheck(board, m)) m->curdom[i] = 0; // No falsification
        }
    }
    // c == 1 >>> col
    else if (c == 1) for (int i = 0;i<SIZE;i++) {
        if (!m->curdom[i]) {
            m->curdom[i] = 1;
            if(ColCheck(board, m)) m->curdom[i] = 0; // No falsification
        }
    }
    // c == 2 >>> neighbour
    else if (c == 2) for (int i = 0;i<SIZE;i++) {
        if (!m->curdom[i]) {
            m->curdom[i] = 1;
            if(NeiCheck(board, m)) m->curdom[i] = 0; // No falsification
        }
    }
    if (CDcount(m) == SIZE) return false;
    else return true;
}

bool Goal(futoshiki* board) {
    for (int i = 0;i<SIZE;i++) {
        for (int j = 0;j<SIZE;j++) {
            if (!board->board[i][j].assigned) return false;
        }
    }
    return true;
}

Do* heuristicpick(futoshiki* board) {
    // MRV
    Do* maxi = &board->board[0][0];
    for (int i = 0;i<SIZE;i++) {
        for (int j = 0;j<SIZE;j++) {
            if(board->board[i][j].assigned) continue;
            if(CDcount(maxi) < CDcount(&board->board[i][j]) || maxi->assigned) {
                maxi = &board->board[i][j];
                if (CDcount(maxi) == SIZE-1) return maxi;
            }
        }
    }
    return maxi;
}

void propagate(futoshiki* board, Do* m) {
	// cout<<"P: "<<m->val<<endl; 
    for (int i = 0;i<SIZE;i++) {
        board->board[m->row][i].curdom[m->val-1] = 1;
        board->board[i][m->col].curdom[m->val-1] = 1;
    }
    if (m->r == -1) {
        for (int i = 0;i<m->val - 1;i++) {
            board->board[m->row][m->col + 1].curdom[i] = 1;
        }
    }
    else if (m->r == 1) {
        for (int i = m->val;i<SIZE;i++) {
            board->board[m->row][m->col + 1].curdom[i] = 1;
        }
    }
    if (m->u == -1) {
        for (int i = 0;i<m->val - 1;i++) {
            board->board[m->row - 1][m->col].curdom[i] = 1;
        }
    }
    else if (m->u == 1) {
        for (int i = m->val;i<SIZE;i++) {
            board->board[m->row - 1][m->col].curdom[i] = 1;
        }
    }
    if (m->l == -1) {
        for (int i = 0;i<m->val - 1;i++) {
            board->board[m->row][m->col - 1].curdom[i] = 1;
        }
    }
    else if (m->l == 1) {
        for (int i = m->val;i<SIZE;i++) {
            board->board[m->row][m->col - 1].curdom[i] = 1;
        }
    }
    if (m->d == -1) {
        for (int i = 0;i<m->val - 1;i++) {
            board->board[m->row + 1][m->col].curdom[i] = 1;
        }
    }
    else if (m->d == 1) {
        for (int i = m->val;i<SIZE;i++) {
            board->board[m->row + 1][m->col].curdom[i] = 1;
        }
    }
}

void Copyboard(futoshiki* dest, const futoshiki* src) {
	memcpy(dest, src, sizeof(futoshiki));
}

bool FC(futoshiki* board, int level) {
	nodes++;
    if (Goal(board)) {
        // Return when all cells are assigned.
        cout << "Goal!" << endl;
        display(board);
        return true;
    }
    Do* v = heuristicpick(board); // Pick with MRV
    v->assigned = true;
    bool dwo = false;
    int pos = 0;
    for (int i = 0;i<SIZE;i++) if (!v->curdom[i]) {
        futoshiki boardcopy;
        Copyboard(&boardcopy, board);
        v->val = i+1;
        propagate(board, v);
        dwo = false;
        // row constraint
        if (!dwo && CheckCons(board, 0, v)) {
            for (int i = 0;i<SIZE;i++) if (!board->board[v->row][i].assigned) {
                dwo = !FCCheck(board, 0, &board->board[v->row][i]);
            }
        }
        // col constraint
        if (!dwo && CheckCons(board, 1, v)) {
            for (int i = 0;i<SIZE;i++) if (!board->board[i][v->col].assigned) {
                dwo = !FCCheck(board, 1, &board->board[i][v->col]);
            }
        }
        // neighbour constraint
        if (!dwo && CheckCons(board, 2, v)) {
            if (v->row && board->board[v->row - 1][v->col].assigned) {
                dwo = !FCCheck(board, 2, &board->board[v->row - 1][v->col]);
            }
            else if (v->row!=SIZE-1 && board->board[v->row + 1][v->col].assigned) {
                dwo = !FCCheck(board, 2, &board->board[v->row + 1][v->col]);
            }
            else if (v->col && board->board[v->row][v->col - 1].assigned) {
                dwo = !FCCheck(board, 2, &board->board[v->row][v->col - 1]);
            }
            else if (v->col!=SIZE-1 && board->board[v->row][v->col + 1].assigned) {
                dwo = !FCCheck(board, 2, &board->board[v->row][v->col + 1]);
            }
        }
        if(!dwo && FC(board, level + 1)) return true;
        Copyboard(board, &boardcopy);
    }
    v->assigned = false;
    return false;
}

void display(futoshiki* board) {
    for (int i = 0;i<SIZE;i++) {
        cout << "\t";
        for (int j = 0;j<SIZE;j++) {
            if (board->board[i][j].r == 1) cout << " " << board->board[i][j].val << " >";
            else if (board->board[i][j].r == -1) cout << " " << board->board[i][j].val << " <";
            else cout << " " << board->board[i][j].val << "  ";
        }
        cout << endl << "\t";
        if (i!=SIZE-1) {
            for (int j = 0;j<SIZE;j++) {
                if (board->board[i+1][j].u == 1) {
                    cout << " ^  ";
                }
                else if (board->board[i+1][j].u == -1) {
                    cout << " v  ";
                }
                else cout << "    ";
            }
        }
        cout << endl;
    }
}