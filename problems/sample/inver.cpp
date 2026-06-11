#include "bits/stdc++.h"
#include "oi.h"

#define pb push_back

using namespace std;
using namespace oi;

Scanner input(stdin, oi::EN);

int main(int argc, char* argv[]) {
    int subtask = atoi(argv[1]);

    ll max_x = 1;
    
    if (subtask == 1) {
        max_x = 1000000000;
    }
    else if (subtask == 2) {
        max_x = 1000000000000000000;
    }

    input.readULL(0, max_x);
    input.readSpace();
    input.readULL(0, max_x);
    input.readEoln();
    input.readEof();

    return 0;
}