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

bitset <maxN> ans;
bitset <maxN> current;
int best = inf;
int n, V;

void backtrack(int i, int sum, int count) {
    if (sum > V) return;

    if (sum == V) {
        if (count < best) {
            best = count;
            ans = current;
        }
        return;
    }

    if (i >= n) return;

    backtrack(i + 1, sum, count);
    current[i] = 1;
    backtrack(i + 1, sum + coins[i], count + 1);
    current[i] = 0;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);

    cin >> n >> V;

    int c;
    for (int i = 0; i < n; i++) {
        cin >> c;
        coins.pb(c);
    }

    backtrack(0, 0, 0);

    if (best == inf) {
        cout << "-1\n";
        return 0;
    }

    cout << best << "\n";

    for (int i = 0; i < n; i++) {
        if (ans[i] == 1) {
            cout << coins[i] << " ";
        }
    }

    cout << "\n";
}