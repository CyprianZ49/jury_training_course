input format:

n (up to 2*10^5) - number of vertices
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
brutal mark

break when max-test

break when non-sorted test
mark but no_cleanup
break specifically on anc or =