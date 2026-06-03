#include <bits/stdc++.h>

#define pb push_back

using namespace std;

const int maxN = 500009;

int root = 0;
vector <int> tree[maxN];

int depth[maxN];

int order_pre[maxN];
int order_post[maxN];
int order = 0;

int sqrt_jump[maxN];
int parent[maxN];

void dfs(int v, int p) {
    parent[v] = p;
    depth[v] = depth[p] + 1;

    order_pre[v] = order++;

    for (int i = 0; i < (int)tree[v].size(); i++) {
        if (tree[v][i] != p) {
            dfs(tree[v][i], v);
        }
    }

    order_post[v] = order++;
}

bool is_anc(int v, int u) {
    return (order_pre[v] <= order_pre[u] && order_post[v] >= order_post[u]);
}

int lca(int v, int u) {
    if (is_anc(v, u)) {
        return v;
    }

    while (!is_anc(parent[v], u)) {
        if (!is_anc(sqrt_jump[v], u)) {
            v = sqrt_jump[v];
        }
        else {
            v = parent[v];
        }
    }

    return parent[v];
}

int main() {
    // ios_base::sync_with_stdio(false);
    // cin.tie(NULL);
    // cout.tie(NULL);

    int n, q;
    cin >> n >> q;
    cin >> root;
    // root = 1;

    int a, b;
    for (int i = 1; i < n; i++) {
        cin >> a >> b;
        tree[a].pb(b);
        tree[b].pb(a);
        // cin >> a;
        // tree[i + 1].pb(a);
        // tree[a].pb(i + 1);
    }

    depth[root] = -1;
    dfs(root, root);

    int sqrt_n = 1;
    while (sqrt_n * sqrt_n < n) sqrt_n++;

    for (int i = 1; i <= n; i++) {
        int v = i;
        for (int c = 0; c < sqrt_n; c++) {
            v = parent[v];
        }
        sqrt_jump[i] = v;
    }

    for (int t = 0; t < q; t++) {
        cin >> a >> b;
        cout << lca(a, b) << '\n';
    }
}