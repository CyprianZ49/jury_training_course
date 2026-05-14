#include <bits/stdc++.h>

using namespace std;

const int maxN = 100009;
const int log2maxN = 18;

int parent[maxN];
int jump[maxN];
int depth[maxN];
vector <int> children[maxN];
int order_pre[maxN];
int order_post[maxN];
int root = 0;
int order = 0;

void DFS(int v) {
    depth[v] = depth[parent[v]] + 1;

    order_pre[v] = order++;

    int p = parent[v];
    if (depth[jump[jump[p]]] - depth[jump[p]] == depth[jump[p]] - depth[p]) {
        jump[v] = jump[jump[p]];
    }
    else {
        jump[v]  = p;
    }

    for (int i = 0; i < (int)children[v].size(); i++) {
        DFS(children[v][i]);
    }

    order_post[v] = order++;
    return;
}

bool is_anc(int x, int y) {
    return order_pre[x] <= order_pre[y] && order_post[x] >= order_post[y];
}

int lca(int x, int y) {
    if (is_anc(x, y)) {
        return x;
    }

    while (!is_anc(parent[x], y)) {
        if (!is_anc(jump[x], y)) {
            x = jump[x];
        }
        else {
            x = parent[x];
        }
    }

    return parent[x];
}

int main() {
    int n;
    cin >> n;

    int a;
    for (int i = 1; i <= n; i++) {
        cin >> a;
        if (a == 0) {
            root = i;
            parent[i] = i;
        }
        else {
            parent[i] = a;
            children[a].push_back(i);
        }
    }

    depth[root] = -1;
    jump[root] = root;
    DFS(root);

    int q;
    cin >> q;
    int x, y;
    for (int i = 0; i < q; i++) {
        cin >> x >> y;
        cout << lca(x, y) << '\n';
    }
}