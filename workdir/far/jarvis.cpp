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
vector <pll> hull;

ll dist(pll a, pll b) {
    ll x = a.st - b.st;
    ll y = a.nd - b.nd;
    return x * x + y * y;
}

ll orient(pll a, pll b, pll c) {
    b.st -= a.st;
    b.nd -= a.nd;
    c.st -= a.st;
    c.nd -= a.nd;
    return b.st * c.nd - c.st * b.nd;
}

bool comp (pll x, pll y) {
    ll o = orient({0, 0}, x, y);
    if (o != 0) return o > 0;
    return dist({0, 0}, x) < dist({0, 0}, y);
}

int main() {
    int n;
    cin >> n;

    ll shift_x = 0, shift_y = inf;
    ll x, y;
    for (int i = 0; i < n; i++) {
        cin >> x >> y;
        points.pb({x, y});
        if (y < shift_y || (y == shift_y && x < shift_x)) {
            shift_x = x;
            shift_y = y;
        }
    }

    for (int i = 0; i < (int)points.size(); i++) {
        points[i].st -= shift_x;
        points[i].nd -= shift_y;
    }

    int current = 0;
    while (points[current] != (pll){0, 0}) current++;

    do {
        hull.pb(points[current]);
        int next = (current + 1) % n;
        for (int i = 0; i < n; i++) {
            ll o = orient(points[current], points[next], points[i]);
            if (o < 0 || (o == 0 && dist(points[current], points[i]) > dist(points[current], points[next]))) {
                next = i;
            }
        }
        current = next;
    } while (points[current] != (pll){0, 0});

    int s = hull.size();

    int i1 = 0;
    int i2 = s - 1;
    while (hull[i2].nd <= hull[i2 - 1].nd) i2--;

    ll best_dist = dist(hull[i1], hull[i2]);
    pll best_pair = {i1, i2};

    for (int k = 0; k < 2 * s; k++) {
        ll o1 = orient(hull[i1], hull[(i1 + 1) % s], hull[i2]);
        ll o2 = orient(hull[i1], hull[(i1 + 1) % s], hull[(i2 + 1) % s]);
        if (o1 < o2) {
            i2 += 1;
            i2 %= s;
        }
        else {
            i1 += 1;
            i1 %= s;
        }

        if (best_dist < dist(hull[i1], hull[i2])) {
            best_dist = dist(hull[i1], hull[i2]);
            best_pair = {i1, i2};
        }
    }

    for (int i = 0; i < s; i++) {
        hull[i].st += shift_x;
        hull[i].nd += shift_y;
    }

    cout << hull[best_pair.st].st << " " << hull[best_pair.st].nd << "\n";
    cout << hull[best_pair.nd].st << " " << hull[best_pair.nd].nd << "\n";

    // cout <<setprecision(10) << sqrt(best_dist) << "\n";
}