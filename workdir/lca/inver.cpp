#include "bits/stdc++.h"
#include "oi.h"

#define pb push_back

using namespace std;
using namespace oi;

Scanner input(stdin, oi::EN);

int subtask_limits_n[4] = {2000, 2000, 200000, 200000};
int subtask_limits_q[4] = {2000, 200000, 2000, 200000};

vector <vector <int> > tree;

int visited = 0;

void DFS(int v, int p) {
    visited += 1;

    for (int i = 0; i < (int)tree[v].size(); i++) {
        if (tree[v][i] != p) {
            DFS(tree[v][i], v);
        }
    }
}

int main(int argc, char* argv[]) {
    int subtask = atoi(argv[1]);

    int n_limit = subtask_limits_n[subtask - 1];
    int q_limit = subtask_limits_q[subtask - 1];

    int n = input.readInt(1, n_limit);
    input.readSpace();
    int q = input.readInt(1, q_limit);
    input.readEoln();
    input.readInt(1, n);
    input.readEoln();

    tree.resize(n + 1);
    for (int i = 1; i < n; i++) {
        int a = input.readInt(1, n);
        input.readSpace();
        int b = input.readInt(1, n);
        input.readEoln();
        tree[a].pb(b);
        tree[b].pb(a);
    }

    for (int i = 0; i < q; i++) {
        input.readInt(1, n);
        input.readSpace();
        input.readInt(1, n);
        input.readEoln();
    }

    DFS(1, 1);

    if (visited != n) {
        cout << "The input graph is not a tree.\n";
        return 1;
    }

    return 0;
}