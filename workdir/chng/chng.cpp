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
int dp[maxV];

bitset <maxV> improved[maxN];

int main() {
    int n, V;
    cin >> n >> V;

    int c;
    for (int i = 0; i < n; i++) {
        cin >> c;
        coins.pb(c);
    }

    for (int i = 0; i < maxV; i++) {
        dp[i] = inf;
    }

    dp[0] = 0;

    for (int i = 0; i < n; i++) {
        c = coins[i];
        for (int x = V; x >= c; x--) {
            if (dp[x - c] + 1 < dp[x]) {
                dp[x] = dp[x - c] + 1;
                improved[i][x] = 1;
            }
        }
    }

    if (dp[V] == inf) {
        cout << "-1\n";
        return 0;
    }
    
    cout << dp[V] << "\n";

    int i = n - 1;
    for (int x = V; x > 0; ) {
        while (improved[i][x] != 1) i--;
        cout << coins[i] << " ";
        x -= coins[i];
        i--;
    }

    cout << "\n";
}