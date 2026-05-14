#include <iostream>
#include <string>

int main(int argc, char* argv[]) {
    // Check if the expected n was provided as a constraint
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <expected_n>" << std::endl;
        return 1;
    }

    int expected_n = std::stoi(argv[1]);
    int actual_n;

    // Read from stdin (which is redirected from your .in file in Python)
    if (!(std::cin >> actual_n)) {
        std::cout << "Error: Could not read integer from input." << std::endl;
        return 1; 
    }

    // Validation logic
    if (actual_n == expected_n) {
        // Success: Exit code 0
        return 0;
    } else {
        // Failure: Print message to stdout (captured by your Python script)
        std::cout << "Validation Failed: Expected " << expected_n 
                  << " but found " << actual_n;
        return 1;
    }
}