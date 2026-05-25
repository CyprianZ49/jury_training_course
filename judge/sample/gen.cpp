#include <bits/stdc++.h>
#include <random>
#include <chrono>

using namespace std;

int main(int argc, char* argv[]) {
    auto seed = chrono::high_resolution_clock::now().time_since_epoch().count() ^ random_device{}();
    mt19937_64 rng(seed);

    // if (argc != 2) {
    //     return 1;
    // }

    int s = atoi(argv[1]);
    if (s < 1 || s > 2) {
        return 1;
    }

    long long max_v = 0;
    if (s == 1) {
        max_v = 1000000000ll;
    }
    else if (s == 2) {
        max_v = 1000000000000000000ll;
    }

    uniform_int_distribution<long long> dist(1ll, max_v);

    cout << dist(rng) << " " << dist(rng) << '\n';

    return 0;
}