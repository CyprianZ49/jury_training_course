#include "oi.h"
#include <bits/stdc++.h>

using namespace std;
using namespace oi;

#define pb push_back
#define st first
#define nd second

typedef long long ll;

map <int, int> coins; 

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

    int n, V;
    test_file >> n >> V;

    int c;
    for (int i = 0; i < n; i++) {
        test_file >> c;
        coins[c] += 1;
    }
    
    int model_ans;
    model_file >> model_ans;

    int user_ans;
    user_ans = user_file.readInt();
    user_file.readEoln();

    if (model_ans != user_ans) {
        cout << "Wrong number of coins\n";
        return 1;
    }

    int sum = 0;
    for (int i = 0; i < user_ans; i++) {
        c = user_file.readUInt();
        user_file.readSpace();

        if (coins[c] <= 0) {
            cout << "There are no coins of value " << c << "left\n";
            return 1;
        }
        coins[c] -= 1;
        
        sum += c;
    }

    if (model_ans != -1) {
        user_file.readEoln();
    }

    user_file.readEof();

    if (sum != V && model_ans != -1) {
        cout << "Your coins do not add up to the correct sum\n";
        return 1;
    }

    cout << "OK";
    return 0;
}