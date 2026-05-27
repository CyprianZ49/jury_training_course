#include <bits/stdc++.h>

#define pb push_back
#define st first
#define nd second

using namespace std;

const int maxN = 200009;
const int lp = 262144 * 2;
const int inf = maxN + 1;

int root = 0;
vector <int> tree[maxN];

pair <int, int> segment_tree[lp * 2];

int depth[maxN];
int st_index[maxN];
int free_index = 1;

void insert (int i, pair <int, int> v) {
    i += lp;
    segment_tree[i] = v;

    i /= 2;
    while (i > 0) {
        segment_tree[i] = min(segment_tree[i * 2], segment_tree[i * 2 + 1]);
        i /= 2;
    }
}

pair <int, int> query(int x, int y) {
    x += lp - 1;
    y += lp + 1;

    pair <int, int> ans = {inf, 0};
    
    while (x / 2 != y / 2) {
        if (x % 2 == 0) {
            ans = min(ans, segment_tree[x + 1]);
        }
        if (y % 2 == 1) {
            ans = min(ans, segment_tree[y - 1]);
        }

        x /= 2;
        y /= 2;
    }

    return ans;
}

void dfs(int v, int p) {
    depth[v] = depth[p] + 1;

    st_index[v] = free_index;
    insert(free_index++, {depth[v], v});

    for (int i = 0; i < (int)tree[v].size(); i++) {
        if (tree[v][i] != p) {
            dfs(tree[v][i], v);
            insert(free_index++, {depth[v], v});
        }
    }
}

int lca(int v, int u) {
    int x = min(st_index[v], st_index[u]);
    int y = max(st_index[v], st_index[u]);
    return query(x, y).nd;
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

    for (int i = lp * 2 - 1; i > 0; i--) {
        segment_tree[i] = {inf, 0};
    }

    depth[root] = -1;
    dfs(root, root);

    for (int t = 0; t < q; t++) {
        cin >> a >> b;
        cout << lca(a, b) << '\n';
    }
}