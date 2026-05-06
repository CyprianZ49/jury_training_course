#include <bits/stdc++.h>

using namespace std;

const int maxN = 100009;
const int log2maxN = 18;

int ancestor[maxN][log2maxN];
vector <int> children[maxN];
int order_pre[maxN];
int order_post[maxN];
int root = 0;
int order = 0;

void DFS(int v) {
    order_pre[v] = order++;

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
    // if (is_anc(x, y)) {
    //     return x;
    // }

    for (int p2 = log2maxN - 1; p2 >= 0; p2--) {
        if (!is_anc(ancestor[x][p2], y)) {
            x = ancestor[x][p2];
        }
    }

    return ancestor[x][0];
}

int main() {
    int n;
    cin >> n;

    int a;
    for (int i = 1; i <= n; i++) {
        cin >> a;
        if (a == 0) {
            root = i;
            ancestor[i][0] = i;
        }
        else {
            ancestor[i][0] = a;
            children[a].push_back(i);
        }
    }

    for (int p2 = 1; p2 < log2maxN; p2++) {
        for (int i = 1; i <= n; i++) {
            ancestor[i][p2] = ancestor[ancestor[i][p2 - 1]][p2 - 1];
        }
    }

    DFS(root);

    int q;
    cin >> q;
    int x, y;
    for (int i = 0; i < q; i++) {
        cin >> x >> y;
        cout << lca(x, y) << '\n';
    }
}