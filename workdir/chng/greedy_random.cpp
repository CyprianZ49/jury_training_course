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
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);
    
    mt19937 rng(23);

    int n, V;
    cin >> n >> V;

    int c;
    for (int i = 0; i < n; i++) {
        cin >> c;
        coins.pb(c);
    }

    vector <int> save_coins = coins;
    int save_V = V;

    vector <int> best_ans;
    best_ans.resize(maxN);

    for (int t = 0; t < maxV; t++) {
        coins = save_coins;
        V = save_V;

        shuffle(coins.begin(), coins.end(), rng);

        vector <int> ans;
        while (V > 0 && !coins.empty()) {
            if (coins.back() <= V) {
                V -= coins.back();
                ans.pb(coins.back());
            }
            coins.pop_back();
        }

        if (V == 0 && ans.size() < best_ans.size()) {
            best_ans = ans;
        }
    }

    if (best_ans.size() == maxN) {
        cout << "-1\n";
        return 0;
    }

    cout << best_ans.size() << "\n";
    
    for (int i = 0; i < (int)best_ans.size(); i++) {
        cout << best_ans[i] << " ";
    }

    cout << "\n";
}