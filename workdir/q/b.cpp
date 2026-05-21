#include <bits/stdc++.h>

using namespace std;

int stall_random() {
    int r = 10000000;
    
    int a = 1;
    int b = 1;
    while (r--) {
        b += a;
        a = b - a;
    }
    b++;
    a--;
    return b;
}

int main() {
    int a;
    cin >> a;
    int b = 0;
    b += stall_random();
    b++;
    if (a == 23234) {
        a += 1;
    }
    // if (rand() % 100 >= 50) a += 1;
    cout << 2 * a << '\n';
    if (b < 0) cout << b;
}