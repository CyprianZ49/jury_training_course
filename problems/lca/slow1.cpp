#include <bits/stdc++.h>

using namespace std;

const int maxN = 100009;
const int log2maxN = 18;

int parent[maxN];
int depth[maxN];
vector <int> children[maxN];
int root = 0;

void DFS(int v) {
    depth[v] = depth[parent[v]] + 1;

    for (int i = 0; i < (int)children[v].size(); i++) {
        DFS(children[v][i]);
    }

    return;
}

int lca(int x, int y) {
    while (depth[x] > depth[y]) {
        x = parent[x];
    }

    while (depth[y] > depth[x]) {
        y = parent[y];
    }

    while (x != y) {
        x = parent[x];
        y = parent[y];
    }

    return x;
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
    DFS(root);

    int q;
    cin >> q;
    int x, y;
    for (int i = 0; i < q; i++) {
        cin >> x >> y;
        cout << lca(x, y) << '\n';
    }
}