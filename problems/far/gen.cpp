#include "bits/stdc++.h"
#include "oi.h"

#define pb push_back
#define st first
#define nd second
typedef long long ll;
#define pll pair <ll, ll>

using namespace std;
using namespace oi;

Random rng;

int subtask_limits_n[2] = {10000, 200000};
ll min_x = -1000000000;
ll max_x = 1000000000;

ll orient(pll a, pll b, pll c) {
    b.st -= a.st;
    b.nd -= a.nd;
    c.st -= a.st;
    c.nd -= a.nd;
    return b.st * c.nd - c.st * b.nd;
}

bool comp (pll x, pll y) {
    ll o = orient({0, 0}, x, y);
    return o < 0;
}

ll dist(pll a, pll b) {
    ll x = a.st - b.st;
    ll y = a.nd - b.nd;
    return x * x + y * y;
}

ll find_y(ll x, ll radius) {
    ll l = 0;
    ll r = max_x;
    while (l != r) {
        ll m = (l + r + 1) / 2;
        if (dist({0, 0}, {x, m}) <= dist({0, 0}, {0, radius})) {
            l = m;
        }
        else {
            r = m - 1;
        }
    }
    return l;
}

vector <pll> shifts;
vector <pll> shifts2;

map <pll, bool> used;

vector <pll> get_tooth(ll v) {
    pll a, b, c;
    bool success = false;

    while (!success) {
        a = {v, 0};

        b.st = rng.randSInt(100, v - 1);
        b.nd = find_y(b.st, v);

        for (ll x = b.st - 1; x > b.st - 100 && x > 0; x--) {
            ll y = b.nd * (v - x) / (v - b.st);
            c = {x, y};

            ll d1 = dist({-v, 0}, b);
            ll d2 = dist({-v, 0}, c);

            if (d2 > d1) {
                success = true;
                break;
            }
        }
    }

    vector <pll> ans = {a, b, c};

    return ans;
}

int main(int argc, char* argv[]) {
    int subtask = atoi(argv[1]);
    int test_id = atoi(argv[2]);

    int seed = 23 + test_id;
    rng.setSeed(seed);

    for (ll i = 1; i <= 680; i++) {
        for (ll j = 1; j <= 680; j++) {
            if (__gcd(i, j) == 1) {
                shifts.pb({i, j});
            }
        }
    }

    int n = subtask_limits_n[subtask - 1];

    cout << n << "\n";

    if (test_id < 4) {
        for (int i = 0; i < n; i++) {
            ll x = rng.randSInt(min_x, max_x);
            ll y = rng.randSInt(min_x, max_x);
            pll xy = {x, y};
            if (used[xy]) {
                i--;
            }
            else {
                used[xy] = true;
                cout << x << " " << y << "\n";
            }
        }
    }
    else if (test_id < 6) {
        vector <pll> test;

        for (ll i = 0; (int)test.size() < n; i++) {
            for (ll j = 0; j <= i && (int)test.size() < n; j++) {
                test.pb({i, j});
            }
        }

        rng.randomShuffle(test.begin(), test.end());

        for (int i = 0; i < (int)test.size(); i++) {
            cout << test[i].st << " " << test[i].nd << "\n";
        }
    }
    else if (test_id < 16) {
        vector <pll> test;

        int n_2 = n / 2;
        for (int i = 0; i < n_2; i++) {
            ll r = rng.randUInt() % shifts.size();
            shifts2.pb(shifts[r]);
            swap(shifts[r], shifts.back());
            shifts.pop_back();
        }
        sort(shifts2.begin(), shifts2.end(), comp);
        ll sum_x = 0, sum_y = 0;
        for (int i = 0; i < (int)shifts2.size(); i++) {
            sum_x += shifts2[i].st;
            sum_y += shifts2[i].nd;
        }
        ll x, y;
        x = -sum_x;
        y = 0;
        for (int i = 0; i < (int)shifts2.size() && n > 0; i++) {
            test.pb({x, y});
            n--;
            x += shifts2[i].st;
            y += shifts2[i].nd;
        }
        x = sum_x;
        y = 0;
        for (int i = 0; i < (int)shifts2.size() && n > 0; i++) {
            test.pb({x, y});
            n--;
            x -= shifts2[i].st;
            y -= shifts2[i].nd;
        }

        rng.randomShuffle(test.begin(), test.end());

        for (int i = 0; i < (int)test.size(); i++) {
            cout << test[i].st << " " << test[i].nd << "\n";
        }
    }
    else {
        vector <pll> tooth1 = get_tooth(max_x / 10);
        vector <pll> tooth2 = get_tooth(max_x / 10);

        ll sgn = (test_id % 2 == 0 ? 1 : -1);

        for (int i = 0; i < 3; i++) {
            cout << tooth1[i].st * sgn << " " << tooth1[i].nd << "\n";
        }

        for (int i = 0; i < 3; i++) {
            cout << tooth2[i].st * sgn *(-1) << " " << tooth2[i].nd * (-1) << "\n";
        }

        for (int i = 6; i < n; i++) {
            ll x = rng.randSInt(-10000, 10000);
            ll y = rng.randSInt(-10000, 10000);
            pll xy = {x, y};
            if (used[xy]) {
                i--;
            }
            else {
                used[xy] = true;
                cout << x << " " << y << "\n";
            }
        }
    }
}