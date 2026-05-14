CXX = g++
BIN_DIR = tmp/bin
DEFAULT_FLAGS = -O2 -Wall -std=c++17

DEFAULT_CHECKER_FLAGS = $(DEFAULT_FLAGS)
A_FLAGS = $(DEFAULT_FLAGS)
GEN_FLAGS = $(DEFAULT_FLAGS)
IN_VER_FLAGS = $(DEFAULT_FLAGS)
B_FLAGS = $(DEFAULT_FLAGS)

TARGETS = $(BIN_DIR)/default_checker $(BIN_DIR)/a $(BIN_DIR)/gen $(BIN_DIR)/in_ver $(BIN_DIR)/b

all: $(BIN_DIR) $(TARGETS)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

$(BIN_DIR)/default_checker: default_checker.cpp
	$(CXX) $(DEFAULT_CHECKER_FLAGS) default_checker.cpp -o $(BIN_DIR)/default_checker

$(BIN_DIR)/a: a.cpp
	$(CXX) $(A_FLAGS) a.cpp -o $(BIN_DIR)/a

$(BIN_DIR)/gen: gen.cpp
	$(CXX) $(GEN_FLAGS) gen.cpp -o $(BIN_DIR)/gen

$(BIN_DIR)/in_ver: in_ver.cpp
	$(CXX) $(IN_VER_FLAGS) in_ver.cpp -o $(BIN_DIR)/in_ver

$(BIN_DIR)/b: b.cpp
	$(CXX) $(B_FLAGS) b.cpp -o $(BIN_DIR)/b

clean:
	rm -rf $(BIN_DIR)/*