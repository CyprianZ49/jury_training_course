#include <iostream>
#include <string>

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <n>" << std::endl;
        return 1;
    }

    try {
        int n = std::stoi(argv[1]);
        
        std::cout << n << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error: Argument must be an integer." << std::endl;
        return 1;
    }

    return 0;
}