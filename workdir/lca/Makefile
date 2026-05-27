CXX = g++
BIN_DIR = tmp/bin
DEFAULT_FLAGS = -O2 -Wall -std=c++17

DEFAULT_CHECKER_FLAGS = $(DEFAULT_FLAGS)
LCA_FLAGS = $(DEFAULT_FLAGS)
GEN_FLAGS = $(DEFAULT_FLAGS)
INVER_FLAGS = $(DEFAULT_FLAGS)
SLOW1_FLAGS = $(DEFAULT_FLAGS)

TARGETS = $(BIN_DIR)/default_checker $(BIN_DIR)/lca $(BIN_DIR)/gen $(BIN_DIR)/inver $(BIN_DIR)/slow1

all: $(BIN_DIR) $(TARGETS)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

$(BIN_DIR)/default_checker: default_checker.cpp
	$(CXX) $(DEFAULT_CHECKER_FLAGS) default_checker.cpp -o $(BIN_DIR)/default_checker

$(BIN_DIR)/lca: lca.cpp
	$(CXX) $(LCA_FLAGS) lca.cpp -o $(BIN_DIR)/lca

$(BIN_DIR)/gen: gen.cpp
	$(CXX) $(GEN_FLAGS) gen.cpp -o $(BIN_DIR)/gen

$(BIN_DIR)/inver: inver.cpp
	$(CXX) $(INVER_FLAGS) inver.cpp -o $(BIN_DIR)/inver

$(BIN_DIR)/slow1: slow1.cpp
	$(CXX) $(SLOW1_FLAGS) slow1.cpp -o $(BIN_DIR)/slow1

clean:
	rm -rf $(BIN_DIR)/*