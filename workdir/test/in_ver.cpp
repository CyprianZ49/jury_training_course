#include <iostream>
#include <string>

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <expected_n>" << std::endl;
        return 1;
    }

    int expected_n = std::stoi(argv[1]);
    int actual_n;

    if (!(std::cin >> actual_n)) {
        std::cout << "Error: Could not read integer from input." << std::endl;
        return 1; 
    }

    if (actual_n == expected_n) {
        return 0;
    } else {
        std::cout << "Validation Failed: Expected " << expected_n 
                  << " but found " << actual_n;
        return 1;
    }
}