CXX = g++
BIN_DIR = tmp/bin
DEFAULT_FLAGS = -O2 -Wall -std=c++17

DEFAULT_CHECKER_FLAGS = $(DEFAULT_FLAGS)
TEST2_FLAGS = $(DEFAULT_FLAGS)
GEN_FLAGS = $(DEFAULT_FLAGS)
IN_VER_FLAGS = $(DEFAULT_FLAGS)

TARGETS = $(BIN_DIR)/default_checker $(BIN_DIR)/test2 $(BIN_DIR)/gen $(BIN_DIR)/in_ver

all: $(BIN_DIR) $(TARGETS)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

$(BIN_DIR)/default_checker: default_checker.cpp
	$(CXX) $(DEFAULT_CHECKER_FLAGS) default_checker.cpp -o $(BIN_DIR)/default_checker

$(BIN_DIR)/test2: test2.cpp
	$(CXX) $(TEST2_FLAGS) test2.cpp -o $(BIN_DIR)/test2

$(BIN_DIR)/gen: gen.cpp
	$(CXX) $(GEN_FLAGS) gen.cpp -o $(BIN_DIR)/gen

$(BIN_DIR)/in_ver: in_ver.cpp
	$(CXX) $(IN_VER_FLAGS) in_ver.cpp -o $(BIN_DIR)/in_ver

clean:
	rm -rf $(BIN_DIR)/*