#include <bits/stdc++.h>

#define pb push_back

using namespace std;

const int maxN = 200009;
const int log2maxN = 18;

int root = 0;
vector <int> tree[maxN];

int order_pre[maxN];
int order_post[maxN];
int order = 0;

int anc[maxN][log2maxN];

void dfs(int v, int p) {
    anc[v][0] = p;

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
    for (int i = log2maxN - 1; i >= 0; i--) {
        if (!is_anc(anc[v][i], u)) {
            v = anc[v][i];
        }
    }

    return anc[v][0];
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

    for (int i = 1; i < log2maxN; i++) {
        for (int v = 1; v <= n; v++) {
            anc[v][i] = anc[anc[v][i - 1]][i - 1];
        }
    }

    for (int t = 0; t < q; t++) {
        cin >> a >> b;
        cout << lca(a, b) << '\n';
    }
}