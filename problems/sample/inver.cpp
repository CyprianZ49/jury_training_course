#include <bits/stdc++.h>
#include <random>
#include <chrono>

using namespace std;

int main(int argc, char* argv[]) {
    if (argc != 2) {
        return 1;
    }

    int s = atoi(argv[1]);
    if (s < 1 || s > 2) {
        cout << "Bad subtask number\n";
        return 1;
    }

    long long max_v = 0;
    if (s == 1) {
        max_v = 1000000000ll;
    }
    else if (s == 2) {
        max_v = 1000000000000000000ll;
    }

    long long a = 0, b = 0;

    cin >> a >> b;
    
    if (a < 1ll) {
        cout << "a < 1\n";
        return 1;
    }

    if (a > max_v) {
        cout << "a > " << max_v << " \n";
        return 1;
    }

    if (b < 1ll) {
        cout << "b < 1\n";
        return 1;
    }

    if (b > max_v) {
        cout << "b > " << max_v << " \n";
        return 1;
    }

    return 0;
}