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

    for (int t = 0; t < 32; t++) {
        coins = save_coins;
        V = save_V;

        shuffle(coins.begin(), coins.end(), rng);
        
        for (int h = 0; h <= 1; h++) {
            for (int i = 0; i < maxN; i++) {
                best[h][i].st = inf;
            }
            best[h][0].st = 0;
        }

        int bt_depth = 12;

        backtrack(0, 0, 0, 0, bt_depth, V);

        int copy_V = V;

        int best_count = best[0][V].st;
        int best_greed_pref = 0;

        vector <int> ans;
        while (V > 0 && (int)coins.size() > bt_depth) {
            if (coins.back() <= V) {
                V -= coins.back();
                ans.pb(coins.back());
            }
            coins.pop_back();
            if (best[0][V].st + (int)ans.size() < best_count) {
                best_count = best[0][V].st + ans.size();
                best_greed_pref = ans.size();
            }
        }

        if (best_count < (int)best_ans.size()) {
            best_ans.clear();
            for (int i = 0; i < best_greed_pref; i++) {
                best_ans.pb(ans[i]);
                copy_V -= ans[i];
            }
            for (int i = 0; i < n; i++) {
                if (best[0][copy_V].nd[i] == 1) {
                    best_ans.pb(coins[i]);
                }
            }
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