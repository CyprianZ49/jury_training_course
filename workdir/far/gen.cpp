#include "bits/stdc++.h"
#include "oi.h"

#define pb push_back
#define st first
#define nd second

using namespace std;
using namespace oi;

Random rng;

int subtask_limits_n[2] = {10000, 200000};
ll min_x = -1000000000;
ll max_x = 1000000000;

int main(int argc, char* argv[]) {
    int subtask = atoi(argv[1]);
    int test_id = atoi(argv[2]);

    int seed = 23 + test_id;
    rng.setSeed(seed);

    int n = subtask_limits_n[subtask - 1];

    cout << n << "\n";

    for (int i = 0; i < n; i++) {
        cout << rng.randSInt(min_x, max_x) << " ";
        cout << rng.randSInt(min_x, max_x) << "\n";
    }
}