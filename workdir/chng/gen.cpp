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

int subtask_limits_n[3] = {24, 48, 5000};
int max_V = 20000;

vector <int> coins;
int V, n;

int main(int argc, char* argv[]) {
    int subtask = atoi(argv[1]);
    int test_id = atoi(argv[2]);

    int seed = 23 + test_id;
    rng.setSeed(seed);

    n = subtask_limits_n[subtask - 1];

    if (test_id < 8) {
        int l = (rng.randUInt() % 20) + 50;
        int m = min(10, n / 3);
        for (int i = 0; i < n; i++) {
            if (i % 3 == 0) coins.pb(l);
            if (i % 3 == 1) coins.pb(l - 1);
            if (i % 3 == 2) coins.pb(1 + (rng.randUInt() % (l - m - 1)));
        }
        V = (n / 3) * l - m;
        while (V > max_V) V -= l; 
    }
    else if (test_id < 15) {
        V = 0;
        int primes[4] = {2, 3, 5, 7};

        int o = 1;
        int c;
        for (int i = 0; i < 4; i++) {
            o *= primes[i];
            for (int j = 1; j < primes[i]; j++) {
                int k = (rng.randUInt() % 15) + 1;
                c = o * k + 1;
                coins.pb(c);
                V += c;
            }
        }

        while ((int)coins.size() > n) {
            coins.pop_back();
        }

        for (int i = (int)coins.size(); i < n; i++) {
            int k = (rng.randUInt() % 30) + 1;
            c = o * k;
            coins.pb(c);
            if (V + c <= max_V) {
                V += c;
            }
        }

        if (V > max_V) {
            V = max_V;
        }
    }
    else if (test_id < 18) {
        for (int i = 0; i < n; i++) {
            int r = (rng.randUInt() % (max_V / 4)) + 1;
            coins.pb(r);
        }

        V = 0;
        for (int i = 0; i < n; i++) {
            if (V + coins[i] <= max_V) {
                V += coins[i];
            }
        }
    }
    else if (test_id < 19) {
        V = max_V;
        for (int i = 0; i < 2; i++) coins.pb(max_V / 2);
        for (int i = 2; i < n; i++) coins.pb(max_V  - 1);
    }
    else {
        for (int i = 0; i < n; i++) {
            int r = (rng.randUInt() % (max_V / 4)) + 1;
            coins.pb(r);
        }

        V = (rng.randUInt() % max_V) + 1;
    }

    rng.randomShuffle(coins.begin(), coins.end());

    cout << n << " " << V << "\n";
    for (int i = 0; i < n; i++) {
        cout << coins[i] << " ";
    }
    cout << "\n";
}