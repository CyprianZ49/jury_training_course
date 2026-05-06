CXX = g++
BIN_DIR = bin
DEFAULT_FLAGS = -O2 -Wall -std=c++17

GEN_FLAGS = $(DEFAULT_FLAGS)
IN_VER_FLAGS = $(DEFAULT_FLAGS)

TARGETS = $(BIN_DIR)/gen $(BIN_DIR)/in_ver

all: $(BIN_DIR) $(TARGETS)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

bin/gen: gen.cpp
	$(CXX) $(GEN_FLAGS) gen.cpp -o bin/gen

bin/in_ver: in_ver.cpp
	$(CXX) $(IN_VER_FLAGS) in_ver.cpp -o bin/in_ver

clean:
	rm -rf $(BIN_DIR)/*