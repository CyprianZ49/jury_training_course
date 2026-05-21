### External verification

judge dirs look like packages but with 1 extra config with:
path to working_package
path to master_package
(and master packages have an extra inver_counterexamples dir)

judge_init
loads master_package into judge
prepares judge_config
loads master_text into wworking_package

judge_model
copies working model_solution bin to judge
adds it's entry into config as a program which passes all
run_tests on this prog

judge_full

ensures memory limit and subtasks match
ensures trusted brute force isn't None

replaces judge checker and inver with working
runs full internal verification
runs bonus inver check on counterexamples
gets package back to normal

finally replaces testcases and generator
runs full verify

runs judge_model
gets package to normal

removes all progs and replaces them with workdir counterparts
removes trusted brute-force
full verify (only inver is wasted)
gets to normal

checks if all subtask combs in master progs are present in working progs


### Part extra

0. On judge init copy text
1. Units
2. Coloring
3. toOI
4. fromOI
5. random place to write this down but this is important - user needs to run make for problems (maybe auto setup somehow?)
6. all programs in master package have names with unique prefix (or something) (maybe reserved name for model?)