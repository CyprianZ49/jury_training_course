#include <bits/stdc++.h>

using namespace std;

const int maxN = 100009;
const int log2maxN = 18;

int parent[maxN];
bool marked[maxN];
int root = 0;

void clean_marks() {
    for (int i = 0; i < maxN; i++) {
        marked[i] = false;
    }
}

int lca(int x, int y) {
    // clean_marks();

    while (x != root) {
        marked[x] = true;
        x = parent[x];
    }
    marked[x] = true;

    while (!marked[y]) {
        y = parent[y];
    }

    return y;
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
        }
    }

    int q;
    cin >> q;
    int x, y;
    for (int i = 0; i < q; i++) {
        cin >> x >> y;
        cout << lca(x, y) << '\n';
    }
}