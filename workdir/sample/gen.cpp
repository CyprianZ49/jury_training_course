#include "bits/stdc++.h"
#include "oi.h"

#define pb push_back
#define st first
#define nd second

using namespace std;
using namespace oi;

Random rng;

int main(int argc, char* argv[]) {
    int subtask = atoi(argv[1]);
    int test_id = atoi(argv[2]);

    int seed = 23 + test_id;
    rng.setSeed(seed);

    ll max_x = 1;
    
    if (subtask == 1) {
        max_x = 1000000000;
    }
    else if (subtask == 2) {
        max_x = 1000000000000000000;
    }

    ll a = rng.randULL() % max_x;
    ll b = rng.randULL() % max_x;
    cout << a << " " << b << "\n";
}