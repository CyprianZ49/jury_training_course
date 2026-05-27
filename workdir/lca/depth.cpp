#include <bits/stdc++.h>

#define pb push_back

using namespace std;

const int maxN = 200009;

int root = 0;
vector <int> tree[maxN];

int depth[maxN];
int parent[maxN];

void dfs(int v, int p) {
    parent[v] = p;
    depth[v] = depth[p] + 1;

    for (int i = 0; i < (int)tree[v].size(); i++) {
        if (tree[v][i] != p) {
            dfs(tree[v][i], v);
        }
    }
}

int lca(int v, int u) {
    if (v == u) {
        return v;
    }
    if (depth[v] < depth[u]) swap(v, u);
    return lca(parent[v], u);
}

int main() {
    int n, q;
    cin >> n >> q;
    // cin >> root;
    root = 1;

    int a, b;
    for (int i = 1; i < n; i++) {
        // cin >> a >> b;
        // tree[a].pb(b);
        // tree[b].pb(a);
        cin >> a;
        tree[a].pb(i+1);
        tree[i+1].pb(a);
    }

    depth[root] = -1;
    dfs(root, root);

    for (int t = 0; t < q; t++) {
        cin >> a >> b;
        cout << lca(a, b) << '\n';
    }
}