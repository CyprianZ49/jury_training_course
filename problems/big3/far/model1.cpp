#include <bits/stdc++.h>

#define st first
#define nd second
#define pb push_back
#define point pair <ll, ll>

typedef long long ll;

using namespace std;

const ll maxC = 1000000009;

vector <point> points;
vector <point> convex_hull;



int main() {
    int n;
    cin >> n;

    ll offset_x = maxC;
    ll offset_y = maxC; 

    ll x, y;
    for (int i = 0; i < n; i++) {
        cin >> x >> y;
        
        offset_x = min(offset_x, x);
        offset_y = min(offset_y, y);

        points.pb({x, y});
    }

    for (int i = 0; i < n; i++) {
        cout << points[i].st << " " << points[i].nd << '\n';
    }
}