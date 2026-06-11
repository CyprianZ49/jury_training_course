CXX = g++
BIN_DIR = tmp/bin
DEFAULT_FLAGS = -O2 -Wall -std=c++17

DEFAULT_CHECKER_FLAGS = $(DEFAULT_FLAGS)
SAMPLE_FLAGS = $(DEFAULT_FLAGS)
GEN_FLAGS = $(DEFAULT_FLAGS)
INVER_FLAGS = $(DEFAULT_FLAGS)
INTEGER_FLAGS = $(DEFAULT_FLAGS)
BAD_FLAGS = $(DEFAULT_FLAGS)

TARGETS = $(BIN_DIR)/default_checker $(BIN_DIR)/sample $(BIN_DIR)/gen $(BIN_DIR)/inver $(BIN_DIR)/integer $(BIN_DIR)/bad

all: $(BIN_DIR) $(TARGETS)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

$(BIN_DIR)/default_checker: default_checker.cpp
	$(CXX) $(DEFAULT_CHECKER_FLAGS) default_checker.cpp -o $(BIN_DIR)/default_checker

$(BIN_DIR)/sample: sample.cpp
	$(CXX) $(SAMPLE_FLAGS) sample.cpp -o $(BIN_DIR)/sample

$(BIN_DIR)/gen: gen.cpp
	$(CXX) $(GEN_FLAGS) gen.cpp -o $(BIN_DIR)/gen

$(BIN_DIR)/inver: inver.cpp
	$(CXX) $(INVER_FLAGS) inver.cpp -o $(BIN_DIR)/inver

$(BIN_DIR)/integer: integer.cpp
	$(CXX) $(INTEGER_FLAGS) integer.cpp -o $(BIN_DIR)/integer

$(BIN_DIR)/bad: bad.cpp
	$(CXX) $(BAD_FLAGS) bad.cpp -o $(BIN_DIR)/bad

clean:
	rm -rf $(BIN_DIR)/*