// checker takes 3 arguments - paths to test.in, prog.out and solution
// the default checker is for singular ouput tasks:
// runs test.in through solution and compares to prog.out
// todo - write

#include <iostream>

int main(int argc, char* argv[]) {
    // argv[0] is always the name of the program itself.
    // argv[1] is the first actual argument provided by the user.

    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <your_argument>" << std::endl;
        return 1;
    }

    // Output the first argument
    std::cout << argv[1] << std::endl;

    return 0;
}