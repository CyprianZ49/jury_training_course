#include <bits/stdc++.h>

#define pb push_back
#define st first
#define nd second
typedef long long ll;
#define pll pair <ll, ll>

using namespace std;

const ll maxN = 200009;
const ll inf = 1000000009;

vector <pll> points;

ll dist(pll a, pll b) {
    ll x = a.st - b.st;
    ll y = a.nd - b.nd;
    return x * x + y * y;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);

    int n;
    cin >> n;

    ll x, y;
    for (int i = 0; i < n; i++) {
        cin >> x >> y;
        points.pb({x, y});
    }

    pll best_pair = {0, 1};

    cout << points[best_pair.st].st << " " << points[best_pair.st].nd << "\n";
    cout << points[best_pair.nd].st << " " << points[best_pair.nd].nd << "\n";

    // cout <<setprecision(10) << sqrt(best_dist) << "\n";
}