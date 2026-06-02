#include "bits/stdc++.h"
#include "oi.h"

#define pb push_back
#define st first
#define nd second

using namespace std;
using namespace oi;

Random rng;

int subtask_limits_n[4] = {2000, 2000, 200000, 200000};
int subtask_limits_q[4] = {2000, 200000, 2000, 200000};

vector <vector <int> > tree;
vector <pair <int, int> > edges;

void generate_random_tree(int n) {
    tree.resize(n + 1);

    for (int i = 2; i <= n; i++) {
        int parent = (rng.randUInt() % (i - 1)) + 1;
        tree[parent].pb(i);
        tree[i].pb(parent);
        edges.pb({i, parent});
    }
}

void generate_long_paths_tree(int n) {
    tree.resize(n + 1);

    int path_length = n / 10;
    int path_count = 8;

    int leftover = n - path_length * path_count;

    for (int i = 0; i < path_count; i++) {
        int path_head = i * path_length + 1;

        if (i == 1) {
            int parent = 1;
            tree[parent].pb(path_head);
            tree[path_head].pb(parent);
            edges.pb({path_head, parent});
        }
        else if (i == 2) {
            int parent = 2;
            tree[parent].pb(path_head);
            tree[path_head].pb(parent);
            edges.pb({path_head, parent});
        }
        else if (i > 2) {
            int parent = (rng.randUInt() % (path_head - 1)) + 1;
            tree[parent].pb(path_head);
            tree[path_head].pb(parent);
            edges.pb({path_head, parent});
        }

        for (int j = 1; j < path_length; j++) {
            int parent = path_head + j - 1;
            int current = path_head + j;
            tree[parent].pb(current);
            tree[current].pb(parent);
            edges.pb({current, parent});
        }
    }

    for (int i = 0; i < leftover; i++) {
        int current = n - i;
        int parent = (rng.randUInt() % (n - leftover)) + 1;
        tree[parent].pb(current);
        tree[current].pb(parent);
        edges.pb({current, parent});
    }
}

void generate_biased_tree(int n) {
    tree.resize(n + 1);

    for (int i = 2; i <= n; i++) {
        int bias = rng.randUInt() % 10;
        bias = 1;

        if (bias == 0) {
            int parent = (rng.randUInt() % (i - 1)) + 1;
            tree[parent].pb(i);
            tree[i].pb(parent);
            edges.pb({i, parent});
        }
        else {
            tree[i - 1].pb(i);
            tree[i].pb(i - 1);
            edges.pb({i, i - 1});
        }
    }
}

int main(int argc, char* argv[]) {
    int subtask = atoi(argv[1]);
    int test_id = atoi(argv[2]);

    int seed = 23 + test_id;
    rng.setSeed(seed);

    int n = subtask_limits_n[subtask - 1];
    int q = subtask_limits_q[subtask - 1];
    
    if (test_id < 5) {
        generate_random_tree(n);
    }
    else if (test_id < 12) {
        generate_long_paths_tree(n);
    }
    else {
        generate_biased_tree(n);
    }

    // rng.randomShuffle(edges.begin(), edges.end());
    int shift = rng.randUInt() % n;
    shift = -1;

    cout << n << " " << q << "\n";
    cout << ((1 + shift) % n) + 1 << "\n";

    for (int i = 0; i < (int)edges.size(); i++) {
        cout << ((edges[i].st + shift) % n) + 1 << " ";
        cout << ((edges[i].nd + shift) % n) + 1 << "\n";
    }

    for (int i = 0; i < q; i++) {
        cout << ((1 + shift) % n) + 1 << " ";
        cout << ((n + shift) % n) + 1 << "\n";

        // int x = (rng.randUInt() % n) + 1;
        // int y = (rng.randUInt() % n) + 1;
        // if (i + 5 >= q) {
        //     cout << x << " " << x << "\n";
        // }
        // else {
        //     cout << x << " " << y << "\n";
        // }
    }
}