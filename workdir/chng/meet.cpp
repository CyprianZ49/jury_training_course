#include <bits/stdc++.h>

using namespace std;

#define pb push_back
#define st first
#define nd second

typedef long long ll;

const int maxV = 20009;
const int maxN = 5009;

const int inf = maxV + 10;

vector <int> coins;

pair<int, bitset<maxN>> best[2][maxV];
bitset <maxN> current;

void backtrack(int i, int sum, int count, int h, int max_i, int V) {
    if (sum > V) return;

    if (count < best[h][sum].st) {
        best[h][sum].st = count;
        best[h][sum].nd = current;
    }

    if (i >= max_i) return;

    backtrack(i + 1, sum, count, h, max_i, V);
    current[i] = 1;
    backtrack(i + 1, sum + coins[i], count + 1, h, max_i, V);
    current[i] = 0;
}

int main() {
    int n, V;
    cin >> n >> V;

    int c;
    for (int i = 0; i < n; i++) {
        cin >> c;
        coins.pb(c);
    }

    for (int h = 0; h <= 1; h++) {
        for (int i = 0; i < maxN; i++) {
            best[h][i].st = inf;
        }
        best[h][0].st = 0;
    }

    int m = n / 2;
    backtrack(0, 0, 0, 0, m, V);
    backtrack(m, 0, 0, 1, n, V);

    int best_val = inf;
    int best_k = 0;
    for (int k = 0; k <= V; k++) {
        if (best[0][k].st + best[1][V - k].st < best_val) {
            best_val = best[0][k].st + best[1][V - k].st;
            best_k = k;
        }
    }

    if (best_val == inf) {
        cout << "-1\n";
        return 0;
    }

    cout << best_val << "\n";

    current |= best[0][best_k].nd;
    current |= best[1][V - best_k].nd;
    for (int i = 0; i < n; i++) {
        if (current[i] == 1) {
            cout << coins[i] << " ";
        }
    }

    cout << "\n";
}