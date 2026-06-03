#include "bits/stdc++.h"
#include "oi.h"

#define pb push_back
#define st first
#define nd second

using namespace std;
using namespace oi;

Random rng;

int subtask_limits_n[4] = {10000, 10000, 200000, 200000};
int subtask_limits_q[4] = {10000, 200000, 10000, 200000};

vector <vector <int> > tree;
vector <pair <int, int> > edges;
vector <int> depth;
int maxDepth = 0;
vector <pair <int, int> > queries;
vector <vector <int> > sorted_by_depth;
vector <int> parent;
vector <pair <int, int> > deep_desc;

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

    int path_length = n / 7;
    int path_count = 6;

    int leftover = n - path_length * path_count;

    if (path_length > 0) {
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
    }

    for (int i = 0; i < leftover; i++) {
        int current = n - i;
        int parent = (rng.randUInt() % (current - 1)) + 1;
        tree[parent].pb(current);
        tree[current].pb(parent);
        edges.pb({current, parent});
    }
}

void generate_biased_tree(int n) {
    tree.resize(n + 1);

    for (int i = 2; i <= n; i++) {
        int bias = rng.randUInt() % 100;
        // bias = 1;

        if (bias < 2) {
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

int DFS(int v, int p) {
    depth[v] = depth[p] + 1;
    parent[v] = p;
    maxDepth = max(maxDepth, depth[v]);
    deep_desc[v] = {v, 1};

    for (int i = 0; i < (int)tree[v].size(); i++) {
        if (tree[v][i] != p) {
            int ret = DFS(tree[v][i], v);

            if (depth[deep_desc[v].st] < depth[ret]) {
                deep_desc[v].nd = deep_desc[v].st;
                deep_desc[v].st = ret;
            }
            else if (depth[deep_desc[v].nd] < depth[ret]) {
                deep_desc[v].nd = ret;
            }
        }
    }

    return deep_desc[v].st;
}

void generate_random_queries(int n, int q) {
    for (int i = 0; i < q; i++) {
        int a = (rng.randUInt() % n) + 1;
        int b = (rng.randUInt() % n) + 1;
        queries.pb({a, b});
    }
}

void generate_depth_gap_queries(int n, int q) {
    sorted_by_depth.resize(maxDepth + 1);

    for (int i = 1; i <= n; i++) {
        sorted_by_depth[depth[i]].pb(i);
    }

    int sqr_q = 1;
    while (sqr_q * sqr_q < q) sqr_q += 1;
    sqr_q -= 1;

    vector <int> deep;
    vector <int> shallow;

    for (int i = 0; i <= maxDepth; i++) {
        for (int j = 0; j < (int)sorted_by_depth[i].size(); j++) {
            shallow.pb(sorted_by_depth[i][j]);
        }
    }

    for (int i = maxDepth; i >= 0; i--) {
        for (int j = 0; j < (int)sorted_by_depth[i].size(); j++) {
            deep.pb(sorted_by_depth[i][j]);
        }
    }

    while (sqr_q * sqr_q > q) sqr_q -= 1;

    for (int i = 0; i < sqr_q; i++) {
        for (int j = 0; j < sqr_q; j++) {
            queries.pb({shallow[i], deep[j]});
        }
    }

    generate_random_queries(n, q - sqr_q * sqr_q);
}

void generate_by_ans_queries(int n, int q) {
    for (int i = 1; i <= n && q; i++) {
        queries.pb(deep_desc[i]);
        q--;
    }
}

void generate_bamboo(int n, int q) {
    cout << n << " " << q << "\n";
    cout << 1 << "\n";

    for (int i = 2; i < n; i++) {
        cout << i - 1 << " " << i << "\n";
    }
    cout << 1 << " " << n << "\n";
    
    for (int i = 0; i < q; i++) {
        int a = n - 1;
        int b = n;
        if (i % 2 == 0) swap(a, b);
        cout << a << " " << b << "\n";
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
    else if (test_id < 13) {
        generate_long_paths_tree(n);
    }
    else if (test_id == 13) {
        generate_bamboo(n, q);
        return 0;
    }
    else {
        generate_biased_tree(n);
    }

    depth.resize(n + 1);
    parent.resize(n + 1);
    deep_desc.resize(n + 1);
    depth[1] = -1;
    (void)DFS(1, 1);

    int q1 = min(n / 4, q / 3);
    generate_by_ans_queries(n, q1);
    generate_by_ans_queries(n, q1);
    int q2 = q - 2 * q1;
    generate_depth_gap_queries(n, q2);

    rng.randomShuffle(edges.begin(), edges.end());
    rng.randomShuffle(queries.begin(), queries.end());
    int shift = rng.randUInt() % n;
    // shift = -1;

    cout << n << " " << q << "\n";
    cout << ((1 + shift) % n) + 1 << "\n";

    for (int i = 0; i < (int)edges.size(); i++) {
        cout << ((edges[i].st + shift) % n) + 1 << " ";
        cout << ((edges[i].nd + shift) % n) + 1 << "\n";
    }

    for (int i = 0; i < q; i++) {
        cout << ((queries[i].st + shift) % n) + 1 << " ";
        cout << ((queries[i].nd + shift) % n) + 1 << "\n";
    }
}