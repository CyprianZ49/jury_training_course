#include <bits/stdc++.h>

#define pb push_back

using namespace std;

const int maxN = 200009;

int root = 0;
vector <int> tree[maxN];

bool marked[maxN];
int parent[maxN];

void dfs(int v, int p) {
    parent[v] = p;

    for (int i = 0; i < (int)tree[v].size(); i++) {
        if (tree[v][i] != p) {
            dfs(tree[v][i], v);
        }
    }
}

int lca(int v, int u) {
    while (v != root) {
        marked[v] = true;
        v = parent[v];
    }
    marked[v] = true;

    while (!marked[u]) {
        u = parent[u];
    }

    return u;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);

    int n, q;
    cin >> n >> q;
    cin >> root;

    int a, b;
    for (int i = 1; i < n; i++) {
        cin >> a >> b;
        tree[a].pb(b);
        tree[b].pb(a);
    }

    dfs(root, root);

    for (int t = 0; t < q; t++) {
        cin >> a >> b;
        cout << lca(a, b) << '\n';
    }
}