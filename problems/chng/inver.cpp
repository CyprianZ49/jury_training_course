#include "oi.h"
#include <bits/stdc++.h>

using namespace std;
using namespace oi;

Scanner input(stdin, oi::EN);

#define pb push_back
#define st first
#define nd second

typedef long long ll;

int subtask_limits_n[3] = {24, 48, 5000};
int max_V = 20000;

int main(int argc, char *argv[]) {
    int subtask = atoi(argv[1]);

    int n_limit = subtask_limits_n[subtask - 1];
    
    int n = input.readInt(1, n_limit);
    input.readSpace();
    input.readInt(1, max_V);
    input.readEoln();

    for (int i = 0; i < n; i++) {
        input.readInt(1, max_V);
        if (i != n - 1) {
            input.readSpace();
        }
    }

    input.readEoln();
    input.readEof();

    return 0;
}