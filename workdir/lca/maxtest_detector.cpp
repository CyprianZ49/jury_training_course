#include <bits/stdc++.h>

#define pb push_back
#define st first
#define nd second

using namespace std;

const int maxN = 500009;

int root = 0;
vector <int> tree[maxN];

int depth[maxN];
int tree_size[maxN];

int path_end[maxN];
int path_id[maxN];
int path_count = 0;

void dfs(int v, int p) {
    depth[v] = depth[p] + 1;
    tree_size[v] = 1;

    for (int i = 0; i < (int)tree[v].size(); i++) {
        if (tree[v][i] != p) {
            dfs(tree[v][i], v);
            tree_size[v] += tree_size[tree[v][i]];
        }
    }
}

void dfs2(int v, int p, int id) {
    path_id[v] = id;

    for (int i = 0; i < (int)tree[v].size(); i++) {
        if (tree[v][i] != p) {
            if (tree_size[tree[v][i]] * 2 >= tree_size[v]) {
                dfs2(tree[v][i], v, id);
            }
            else {
                path_count += 1;
                path_end[path_count] = v;
                dfs2(tree[v][i], v, path_count);
            }
        }
    }
}

int lca(int v, int u) {
    while (path_id[v] != path_id[u]) {
        if (depth[path_end[path_id[v]]] > depth[path_end[path_id[u]]]) {
            v = path_end[path_id[v]];
        }
        else {
            u = path_end[path_id[u]];
        }
    }

    if (depth[v] > depth[u]) swap(v, u);
    return v;
}

int main() {
    int n, q;
    cin >> n >> q;

    if (n == 500000 && q == 500000) return 1;

    cin >> root;

    int a, b;
    for (int i = 1; i < n; i++) {
        cin >> a >> b;
        tree[a].pb(b);
        tree[b].pb(a);
    }

    depth[root] = -1;
    dfs(root, root);

    depth[0] = -1;
    path_end[0] = 0;
    dfs2(root, root, 0);

    for (int t = 0; t < q; t++) {
        cin >> a >> b;
        cout << lca(a, b) << '\n';
    }
}