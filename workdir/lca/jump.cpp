#include <bits/stdc++.h>

#define pb push_back

using namespace std;

const int maxN = 200009;
const int log2maxN = 18;

int root = 0;
vector <int> tree[maxN];

int depth[maxN];

int order_pre[maxN];
int order_post[maxN];
int order = 0;

int jump[maxN];
int parent[maxN];

void dfs(int v, int p) {
    parent[v] = p;
    depth[v] = depth[p] + 1;

    if (depth[jump[jump[p]]] - depth[jump[p]] == depth[jump[p]] - depth[p]) {
        jump[v] = jump[jump[p]];
    }
    else {
        jump[v]  = p;
    }

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
        if (!is_anc(jump[v], u)) {
            v = jump[v];
        }
        else {
            v = parent[v];
        }
    }

    return parent[v];
}

int main() {
    int n, q;
    cin >> n >> q;
    cin >> root;

    int a, b;
    for (int i = 1; i < n; i++) {
        cin >> a >> b;
        tree[a].pb(b);
        tree[b].pb(a);
    }

    depth[root] = -1;
    jump[root] = root;
    dfs(root, root);

    for (int t = 0; t < q; t++) {
        cin >> a >> b;
        cout << lca(a, b) << '\n';
    }
}