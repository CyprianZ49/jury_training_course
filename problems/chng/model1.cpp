#include <bits/stdc++.h>

using namespace std;

typedef long long ll;

struct entry {
    int min_coins;
    int last_coin;
    ll possible_ways;
};

const ll mod = 1000000007;
const int maxW = 10009;
const ll inf = maxW + 10;
vector <int> coins;
vector <int> amount;
entry dp[maxW];


int main() {
    int n;
    cin >> n;

    // it is guaranteed that all coins have different nominals
    ll c;
    for (int i = 0; i < n; i++) {
        cin >> c;
        coins.push_back(c);
        amount.push_back(0);
    }

    ll W;
    cin >> W;

    dp[0].min_coins = 0;
    dp[0].last_coin = -1;
    dp[0].possible_ways = 1;

    for (int i = 1; i < maxW; i++) {
        dp[i].min_coins = inf;
    }

    for (int i = 0; i < n; i++) {
        c = coins[i];
        for (int w = c; w <= W; w += 1) {
            if (dp[w].min_coins > dp[w - c].min_coins + 1) {
                dp[w].min_coins = dp[w - c].min_coins + 1;
                dp[w].last_coin = i;
                dp[w].possible_ways = dp[w - c].possible_ways;
            }
            else if (dp[w].min_coins == dp[w - c].min_coins + 1) {
                dp[w].possible_ways += dp[w - c].possible_ways;
                dp[w].possible_ways %= mod;
            }
        }
    }

    if (dp[W].min_coins == inf) {
        cout << "-1\n";
        return 0;
    }
    
    cout << dp[W].min_coins << " " << dp[W].possible_ways << '\n';

    for (int w = W; w > 0; ) {
        c = dp[w].last_coin;
        amount[c] += 1;
        w -= coins[c];
    }

    for (int i = 0; i < n; i++) {
        cout << amount[i] << " ";
    }
    cout << '\n';
}