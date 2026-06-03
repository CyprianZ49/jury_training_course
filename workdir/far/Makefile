CXX = g++
BIN_DIR = tmp/bin
DEFAULT_FLAGS = -O2 -Wall -std=c++17

CHECKER_FLAGS = $(DEFAULT_FLAGS)
FAR_FLAGS = $(DEFAULT_FLAGS)
GEN_FLAGS = $(DEFAULT_FLAGS)
INVER_FLAGS = $(DEFAULT_FLAGS)
BRUTE_N2_FLAGS = $(DEFAULT_FLAGS)
CONVEX_BUG_FLAGS = $(DEFAULT_FLAGS)
HULL_N2_FLAGS = $(DEFAULT_FLAGS)
JARVIS_FLAGS = $(DEFAULT_FLAGS)
MAXTEST_DETECTOR_FLAGS = $(DEFAULT_FLAGS)
MONOTONE_FLAGS = $(DEFAULT_FLAGS)
MONOTONE_EXTRA_FLAGS = $(DEFAULT_FLAGS)
TERRIBLE_FLAGS = $(DEFAULT_FLAGS)

TARGETS = $(BIN_DIR)/checker $(BIN_DIR)/far $(BIN_DIR)/gen $(BIN_DIR)/inver $(BIN_DIR)/brute_n2 $(BIN_DIR)/convex_bug $(BIN_DIR)/hull_n2 $(BIN_DIR)/jarvis $(BIN_DIR)/maxtest_detector $(BIN_DIR)/monotone $(BIN_DIR)/monotone_extra $(BIN_DIR)/terrible

all: $(BIN_DIR) $(TARGETS)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

$(BIN_DIR)/checker: checker.cpp
	$(CXX) $(CHECKER_FLAGS) checker.cpp -o $(BIN_DIR)/checker

$(BIN_DIR)/far: far.cpp
	$(CXX) $(FAR_FLAGS) far.cpp -o $(BIN_DIR)/far

$(BIN_DIR)/gen: gen.cpp
	$(CXX) $(GEN_FLAGS) gen.cpp -o $(BIN_DIR)/gen

$(BIN_DIR)/inver: inver.cpp
	$(CXX) $(INVER_FLAGS) inver.cpp -o $(BIN_DIR)/inver

$(BIN_DIR)/brute_n2: brute_n2.cpp
	$(CXX) $(BRUTE_N2_FLAGS) brute_n2.cpp -o $(BIN_DIR)/brute_n2

$(BIN_DIR)/convex_bug: convex_bug.cpp
	$(CXX) $(CONVEX_BUG_FLAGS) convex_bug.cpp -o $(BIN_DIR)/convex_bug

$(BIN_DIR)/hull_n2: hull_n2.cpp
	$(CXX) $(HULL_N2_FLAGS) hull_n2.cpp -o $(BIN_DIR)/hull_n2

$(BIN_DIR)/jarvis: jarvis.cpp
	$(CXX) $(JARVIS_FLAGS) jarvis.cpp -o $(BIN_DIR)/jarvis

$(BIN_DIR)/maxtest_detector: maxtest_detector.cpp
	$(CXX) $(MAXTEST_DETECTOR_FLAGS) maxtest_detector.cpp -o $(BIN_DIR)/maxtest_detector

$(BIN_DIR)/monotone: monotone.cpp
	$(CXX) $(MONOTONE_FLAGS) monotone.cpp -o $(BIN_DIR)/monotone

$(BIN_DIR)/monotone_extra: monotone_extra.cpp
	$(CXX) $(MONOTONE_EXTRA_FLAGS) monotone_extra.cpp -o $(BIN_DIR)/monotone_extra

$(BIN_DIR)/terrible: terrible.cpp
	$(CXX) $(TERRIBLE_FLAGS) terrible.cpp -o $(BIN_DIR)/terrible

clean:
	rm -rf $(BIN_DIR)/*