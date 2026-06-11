#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cmath>
#include <iomanip>

using namespace std;

// maximum absolute error for comparing floating point numbers
const double epsilon = 1e-6;

bool is_double(const string& s, double& val) {
    int dot_count = 0;
    int digit_count = 0;

    for (int i = 0; i < (int)s.length(); i += 1) {
        if (s[i] >= '0' && s[i] <= '9') {
            digit_count += 1;
        }
        else if (s[i] == '.') {
            dot_count += 1;
        }
        else if (s[i] == '-') {
            if (i != 0) return false;
        }
        else {
            return false;
        }
    }

    if (dot_count != 1 || digit_count == 0) return false;

    val = strtod(s.c_str(), nullptr);
    return true;
}

bool tokens_match(const string& user, const string& model) {
    if (user == model) return true;

    double u_val, m_val;
    if (is_double(user, u_val) && is_double(model, m_val)) {
        return fabs(u_val - m_val) < epsilon;
    }
    return false;
}

string incorrect_info(const string& a, const string& b) {
    for (int i = 0; i < min((int)a.length(), (int)b.length()); i++)
        if (a[i] != b[i]) {
            int start_pos = max(0, i - 25);
            int end_pos = min((int)a.length() - 1, i + 25);
            string info;
            if (start_pos > 0) info += "<ommitted>";
            info += a.substr(start_pos, end_pos - start_pos + 1);
            if (end_pos < (int)a.length() - 1) info += "<ommitted>";
            return info;
        }
    if (a.length() != b.length()) {
        int start_pos = max(0, (int)a.length() - 30);
        string info;
        if (start_pos > 0) info += "<ommitted>";
        info += a.substr(start_pos, 30);
        return info;
    }
    return "";
}

bool is_whitespace(char ch) {
    return ((ch == ' ') || (ch == '\t') || (ch == '\n') || (ch == '\r'));
}

vector<string> tokenize(const string& s) {
  vector<string> tokens;
  string cur_token;
  for (int i = 0; i < (int)s.length(); i++) {
    if (is_whitespace(s[i])) {
      if (!cur_token.empty()) tokens.push_back(cur_token);
      cur_token = "";
    }
    else
      cur_token.push_back(s[i]);
  }
  if (!cur_token.empty()) tokens.push_back(cur_token);
  return tokens;
}

int main(int argc, char *argv[]) {
    if (argc < 4) {
        cout << "Checker expects arguments <test_input> <user_output> <model_solution_output>\n";
        return 1;
    }

    string input_path = argv[1];
    string user_out_path = argv[2];
    string model_out_path = argv[3];

    ifstream model_file(model_out_path);
    ifstream user_file(user_out_path);

    string correct_line;
    string user_line;
    int line_index = 1;
    while (getline(model_file, correct_line)) {
        if (!getline(user_file, user_line)) {
            vector<string> correct_tokens = tokenize(correct_line);
            if (!correct_tokens.empty()) {
                cout << "User output ended too early. "
                     << "Expected \"" << incorrect_info(correct_tokens[0], "") << "\" "
                     << "as first token on line " << line_index << ".\n";
                return 1;
            }
        }

        while (is_whitespace(correct_line.back())) correct_line.pop_back();
        while (is_whitespace(user_line.back())) user_line.pop_back();

        if (user_line != correct_line) {
            vector<string> correct_tokens = tokenize(correct_line);
            vector<string> user_tokens = tokenize(user_line);

            if (correct_tokens != user_tokens) {
                for (int i = 0; i < (int)min(correct_tokens.size(), user_tokens.size()); i++)
                    if (!tokens_match(user_tokens[i], correct_tokens[i])) {
                        cout << "Line " << line_index << ", token " << i+1
                             << " of user output is incorrect: "
                             << "\"" << incorrect_info(user_tokens[i], correct_tokens[i]) << "\""
                             << " instead of "
                             << "\"" << incorrect_info(correct_tokens[i], user_tokens[i]) << "\""
                             << ".\n";
                        return 1;
                    }
                if (user_tokens.size() < correct_tokens.size()) {
                    cout << "Line " << line_index
                         << " of user output is incorrect: "
                         << "end of line provided at token " << user_tokens.size() + 1 << " "
                         << "instead of "
                         << "\"" << incorrect_info(correct_tokens[user_tokens.size()], "") << "\""
                         << ".\n";
                    return 1;
                }
                if (user_tokens.size() > correct_tokens.size()) {
                     cout << "Line " << line_index
                         << " of user output is incorrect: "
                         << "at token " << correct_tokens.size() + 1 << " "
                         << "\"" << incorrect_info(user_tokens[correct_tokens.size()], "") << "\""
                         << " was provided instead of end of line character"
                         << ".\n";
                    return 1;
                }
            }

            cout << "Line " << line_index
                 << " of user output is incorrect: "
                 << "incorrect whitespaces between tokens"
                 << ".\n";
            return 1;
        }
        line_index++;
    }
    while (getline(user_file, user_line)) {
        vector<string> user_tokens = tokenize(user_line);
        if (!user_tokens.empty()) {
            cout << "User output contains excessive non-empty lines. "
                 << "Provided \"" << incorrect_info(user_tokens[0] , "") << "\" "
                 << "as the first token on line " << line_index << ".\n";
            return 1;
        }
        line_index++;
    }
    cout << "OK";
    return 0;
}