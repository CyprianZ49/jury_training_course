CXX = g++
BIN_DIR = tmp/bin
DEFAULT_FLAGS = -O2 -Wall -std=c++17

CHECKER_FLAGS = $(DEFAULT_FLAGS)
CHNG_FLAGS = $(DEFAULT_FLAGS)
GEN_FLAGS = $(DEFAULT_FLAGS)
INVER_FLAGS = $(DEFAULT_FLAGS)
BACKTRACK_FLAGS = $(DEFAULT_FLAGS)
BITSET_FLAGS = $(DEFAULT_FLAGS)
CHECKER_CHECKER_FLAGS = $(DEFAULT_FLAGS)
GREEDY_FLAGS = $(DEFAULT_FLAGS)
GREEDY_EXTRA_FLAGS = $(DEFAULT_FLAGS)
GREEDY_RANDOM_FLAGS = $(DEFAULT_FLAGS)
HYBRID_FLAGS = $(DEFAULT_FLAGS)
HYBRID_RANDOM_FLAGS = $(DEFAULT_FLAGS)
MAXTEST_DETECTOR_FLAGS = $(DEFAULT_FLAGS)
MEET_FLAGS = $(DEFAULT_FLAGS)

TARGETS = $(BIN_DIR)/checker $(BIN_DIR)/chng $(BIN_DIR)/gen $(BIN_DIR)/inver $(BIN_DIR)/backtrack $(BIN_DIR)/bitset $(BIN_DIR)/checker_checker $(BIN_DIR)/greedy $(BIN_DIR)/greedy_extra $(BIN_DIR)/greedy_random $(BIN_DIR)/hybrid $(BIN_DIR)/hybrid_random $(BIN_DIR)/maxtest_detector $(BIN_DIR)/meet

all: $(BIN_DIR) $(TARGETS)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

$(BIN_DIR)/checker: checker.cpp
	$(CXX) $(CHECKER_FLAGS) checker.cpp -o $(BIN_DIR)/checker

$(BIN_DIR)/chng: chng.cpp
	$(CXX) $(CHNG_FLAGS) chng.cpp -o $(BIN_DIR)/chng

$(BIN_DIR)/gen: gen.cpp
	$(CXX) $(GEN_FLAGS) gen.cpp -o $(BIN_DIR)/gen

$(BIN_DIR)/inver: inver.cpp
	$(CXX) $(INVER_FLAGS) inver.cpp -o $(BIN_DIR)/inver

$(BIN_DIR)/backtrack: backtrack.cpp
	$(CXX) $(BACKTRACK_FLAGS) backtrack.cpp -o $(BIN_DIR)/backtrack

$(BIN_DIR)/bitset: bitset.cpp
	$(CXX) $(BITSET_FLAGS) bitset.cpp -o $(BIN_DIR)/bitset

$(BIN_DIR)/checker_checker: checker_checker.cpp
	$(CXX) $(CHECKER_CHECKER_FLAGS) checker_checker.cpp -o $(BIN_DIR)/checker_checker

$(BIN_DIR)/greedy: greedy.cpp
	$(CXX) $(GREEDY_FLAGS) greedy.cpp -o $(BIN_DIR)/greedy

$(BIN_DIR)/greedy_extra: greedy_extra.cpp
	$(CXX) $(GREEDY_EXTRA_FLAGS) greedy_extra.cpp -o $(BIN_DIR)/greedy_extra

$(BIN_DIR)/greedy_random: greedy_random.cpp
	$(CXX) $(GREEDY_RANDOM_FLAGS) greedy_random.cpp -o $(BIN_DIR)/greedy_random

$(BIN_DIR)/hybrid: hybrid.cpp
	$(CXX) $(HYBRID_FLAGS) hybrid.cpp -o $(BIN_DIR)/hybrid

$(BIN_DIR)/hybrid_random: hybrid_random.cpp
	$(CXX) $(HYBRID_RANDOM_FLAGS) hybrid_random.cpp -o $(BIN_DIR)/hybrid_random

$(BIN_DIR)/maxtest_detector: maxtest_detector.cpp
	$(CXX) $(MAXTEST_DETECTOR_FLAGS) maxtest_detector.cpp -o $(BIN_DIR)/maxtest_detector

$(BIN_DIR)/meet: meet.cpp
	$(CXX) $(MEET_FLAGS) meet.cpp -o $(BIN_DIR)/meet

clean:
	rm -rf $(BIN_DIR)/*