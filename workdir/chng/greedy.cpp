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

int main() {
    int n, V;
    cin >> n >> V;

    int c;
    for (int i = 0; i < n; i++) {
        cin >> c;
        coins.pb(c);
    }

    sort(coins.begin(), coins.end());

    vector <int> ans;
    while (V > 0 && !coins.empty()) {
        if (coins.back() <= V) {
            V -= coins.back();
            ans.pb(coins.back());
        }
        coins.pop_back();
    }

    if (V > 0) {
        cout << "-1\n";
        return 0;
    }

    cout << ans.size() << "\n";

    for (int i = 0; i < (int)ans.size(); i++) {
        cout << ans[i] << " ";
    }

    cout << "\n";
}