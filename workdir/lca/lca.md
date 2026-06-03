input format:

n (up to 2*10^5) (at least 2) - number of vertices
q (up to 2*10^5) - number of queries

r - root

n-1 lines with a-b

q lines lca(a, b)

subtasks:
1. n <= 2 * 10^3, q <= 2 * 10^3
2. n <= 2 * 10^3, q <= 2 * 10^5
3. n <= 2 * 10^5, q <= 2 * 10^3
4. full



checklist:

binary-lifting anc - DONE
bin-lift jump - DONE
euler-tour trick - DONE
hld - DONE

sqr jump  - DONE
precalc all pairs (dp with mem) - DONE

brutal depth - DONE
brutal mark - DONE

break when max-test - DONE
break when root != 1 - DONE

break when non-sorted test - DONE
mark but no_cleanup as a very bad example - DONE
break specifically on anc or = - DONE


inver is rather simple maybe except OI.h usage
gen:
completely random
binary tree with 


don't forget inver_tests!