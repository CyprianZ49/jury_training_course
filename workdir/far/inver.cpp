#include "bits/stdc++.h"
#include "oi.h"

#define pb push_back

typedef long long ll;

using namespace std;
using namespace oi;

Scanner input(stdin, oi::EN);

int subtask_limits_n[2] = {10000, 200000};
ll min_x = -1000000000;
ll max_x = 1000000000;

int main(int argc, char* argv[]) {
    int subtask = atoi(argv[1]);

    int n_limit = subtask_limits_n[subtask - 1];

    int n = input.readInt(2, n_limit);
    input.readEoln();

    vector <pair <ll, ll> > points;

    for (int i = 0; i < n; i++) {
        ll x = input.readLL(min_x, max_x);
        input.readSpace();
        ll y = input.readLL(min_x, max_x);
        input.readEoln();
        points.pb({x, y});
    }

    input.readEof();

    sort(points.begin(), points.end());

    for (int i = 1; i < n; i++) {
        if (points[i] == points[i - 1]) {
            cout << "The point " << points[i].first << " " << points[i].second << "appears twice.\n";
            return 1;
        }
    }

    return 0;
}