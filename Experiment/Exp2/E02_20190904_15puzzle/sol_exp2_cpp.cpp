#include <iostream> 
#include <cstdlib>
using namespace std;


int ** load(const int size) {
    int Map[size][size] = {
        {7, 5, 2, 4}, 
        {9, 0, 1, 8},
        {6, 10, 3, 12},
        {13, 14, 11, 15}
    }
    return Map;
}


int main() {
    const int size = 4;
    int (*ptr)[size] = load(size);
    return 0;
}