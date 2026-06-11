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
int dp[2][maxV];

vector <int> ans;

void compute_dp(int x, int y, int V, int h) {
    for (int i = 0; i <= V; i++) dp[h][i] = inf;
    dp[h][0] = 0;

    for (int i = x; i <= y; i++) {
        int c = coins[i];
        for (int val = V; val >= c; val--) {
            if (dp[h][val - c] + 1 < dp[h][val]) {
                dp[h][val] = dp[h][val - c] + 1;
            }
        }
    }
}

void solve(int x, int y, int V) {
    if (V == 0) return;

    if (x == y) {
        if (coins[x] == V) {
            ans.pb(coins[x]);
        }
        return;
    }

    int m = (x + y) / 2;
    compute_dp(x, m, V, 0);
    compute_dp(m + 1, y, V, 1);

    int best_val = inf;
    int best_k = -1;
    for (int k = 0; k <= V; k++) {
        if (dp[0][k] + dp[1][V - k] < best_val) {
            best_val = dp[0][k] + dp[1][V - k];
            best_k = k;
        }
    }

    if (best_val == inf) return;

    solve(x, m, best_k);
    solve(m + 1, y, V - best_k);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);
    
    int n, V;
    cin >> n >> V;

    int c;
    for (int i = 0; i < n; i++) {
        cin >> c;
        coins.pb(c);
    }

    solve(0, n - 1, V);

    if (ans.size() == 0) {
        cout << "-1\n";
        return 0;
    }

    cout << ans.size() << "\n";

    for (int i = 0; i < (int)ans.size(); i++) {
        cout << ans[i] << " ";
    }

    cout << "\n";
}