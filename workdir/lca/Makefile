CXX = g++
BIN_DIR = tmp/bin
DEFAULT_FLAGS = -O2 -Wall -std=c++17

DEFAULT_CHECKER_FLAGS = $(DEFAULT_FLAGS)
LCA_FLAGS = $(DEFAULT_FLAGS)
GEN_FLAGS = $(DEFAULT_FLAGS)
INVER_FLAGS = $(DEFAULT_FLAGS)
ANC_EDGECASE_FLAGS = $(DEFAULT_FLAGS)
DEPTH_FLAGS = $(DEFAULT_FLAGS)
EASY_GEN_CHECKER_FLAGS = $(DEFAULT_FLAGS)
EULER_TOUR_FLAGS = $(DEFAULT_FLAGS)
HLD_FLAGS = $(DEFAULT_FLAGS)
JUMP_FLAGS = $(DEFAULT_FLAGS)
MARK_FLAGS = $(DEFAULT_FLAGS)
MAXTEST_DETECTOR_FLAGS = $(DEFAULT_FLAGS)
MEMO_FLAGS = $(DEFAULT_FLAGS)
ROOT_1_CHECKER_FLAGS = $(DEFAULT_FLAGS)
SQRT_FLAGS = $(DEFAULT_FLAGS)
TERRIBLE_FLAGS = $(DEFAULT_FLAGS)

TARGETS = $(BIN_DIR)/default_checker $(BIN_DIR)/lca $(BIN_DIR)/gen $(BIN_DIR)/inver $(BIN_DIR)/anc_edgecase $(BIN_DIR)/depth $(BIN_DIR)/easy_gen_checker $(BIN_DIR)/euler_tour $(BIN_DIR)/hld $(BIN_DIR)/jump $(BIN_DIR)/mark $(BIN_DIR)/maxtest_detector $(BIN_DIR)/memo $(BIN_DIR)/root_1_checker $(BIN_DIR)/sqrt $(BIN_DIR)/terrible

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

$(BIN_DIR)/anc_edgecase: anc_edgecase.cpp
	$(CXX) $(ANC_EDGECASE_FLAGS) anc_edgecase.cpp -o $(BIN_DIR)/anc_edgecase

$(BIN_DIR)/depth: depth.cpp
	$(CXX) $(DEPTH_FLAGS) depth.cpp -o $(BIN_DIR)/depth

$(BIN_DIR)/easy_gen_checker: easy_gen_checker.cpp
	$(CXX) $(EASY_GEN_CHECKER_FLAGS) easy_gen_checker.cpp -o $(BIN_DIR)/easy_gen_checker

$(BIN_DIR)/euler_tour: euler_tour.cpp
	$(CXX) $(EULER_TOUR_FLAGS) euler_tour.cpp -o $(BIN_DIR)/euler_tour

$(BIN_DIR)/hld: hld.cpp
	$(CXX) $(HLD_FLAGS) hld.cpp -o $(BIN_DIR)/hld

$(BIN_DIR)/jump: jump.cpp
	$(CXX) $(JUMP_FLAGS) jump.cpp -o $(BIN_DIR)/jump

$(BIN_DIR)/mark: mark.cpp
	$(CXX) $(MARK_FLAGS) mark.cpp -o $(BIN_DIR)/mark

$(BIN_DIR)/maxtest_detector: maxtest_detector.cpp
	$(CXX) $(MAXTEST_DETECTOR_FLAGS) maxtest_detector.cpp -o $(BIN_DIR)/maxtest_detector

$(BIN_DIR)/memo: memo.cpp
	$(CXX) $(MEMO_FLAGS) memo.cpp -o $(BIN_DIR)/memo

$(BIN_DIR)/root_1_checker: root_1_checker.cpp
	$(CXX) $(ROOT_1_CHECKER_FLAGS) root_1_checker.cpp -o $(BIN_DIR)/root_1_checker

$(BIN_DIR)/sqrt: sqrt.cpp
	$(CXX) $(SQRT_FLAGS) sqrt.cpp -o $(BIN_DIR)/sqrt

$(BIN_DIR)/terrible: terrible.cpp
	$(CXX) $(TERRIBLE_FLAGS) terrible.cpp -o $(BIN_DIR)/terrible

clean:
	rm -rf $(BIN_DIR)/*