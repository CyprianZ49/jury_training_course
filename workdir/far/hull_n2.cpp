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
vector <pll> convex_hull;

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

    sort(points.begin(), points.end(), comp);

    convex_hull.pb(points[0]);
    convex_hull.pb(points[1]);
    for (int i = 2; i < (int)points.size(); i++) {
        while (convex_hull.size() >= 2 &&
               orient(convex_hull[convex_hull.size() - 2],
                      convex_hull[convex_hull.size() - 1],
                      points[i]) <= 0) {
            convex_hull.pop_back();
        }
        convex_hull.pb(points[i]);
    }

    ll best_dist = dist(convex_hull[0], convex_hull[1]);
    pll best_pair = {0, 1};

    for (int i = 0; i < (int)convex_hull.size(); i++) {
        for (int j = i + 1; j < (int)convex_hull.size(); j++) {
            if (best_dist < dist(convex_hull[i], convex_hull[j])) {
                best_dist = dist(convex_hull[i], convex_hull[j]);
                best_pair = {i, j};
            }
        }
    }

    for (int i = 0; i < (int)convex_hull.size(); i++) {
        convex_hull[i].st += shift_x;
        convex_hull[i].nd += shift_y;
    }

    cout << convex_hull[best_pair.st].st << " " << convex_hull[best_pair.st].nd << "\n";
    cout << convex_hull[best_pair.nd].st << " " << convex_hull[best_pair.nd].nd << "\n";

    // cout <<setprecision(10) << sqrt(best_dist) << "\n";
}