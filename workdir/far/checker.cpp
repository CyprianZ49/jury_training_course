#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cmath>
#include <iomanip>
#include "oi.h"

using namespace std;
using namespace oi;

#define pb push_back
#define st first
#define nd second

typedef long long ll;
#define pll pair <ll, ll>

ll dist(pll a, pll b) {
    ll x = a.st - b.st;
    ll y = a.nd - b.nd;
    return x * x + y * y;
}

int main(int argc, char *argv[]) {
    if (argc < 4) {
        cout << "Checker expects arguments <test_input> <user_output> <model_solution_output>\n";
        return 1;
    }

    string input_path = argv[1];
    string user_out_path = argv[2];
    string model_out_path = argv[3];

    ifstream test_file(input_path);
    ifstream model_file(model_out_path);
    Scanner user_file(user_out_path.c_str(), oi::EN);

    vector <pll> points;
    int n;
    test_file >> n;
    ll x, y;
    for (int i = 0; i < n; i++) {
        test_file >> x >> y;
        points.pb({x, y});
    }
    
    pll a, b;
    model_file >> a.st >> a.nd >> b.st >> b.nd;

    
    pll c, d;
    c.st = user_file.readLL();
    user_file.readSpace();
    c.nd = user_file.readLL();
    user_file.readEoln();

    d.st = user_file.readLL();
    user_file.readSpace();
    d.nd = user_file.readLL();
    user_file.readEoln();

    user_file.readEof();

    bool c_valid = false;
    bool d_valid = false;

    for (int i = 0; i < n; i++) {
        if (c == points[i]) c_valid = true;
        if (d == points[i]) d_valid = true;
    }

    if (!c_valid || !d_valid) {
        cout << "Output points are not present in input.\n";
        return 1;
    }

    if (c == d) {
        cout << "You outputed the same point twice.\n";
        return 1;
    }

    if (dist(a, b) > dist(c, d)) {
        cout << "There is a pair of points with larger distance.\n";
        return 1;
    }

    if (dist(a, b) < dist(c, d)) {
        cout << "This is very wrong - user did better than model!\n";
        return 1;
    }

    cout << "OK";
    return 0;
}