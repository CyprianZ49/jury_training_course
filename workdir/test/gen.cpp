#include <iostream>

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <your_argument>" << std::endl;
        return 1;
    }

    std::cout << argv[1] << '\n';

    return 0;
}